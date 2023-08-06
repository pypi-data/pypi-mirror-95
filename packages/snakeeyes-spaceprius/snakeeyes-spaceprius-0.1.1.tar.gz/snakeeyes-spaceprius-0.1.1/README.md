# SnakeEyes [![Build Status](https://www.travis-ci.com/SpacePrius/SnakeEyes.svg?branch=main)](https://www.travis-ci.com/SpacePrius/SnakeEyes) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/3c94f19f5d5a495eaaabdde028fa0043)](https://www.codacy.com/gh/SpacePrius/SnakeEyes/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SpacePrius/SnakeEyes&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/3c94f19f5d5a495eaaabdde028fa0043)](https://www.codacy.com/gh/SpacePrius/SnakeEyes/dashboard?utm_source=github.com&utm_medium=referral&utm_content=SpacePrius/SnakeEyes&utm_campaign=Badge_Coverage)

SnakeEyes is a python dice library designed to be easily extensible.
***VERY MUCH WIP***

## Input
Input with snakeyes is done in form of
```
[quantity]d[sides][diceoperators][math]
```

Examples of valid input are:
```
1d20
4d6
1d20+5
(1d20+27)*16
(20+5)/12
```

## Operators
"x" - Exploding dice, used in the form:
```
[diceroll]x[threshhold]
```

Any roll in the result set, meeting or exceeding the threshold, will trigger another roll to be made. Returns the set of rolls, with the addition of any exploded rolls.

">" - Inequality, used in the form:
```
[diceroll]>[threshold]
```
Any roll which exceeds the threshold will count as a success, returns a tuple with the rolls value, combined with a bool indicating whether it exceeded the threshold.