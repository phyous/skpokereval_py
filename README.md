# skpokereval_py

A fast and lightweight 32-bit Texas Hold'em 7-card hand evaluator written in C++ & wrapped in python.
Based on:
* https://github.com/kennethshackleton/SKPokerEval
* https://github.com/gsugar87/SKPokerPython

## Installation
1. Run `python3 setup.py install`. This will generate an .so file which can be dynamically loaded.
2. For dynamic linked libraries to be loaded, the paths searched must be in LD_LIBRARY_PATH. Ensure this is defined; ex: export LD_LIBRARY_PATH=/usr/local/lib/python3.9/site-packages

## Usage
`getRank` function takes two lists: 
1. ourCards (2 cards in our hand)
2. boardCards (3-5 cards on the table)

It returns the rank of our best possible hand (higher is better).
Notes:
* A card is an int [0-51]
* Card values are as follows 0=As, 1=Ah, 2=Ad, 3=Ac, 4=Ks, 5=Kh, 6=Kd, ..., 50=2d, 51=2c. (s = spade, h=heart, d = diamond, c = club).

```
>>> import handEvaluatorCPP
>>> handEvaluatorCPP.getRank([1,2], [3,4,5,6,7])
7440
```

## How does it work?

We exploit a key-scheme that gives us just enough uniqueness to correctly identify the integral rank of any 7-card hand, where the greater this rank is the better the hand we hold and two hands of the same rank always draw. We require a memory footprint of just less than 135kB and typically six additions to rank a hand.

To start with we computed by brute force the first thirteen non-negative integers such that the formal sum of exactly seven with each taken at most four times is unique among all such sums: 0, 1, 5, 22, 98, 453, 2031, 8698, 22854, 83661, 262349, 636345 and 1479181. A valid sum might be 0+0+1+1+1+1+5 = 9 or 0+98+98+453+98+98+1 = 846, but invalid sum expressions include 0+262349+0+0+0+1 (too few summands), 1+1+5+22+98+453+2031+8698 (too many summands), 0+1+5+22+98+453+2031+8698 (again too many summands, although 1+5+22+98+453+2031+8698 is a legitimate expression) and 1+1+1+1+1+98+98 (too many 1's). We assign these integers as the card face values and add these together to generate a key for any non-flush 7-card hand. The largest non-flush key we see is 7825759, corresponding to any of the four quad-of-aces-full-of-kings.

Similarly, we assign the integer values 0, 1, 8 and 57 for spade, heart, diamond and club respectively. Any sum of exactly seven values taken from {0, 1, 8, 57} is unique among all such sums. We add up the suits of a 7-card hand to produce a "flush check" key and use this to look up the flush suit value if any. The largest flush key we see is 7999, corresponding to any of the four 7-card straight flushes with ace high, and the largest suit key is 399.

The extraordinarily lucky aspect of this is that the maximum non-flush key we have, 7825759, is a 23-bit integer (note 2^23 = 8388608) and the largest suit key we find, 57*7 = 399, is a 9-bit integer (note 2^9 = 512). If we bit-shift each card's flush check and add to this its non-flush face value to make a card key in advance, when we aggregate the resulting card keys over a given 7-card hand we generate a 23+9 = 32-bit integer key for the whole hand. This integer key can only just be accommodated by a standard 32-bit `int` type and yet still carries enough information to decide if we're looking at a flush and if not to then look up the rank of the hand.
