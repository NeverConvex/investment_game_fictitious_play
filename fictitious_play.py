import numpy as np
import random

REWARD = 20.0
ENDOW = 6

def payoff(pnum, strat0, strat1):
    if pnum == 0:
        if strat0 > strat1:
            return REWARD - strat0
        return -strat0
    elif pnum == 1:
        if strat1 > strat0:
            return REWARD - strat1
        return -strat1

def ev(pnum, my_strat, other_player_history):
    probs = other_player_history / np.sum(other_player_history)
    if pnum == 0:
        expected_val = np.sum([p * payoff(pnum, my_strat, i) for i, p in enumerate(probs)])
    else:
        expected_val = np.sum([p * payoff(pnum, i, my_strat) for i, p in enumerate(probs)])
    return expected_val

def br(pnum, other_player_history):
    evs = np.array([ev(pnum, i, other_player_history) for i in range(ENDOW)])
    br_inds = np.array([i for i in range(len(evs))])[evs == np.max(evs)]
    return random.choice(br_inds)

def fictitious_play(iterations, history):
    for i in range(iterations):
        br0, br1 = br(0, history[1]), br(1, history[0])
        history[0][br0] += 1
        history[1][br1] += 1
    return history

def main():
    iterations = 10000
    initial_history = [np.array([1 for _ in range(ENDOW)]), np.array([1 for _ in range(ENDOW)])]
    new_history = fictitious_play(iterations, initial_history)
    for i in range(2):
        player_hist = new_history[i]/np.sum(new_history[i])
        print(f"For p{i}, fictitious play returned: {np.around(player_hist, 2)}")

if __name__ == "__main__":
    main()
