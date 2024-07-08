import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from structure.BEZIK import BEZIK

model = BEZIK

test = "Sprawdź, gdzie na stronie o Ignacym Janie Paderewskim znajduje się napis 'matki'"
model(test)