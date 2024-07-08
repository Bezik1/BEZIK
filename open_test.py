import sys
import os

from structure.BEZIK import BEZIK

model = BEZIK(True)

test = "Otwórz excel"
command_str = model(test)
print(command_str)