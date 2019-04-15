#include <iostream>
#include <fst/fstlib.h>

using namespace fst;
using namespace std;
using StateId = StdArc::StateId;
using Weight = StdArc::Weight;
using Label = StdArc::Label;

// A vector FST is a general mutable(易变的) FST
static StdVectorFst fst_;

void init() {
    /*
     *    (1, 1, 0.1)
     *    ---------->      (2, 2, 1.2)    (3, 3, 2.1)
     * 0               1   ----------> 2  ----------> 3
     *    (2, 2, 0.2)
     *    ---------->
     * state, state_id = 0 weight = 0
     * arc start
     * arc, ilabel = 1, olabel = 1, nextstate = 1, weight = 0.1
     * arc, ilabel = 2, olabel = 2, nextstate = 1, weight = 0.2
     * arc endl
     *
     * state, state_id = 1 weight = 1
     * arc start
     * arc, ilabel = 2, olabel = 2, nextstate = 2, weight = 1.2
     * arc endl
     *
     * state, state_id = 2 weight = 2
     * arc start
     * arc, ilabel = 3, olabel = 3, nextstate = 3, weight = 2.1
     * arc endl
     *
     * state, state_id = 3 weight = 3
     * arc start
     * arc endl
     *
     */
    // Adds state 0 to the initially empty FST and make it the start state.
    fst_.AddState();   // 1st state will be state 0 (returned by AddState)
    fst_.SetStart(0);  // arg is state ID
    fst_.SetFinal(0, 0);  // 1st arg is state ID, 2nd arg weight

    // Adds two arcs exiting state 0.
    // Arc constructor args: ilabel, olabel, weight, dest state ID.
    fst_.AddArc(0, StdArc(1, 1, 0.1, 1));  // 1st arg is src state ID
    fst_.AddArc(0, StdArc(2, 2, 0.2, 1));

    // Adds state 1 and its arc.
    fst_.AddState();
    fst_.SetFinal(1, 1);
    fst_.AddArc(1, StdArc(2, 2, 1.2, 2));

    // Adds state 2 and its arc.
    fst_.AddState();
    fst_.SetFinal(2, 2);
    fst_.AddArc(2, StdArc(3, 3, 2.1, 3));

    // Adds state 3 and set its final weight.
    fst_.AddState();
    fst_.SetFinal(3, 3);

    // We can save this FST to a file with:
    fst_.Write("binary.fst");
}

void display_arc(const StdArc &arc) {
    cout<<"arc, ilabel = "<<arc.ilabel<<", olabel = "<<arc.olabel<<", nextstate = "<<arc.nextstate<<", weight = "<<arc.weight.Value()<<endl;
}

void iter_state_and_arc() {
    // Gets the initial state; if == kNoState => empty FST.
    StateId initial_state = fst_.Start();

    for (StateIterator<StdFst> iters(fst_); !iters.Done(); iters.Next()) {
        // Get state i's final weight; if == Weight::Zero() => non-final.
        StdArc::StateId state_id = iters.Value();

        Weight weight = fst_.Final(state_id);
        cout<<"state, state_id = "<<state_id<<" weight = "<<weight<<endl;

        cout<<"arc start"<<endl;
        // Iterates over state i's arcs.
        for (ArcIterator<StdFst> aiter(fst_, state_id); !aiter.Done(); aiter.Next()) {
            display_arc(aiter.Value());
        }
        cout<<"arc endl"<<endl<<endl;
    }
}

void match() {
    // Iterates over state i's arcs that have input label l
    // (FST must support this - in the simplest cases,  true when the input labels are sorted).
    Matcher<StdFst> matcher(fst_, MATCH_INPUT);
    matcher.SetState(0);
    // Find ilabel, not stateId
    if (matcher.Find(1)) {
        for (; !matcher.Done(); matcher.Next()) {
            display_arc(matcher.Value());
        }
    }
}

int main() {
    init();
    iter_state_and_arc();
    match();
    return 0;
}