# you can roll your ball as much as you can but the game rule is:
# Each pin has a number.
# You can pass the pin or hit one or two pins at a time.
# if you pass the pin, we simply ignore the number of the pin, so 0 point is possible. 
# if you hit a single pin, you can get the point that pin describes
# if you hit two pit at a same time, you can get the multiplication of the two pins.

from random import randint
from utils import Timer

N = 10 # // N >= 1 
PINS = [randint(-10, 10) for _ in range(N)]
print(PINS)
memoization = N * [-1] # // initial maximum, of course 0, don't need to hit, but to check if memoized, we put minus value that never occurs. 


def bowling(N):
    if memoization[N-1] > -1:
        return memoization[N-1]
    elif N>2:
        candidate_1 = bowling(N-1)
        candidate_2 = bowling(N-1) + PINS[N-1]
        candidate_3 = bowling(N-2) + PINS[N-2] * PINS[N-1]
        memoization[N-1] = max(candidate_1, candidate_2, candidate_3)
        return memoization[N-1]
    elif N == 2:
        candidate_1 = bowling(N-1)
        candidate_2 = bowling(N-1) + PINS[N-1]
        candidate_3 = PINS[1] * PINS[0]
        memoization[N-1] = max(candidate_1, candidate_2, candidate_3)
        return memoization[N-1]

    elif N == 1:
        memoization[N-1] = max(0, PINS[0])
        return memoization[N-1]

def max_bowling_score(pins):
    # dp[i] only depends on dp[i-1] and dp[i-2],
    # so we can roll variables forward.
    N = len(pins)
    if N == 0:
        return 0
    prev2 = 0
    prev1 = max(0, pins[0])

    for i in range(1, N):
        skip = prev1
        hit1 = prev1 + pins[i]
        hit2 = prev2 + pins[i-1] * pins[i]
        
        current = max(skip, hit1, hit2)
        
        prev2, prev1 = prev1, current
    
    return prev1

with Timer() as timer:
    print(bowling(10))
with Timer() as timer:
    print(max_bowling_score(PINS))