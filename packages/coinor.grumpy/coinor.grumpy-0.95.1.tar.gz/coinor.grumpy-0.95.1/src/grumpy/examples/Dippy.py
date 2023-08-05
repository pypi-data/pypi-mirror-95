from __future__ import print_function
DEBUGGING = False

import sys

#sys.path.append("C:\\COIN\\GIMPy\\GrUMPy\\trunk")
#sys.path.append("C:\\COIN\\GIMPy\\trunk")

from pulp import *
from coinor.dippy import DipProblem, Solve

prob = DipProblem("Dippy Example", display_mode = 'matplotlib', 
                  display_interval = 1)

x1 = LpVariable("x_1", 0, None, LpInteger)
x2 = LpVariable("x_2", 0, cat=LpInteger)

prob += -x1 - x2, "min"

prob += -2 * x1 +  2 * x2 >= 1
prob += -8 * x1 + 10 * x2 <= 13

Solve(prob, {
    'CutCGL': 0,
})

for var in prob.variables():
    print(var.name, "=", var.value())

prob.Tree.display()
