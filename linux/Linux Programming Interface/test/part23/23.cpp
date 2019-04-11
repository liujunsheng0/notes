#define _POSIX_C_SOURCE 199309
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <stdio.h>

static volatile sig_atomic_t gotAlarm = 0;

void exit_(char *msg) {
    printf("error %s\n", msg);
    _exit(EXIT_FAILURE);
}

void displayTimes(const char *msg, bool includeTimer)
{
    struct itimerval itv;
    static struct timeval start;
    struct timeval curr;
    static int callNum = 0;             /* Number of calls to this function */

    if (callNum == 0)                   /* Initialize elapsed time meter */
        if (gettimeofday(&start, NULL) == -1) {
            exit_("gettimeofday");
        }

    if (callNum % 20 == 0) {
        printf("       Elapsed   It Value  Interval\n");
    }

    if (gettimeofday(&curr, NULL) == -1) {
        exit_("gettimeofday");
    }
    printf("%-7s %6.2f", msg, curr.tv_sec - start.tv_sec +
                              (curr.tv_usec - start.tv_usec) / 1000000.0);

    if (includeTimer) {
        if (getitimer(ITIMER_REAL, &itv) == -1) {
            exit_("getitimer");
        }
        printf("  %6.2f  %6.2f",
               itv.it_value.tv_sec + itv.it_value.tv_usec / 1000000.0,
               itv.it_interval.tv_sec + itv.it_interval.tv_usec / 1000000.0);
    }

    printf("\n");
    callNum++;
}
void sigalrmHandler(int sig)
{
    gotAlarm = 1;
}

void test_get_setitimer(int argc, char *argv[]) {
    struct itimerval itv;
    clock_t prevClock;
    int maxSigs;                /* Number of signals to catch before exiting */
    int sigCnt;                 /* Number of signals so far caught */
    struct sigaction sa;

    itv.it_value.tv_sec = 5;
    itv.it_value.tv_usec = 0;
    itv.it_interval.tv_sec = 5;
    itv.it_interval.tv_usec = 0;

    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sa.sa_handler = sigalrmHandler;
    if (sigaction(SIGALRM, &sa, NULL) == -1) {
        exit_("sigaction");
    }

    maxSigs = (itv.it_interval.tv_sec == 0 && itv.it_interval.tv_usec == 0) ? 1 : 3;

    displayTimes("START:  ", false);
    if (setitimer(ITIMER_REAL, &itv, NULL) == -1) {
        exit_("setitimer");
    }

    prevClock = clock();
    sigCnt = 0;

    while (true) {
        /* Inner loop consumes at least 0.5 seconds CPU time */
        while (((clock() - prevClock) * 10 / CLOCKS_PER_SEC) < 5) {
            if (gotAlarm) {                     /* Did we get a signal? */
                gotAlarm = 0;
                displayTimes("SIGALRM:", true);
                sigCnt++;
                if (sigCnt >= maxSigs) {
                    printf("finish\n");
                    return;
                }
            }
        }

        prevClock = clock();
        displayTimes("While:  ", true);
    }
}


static void handler(int sig)
{
    printf("Caught signal\n");          /* UNSAFE (see Section 21.1.2) */
}

void test_timeout(bool is_restart) {
    printf("sigaction is SA_RESTART? %d\n", is_restart);
    struct sigaction sa;
    #define BUF_SIZE 200
    char buf[BUF_SIZE];
    ssize_t numRead;
    int savedErrno;

    sa.sa_flags = 0;
    if (is_restart) {
        sa.sa_flags = SA_RESTART;
    }
    sigemptyset(&sa.sa_mask);
    sa.sa_handler = handler;
    if (sigaction(SIGALRM, &sa, NULL) == -1) {
        exit_("sigaction");
    }

    struct itimerval itv;
    itv.it_value.tv_sec = 5;
    itv.it_value.tv_usec = 0;
    itv.it_interval.tv_sec = 5;
    itv.it_interval.tv_usec = 0;

    if (setitimer(ITIMER_REAL, &itv, NULL) == -1) {
        exit_("setitimer 1");
    }
    savedErrno = errno;                 /* In case alarm() changes it */

    numRead = read(STDIN_FILENO, buf, BUF_SIZE);
    itv.it_value.tv_sec = 0;
    itv.it_value.tv_usec = 0;
    itv.it_interval.tv_sec = 0;
    itv.it_interval.tv_usec = 0;
    if (setitimer(ITIMER_REAL, &itv, NULL) == -1) {
        exit_("setitimer 2");
    }

    errno = savedErrno;

    /* Determine result of read() */

    if (numRead == -1) {
        if (errno == EINTR) {
            printf("Read timed out\n");
        }
        else {
            exit_("read error");
        }
    } else {
        printf("Successful read (%ld bytes): %.*s", (long) numRead, (int) numRead, buf);
    }
}

int main(int argc, char *argv[])
{
//    test_get_setitimer(argc, argv);
    test_timeout(false);
    test_timeout(true);
}