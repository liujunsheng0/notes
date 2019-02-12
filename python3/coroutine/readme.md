[github ����](https://github.com/liujunsheng0/study_py3/tree/master/coroutine)   https://github.com/liujunsheng0/study_py3/tree/master/coroutine

# �Ķ�˳��

1. readme.md
2. coroutine_test.py
3. asyc_test.py
4. consumer_produce.py
5. aio_http

# [�첽IO](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143208573480558080fa77514407cb23834c78c6c7309000)

**ͬ��IO��**CPU���ٶ�ԶԶ���ڴ��̡������IO����һ���߳��У�CPUִ�д�����ٶȼ��죬Ȼ����һ������IO���������д�ļ���������������ʱ������Ҫ�ȴ�IO������ɣ����ܼ���������һ��������

��IO�����Ĺ����У���ǰ�̱߳����𣬶�������ҪCPUִ�еĴ�����޷�����ǰ�߳�ִ�С�

��Ϊһ��IO�����������˵�ǰ�̣߳��������������޷�ִ�У��������Ǳ���ʹ�ö��̻߳��߶����������ִ�д��룬Ϊ����û�����ÿ���û��������һ���̣߳��������IO�����̱߳����������û����̲߳���Ӱ�졣

���̺߳Ͷ���̵�ģ����Ȼ����˲������⣬����ϵͳ���������޵������̡߳�����ϵͳ�л��̵߳Ŀ���Ҳ�ܴ����ԣ�һ���߳��������࣬CPU��ʱ��ͻ����߳��л����ˣ��������д����ʱ������ˣ�����������������½���

��������Ҫ�����������CPU����ִ��������IO�豸�Ĺ������ز�ƥ�䣬���̺߳Ͷ����ֻ�ǽ����һ�����һ�ַ�����

��һ�ֽ��IO����ķ�����**�첽IO**����������Ҫִ��һ����ʱ��IO����ʱ����ֻ����IOָ������ȴ�IO�����Ȼ���ȥִ�����������ˡ�һ��ʱ��󣬵�IO���ؽ��ʱ����֪ͨCPU���д���

���������������ͨ˳��д���Ĵ���ʵ������û������첽IO�ģ�

```python
do_some_code()
f = open(file, 'r')
r = f.read() # <== �߳�ͣ�ڴ˴��ȴ�IO�������
# IO������ɺ��̲߳��ܼ���ִ��:
do_some_code(r)
```

------

**�첽IOģ����Ҫһ����Ϣѭ��������Ϣѭ���У����̲߳��ϵ��ظ�"��ȡ��Ϣ-������Ϣ"��һ����**

```python
loop = get_event_loop()
while True:
    event = loop.get_event()
    process_event(event)
```

��Ϣģ����ʵ����Ӧ��������Ӧ�ó������ˡ�һ��GUI��������߳̾͸���ͣ�ض�ȡ��Ϣ��������Ϣ�����еļ��̡�������Ϣ�������͵�GUI�������Ϣ�����У�Ȼ����GUI��������̴߳���

����GUI�̴߳�����̡�������Ϣ���ٶȷǳ��죬�����û��о������ӳ١�ĳЩʱ��GUI�߳���һ����Ϣ����Ĺ������������⵼��һ����Ϣ����ʱ���������ʱ���û���о�������GUI����ֹͣ��Ӧ�ˣ��ü��̡�����궼û�з�Ӧ���������˵������Ϣģ���У�����һ����Ϣ����ǳ�Ѹ�٣��������߳̽��޷���ʱ������Ϣ�����е�������Ϣ�����³�����ȥֹͣ��Ӧ��

> **��Ϣģ������ν��ͬ��IO����ȴ�IO������һ������أ�**
>
> ������IO����ʱ������ֻ���𷢳�IO���󣬲��ȴ�IO�����Ȼ��ֱ�ӽ���������Ϣ����������һ����Ϣ������̡���IO������ɺ󣬽��յ�һ��"IO���"����Ϣ���������Ϣʱ�Ϳ���ֱ�ӻ�ȡIO�����������"����IO����"���յ�"IO���"�����ʱ���ͬ��IOģ���£����߳�ֻ�ܹ��𣬵��첽IOģ���£����̲߳�û����Ϣ����������Ϣѭ���м�������������Ϣ�����������첽IOģ���£�һ���߳̾Ϳ���ͬʱ������IO���󣬲���û���л��̵߳Ĳ��������ڴ����IO�ܼ��͵�Ӧ�ó���ʹ���첽IO���������ϵͳ�Ķ�������������



# [�����Ͳ���](https://www.zhihu.com/question/33515481/answer/58849148)

��Է��Ե�һ�룬�绰���ˣ���һֱ���������Ժ��ȥ�ӣ����˵���㲻֧�ֲ���Ҳ��֧�ֲ��У�
��Է��Ե�һ�룬�绰���ˣ���ͣ���������˵绰�����������Է�����˵����֧�ֲ�����
��Է��Ե�һ�룬�绰���ˣ���һ�ߴ�绰һ�߳Է�����˵����֧�ֲ��У�

�����Ĺؼ������д������������������һ��Ҫͬʱ�����еĹؼ�������ͬʱ�����������������
����������ؼ��ĵ���ǣ��Ƿ��� **ͬʱ**


# [Э��](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432090171191d05dae6e129940518d1d6cf6eeaaa969000)
�����������������ж��ǲ㼶���ã�����A����B��B��ִ�й������ֵ�����C��Cִ����Ϸ��أ�Bִ����Ϸ��أ������Aִ����ϡ��ӳ��������ͨ��ջʵ�ֵģ�һ���߳̾���ִ��һ���ӳ���

�ӳ����������һ����ڣ�һ�η��أ�����˳������ȷ�ġ���Э�̵ĵ��ú��ӳ���ͬ��

**Э�̣��ֳ�΢�̣߳��˳̣�Ӣ����Coroutine��**

+ Э�̵����ã�����ִ�к���Aʱ��������ʱ�жϣ�ȥִ�к���B��Ȼ���жϼ���ִ�к���A�����������л���������һ���̲����Ǻ������ã�û�е�����䣩����һ�������̿�������̣߳�Ȼ��Э��ֻ��һ���߳�ִ�С�

  Э�̿���ȥҲ���ӳ��򣬵�ִ�й����У����ӳ����ڲ����жϣ�Ȼ��ת��ִ�б���ӳ������ʵ���ʱ���ٷ���������ִ�С�ע�⣬��һ���ӳ������жϣ�ȥִ�������ӳ��򣬲��Ǻ������ã��е�����CPU���жϡ�

+ Э�̵��ص�����һ���߳�ִ�ж��Э�̣��ǺͶ��̱߳ȣ�Э���к����ƣ�
  1. �������ƾ���Э�̼��ߵ�ִ��Ч�ʡ���Ϊ�ӳ����л������߳��л��������ɳ���������ƣ���ˣ�û���߳��л��Ŀ������Ͷ��̱߳ȣ��߳�����Խ�࣬Э�̵��������ƾ�Խ���ԡ�
  2. �ڶ������ƾ��ǲ���Ҫ���̵߳������ƣ�**��Ϊֻ��һ���̣߳�Ҳ������ͬʱд������ͻ**����Э���п��ƹ�����Դ��������ֻ��Ҫ�ж�״̬�ͺ��ˣ�����ִ��Ч�ʱȶ��̸߳ߺܶࡣ

+ Э�����ó���

  **Э���ʺϴ���IO�ܼ��ͳ����Ч�����⣬���Ǵ���CPU�ܼ��Ͳ������ĳ�������Ҫ��ַ���CPU�����ʿ��Խ�϶����+Э��**

+ Э��Ӧ��
  1. Python2
     + yield
     + [gevent](https://thief.one/2017/02/20/Python%E5%8D%8F%E7%A8%8B/)
  2. Python3
     - asynico + yield from��python3.4��
     - async + await��>= python3.5��
     - gevent

+ ��������generator����Э�̣�coroutine��������

  1. generator��������ֵ��һ���ǵ��������У�coroutine��ע��������ֵ�������ݵ�������
  2. coroutine���������������������generator��������������
  3. coroutineǿ��Эͬ���Ƴ�������generatorǿ������״̬�Ͳ�������
  4. ���Ƶ��ǣ����Ƕ��ǲ���return��ʵ���ظ����õĺ���/���󣬶��õ���**yield(�ж�/�ָ�)**�ķ�ʽ��ʵ�֡���yield�ں����з���ֵʱ�ᱣ�溯����״̬, ʹ��һ�ε��ú���ʱ�����һ�ε�״̬����ִ�У�

����yieldд�����������ߣ�����ʵ�ַ�ʽ���[github](https://github.com/liujunsheng0/study_py3/blob/master/coroutine/consumer_produce.py)

```python
# ������
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    # ����������
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)
```

ע�⵽`consumer`������һ��`generator`����һ��`consumer`����`produce`��

1. ���ȵ���`c.send(None)`������������
2. Ȼ��һ�������˶�����ͨ��`c.send(n)`�л���`consumer`ִ�У�
3. `consumer`ͨ��`yield`�õ���Ϣ��������ͨ��`yield`�ѽ�����أ�
4. `produce`�õ�`consumer`����Ľ��������������һ����Ϣ��
5. `produce`�����������ˣ�ͨ��`c.close()`�ر�`consumer`���������̽�����

����������������һ���߳�ִ�У�`produce`��`consumer`Э������������Գ�Ϊ"Э��"�������̵߳���ռʽ������



# ���ʽ���

+ event_loop �¼�ѭ��

  ������һ������ѭ��������Ա���Э�̶��󣨿�����Ϊ��ִ�к�����ע�ᵽ�¼�ѭ���ϡ��������¼�������ʱ�򣬵�����Ӧ��Э�̶���

+ coroutine Э��

  Э�̶���ָһ��ʹ��async�ؼ��ֶ���ĺ��������ĵ��ò�������ִ�к��������ǻ᷵��һ��Э�̶���Э�̶�����Ҫע�ᵽ�¼�ѭ�������¼�ѭ������

+ task  ����

  һ��Э�̶������һ��ԭ�����Թ���ĺ������������Ƕ�Э�̽�һ����װ�����а�������ĸ���״̬��

+ future

   ������ִ�л�û��ִ�е�����Ľ��������task��û�б��ʵ�����

+ asyncio

   ��Python 3.4�汾����ı�׼�⣬ֱ��**�����˶��첽IO��֧��**��

+ async/await

  python3.5 ���ڶ���Э�̵Ĺؼ��֣�async����һ��Э�̣�await���ڹ����������첽���ýӿڡ�



# [asyncio](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432090954004980bd351f2cd4cc18c9e6c06d855c498000)

`asyncio`��Python 3.4�汾����ı�׼�⣬ֱ��**�����˶��첽IO��֧��**��

`asyncio`�ı��ģ�;���һ����Ϣѭ������`asyncio`ģ���л�ȡ`EventLoop`�����ã�Ȼ�����Ҫִ�е�Э���ӵ�`EventLoop`��ִ�У���ʵ�����첽IO��

1. `asyncio`�ṩ�����Ƶ��첽IO֧�֣�
2. �첽������Ҫ��`coroutine`��ͨ��`yield from`��ɣ����ڲ���`yield from`������һ��coroutineʵ���첽������
3. ���`coroutine`���Է�װ��һ��TaskȻ�󲢷�ִ��

���[github](https://github.com/liujunsheng0/study_py3/blob/master/coroutine/coroutine_test.py)



# async/await

��`asyncio`�ṩ��`@asyncio.coroutine`���԰�һ��generator���Ϊcoroutine���ͣ�Ȼ����coroutine�ڲ���`yield from`������һ��coroutineʵ���첽������

Ϊ�˼򻯲����õر�ʶ�첽IO����Python 3.5��ʼ�������µ��﷨`async`��`await`��������coroutine�Ĵ��������׶���

��ע�⣬`async`��`await`�����coroutine�����﷨��Ҫʹ���µ��﷨��ֻ��Ҫ�������򵥵��滻��

1. ��`@asyncio.coroutine`�滻Ϊ`async`��
2. ��`yield from`�滻Ϊ`await`��

**async��await��ʹ��**

+ ʹ��async���Զ���Э�̶���

+ ʹ��await������Ժ�ʱ�Ĳ������й��𣬾������������yieldһ���������ó�����Ȩ��

  Э������await���¼�ѭ����������Э�̣�ִ�б��Э�̣�ֱ��������Э��Ҳ�������ִ����ϣ��ٽ�����һ��Э�̵�ִ�У�Э�̵�Ŀ��Ҳ����һЩ��ʱ�Ĳ����첽����

+ **await������ı�����һ��Awaitable���󣬻���ʵ������ӦЭ��Ķ��󣬲鿴Awaitable������Ĵ��룬������ֻҪһ����ʵ����`__await__`��������ôͨ�������������ʵ������һ��Awaitable������Coroutine��Ҳ�̳���Awaitable��**

ʹ��demo���[github](https://github.com/liujunsheng0/study_py3/blob/master/coroutine/asyc_test.py)

# gevent

gevent�ǵ������⣬ͨ��greenletʵ��Э�̡�

+ ����˼�� ����

  ��һ��greenlet����IO����ʱ������������磬���Զ��л���������greenlet���ȵ�IO������ɣ������ʵ���ʱ���л���������ִ�С�����IO�����ǳ���ʱ������ʹ�����ڵȴ�״̬������geventΪ�����Զ��л�Э�̣��ͱ�֤����greenlet�����У������ǵȴ�IO��

+ ʹ��demo���[github](https://github.com/liujunsheng0/study_py3/tree/master/coroutine/aio_http)

# ��ͬ��ʽʵ��hello world

�������[github](https://github.com/liujunsheng0/study_py3/blob/master/coroutine/coroutine_test.py)

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
from datetime import datetime
import time

import asyncio


def now():
    return datetime.now().strftime('%H:%M:%S')


def hello(num: int):
    print("Hello", num, 'now =', now(), 'serve thread id =', threading.currentThread().ident)
    time.sleep(num)
    print("Bye..", num, 'now =', now())


def thread_test():
    tasks = [threading.Thread(target=hello, args=[i, ]) for i in range(3)]
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()
    # result
    # Hello 0 now = 17:29:19 serve thread id = 13856
    # Hello 1 now = 17:29:19 serve thread id = 15188
    # Hello 2 now = 17:29:19 serve thread id = 15320
    # Bye.. 0 now = 17:29:19
    # Bye.. 1 now = 17:29:20
    # Bye.. 2 now = 17:29:21


def asyncio_test():
    # asyncio.coroutine ��һ��generator���Ϊcoroutine����
    @asyncio.coroutine
    def hello(num: int):
        print("Hello", num, 'now =', now(), 'serve thread id =', threading.currentThread().ident)
        # �첽����asyncio.sleep(num), �˴����Կ�����ʱ��IO����...
        # �ڴ��ڼ�, ���̲߳�δ�ȴ�, ����ȥִ��EventLoop����������ִ�е�coroutine, ���ʵ�ֲ���ִ��
        yield from asyncio.sleep(num)
        print("Bye..", num, 'now =', now())

    # ��ȡEventLoop
    loop = asyncio.get_event_loop()
    # Э��ִ��˳��, ò�ƺ�tasks�е�����˳���й�, �������Ƚ���ִ�ж��а�....
    tasks = [hello(i) for i in range(1, 4)]
    # ִ��coroutine
    task = asyncio.wait(tasks)
    loop.run_until_complete(task)
    loop.close()
    # ִ�н������
    # Hello 1 now = 17:43:02 serve thread id = 14808
    # Hello 2 now = 17:43:02 serve thread id = 14808
    # Hello 3 now = 17:43:02 serve thread id = 14808
    # Bye.. 1 now = 17:43:03
    # Bye.. 2 now = 17:43:04
    # Bye.. 3 now = 17:43:05
    # �ɴ�ӡ�ĵ�ǰ�߳�id���Կ���, ����coroutine����ͬһ���̲߳���ִ�е�.
    # �����asyncio.sleep(2)����������IO����, ����coroutine����һ���̲߳���ִ�е�, ������Ϊ��һ���̵߳Ĳ���...
    # ִ�й���˵��
    # 1. ���¼�ѭ����ʼ����ʱ, ������Task��Ѱ��coroutine��ִ�е���, ��Ϊ�¼�ѭ��ע����task(������Ϊ���¼�ѭ����ע��������Э��,
    #    ��[task1, task2, task3]), ���task��ʼִ��(����task1��ִ��)
    # 2. task1ִ����yield from asyncio.sleep(1)ʱ, task1����, ��Э��asyncio.sleep(1)���뵽�¼�ѭ������
    #    (Э��ִ�й�����, ������yield, yield from, awaitʱ, Э�̹���, ���浱ǰִ�л���, ִ������Э��)
    #    (����һ��yield �൱���ó�ִ��Ȩ, ִ������Э��)
    # 3. �¼�ѭ���ڶ����в��ҿɱ����ȵ�Э��, ִ������Э��,
    #    ִ��˳���������:
    #    task2, task2����, asyncio.sleep(2)���뵽�¼�ѭ������
    #    task3, task3����, asyncio.sleep(3)���뵽�¼�ѭ������
    #    asyncio.sleep(1), asyncio.sleep(1)����, �ȴ���ʱ����
    #    asyncio.sleep(1), asyncio.sleep(2)����, �ȴ���ʱ����
    #    asyncio.sleep(1), asyncio.sleep(3)����, �ȴ���ʱ����
    # 4. asyncio.sleep(1), ��ʱ����, ִ��task1, task1ִ�����, ִ������Э��
    #    asyncio.sleep(2), ��ʱ����, ִ��task2, task2ִ�����, ִ������Э��
    #    asyncio.sleep(3), ��ʱ����, ִ��task3, task3ִ�����, ִ������Э��


def async_test():
    async def hello(num: int):
        print("Hello", num, 'now =', now(), 'serve thread id =', threading.currentThread().ident)
        # �첽����asyncio.sleep(1)
        await asyncio.sleep(num)
        # ���ʹ��time.sleep ����˳��ִ��, ��������Э�̵���ʽִ��
        # time.sleep(2)
        print("Bye..", num, 'now =', now())

    # ��ȡEventLoop
    loop = asyncio.get_event_loop()
    tasks = [hello(i) for i in range(3)]
    # ִ��coroutine
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    # ���
    # Hello 0 now = 17:44:11 serve thread id = 14796
    # Hello 1 now = 17:44:11 serve thread id = 14796
    # Hello 2 now = 17:44:11 serve thread id = 14796
    # Bye.. 0 now = 17:44:11
    # Bye.. 1 now = 17:44:12
    # Bye.. 2 now = 17:44:13


def gevent_test():
    import gevent
    from gevent import monkey
    monkey.patch_all()
    tasks = [gevent.spawn(hello, i) for i in range(3)]
    gevent.joinall(tasks)
    # �������
    # Hello 0 now = 17:44:47 serve thread id = 46817808
    # Hello 1 now = 17:44:47 serve thread id = 46818112
    # Hello 2 now = 17:44:47 serve thread id = 46818264
    # Bye.. 0 now = 17:44:47
    # Bye.. 2 now = 17:44:48
    # Bye.. 1 now = 17:44:49


if __name__ == '__main__':
    # thread_test()
    # asyncio_test()
    # async_test()
    gevent_test()
    # �ӽ������, ���߳���Э�̵�Ч��һ��, ���ﵽ��IO����ʱ�л��Ĺ���.
    # ��ͬ����, ���߳��л������߳�(�̼߳��л�), Э���л�����������(�������Ϊִ�еĺ���).
    # ���л��̵߳Ŀ�����Ҫ�����л������ĵĿ���, ��˵��߳�Խ��, Э�̵�Ч�ʾ�Խ�ȶ��̵߳ĸߡ�

```



# ѧϰ����

[��ѩ��---�첽IO](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143208573480558080fa77514407cb23834c78c6c7309000)

[Э��](https://thief.one/2017/02/20/Python%E5%8D%8F%E7%A8%8B/)

[Э�̵�ѧϰ���о�](https://thief.one/2018/06/21/1/)

[�첽IO](https://www.jianshu.com/p/b5e347b3a17c)

[����-ͬ�������̣߳�����̣�Э��](https://zhuanlan.zhihu.com/p/25228075)

https://zhuanlan.zhihu.com/p/27258289