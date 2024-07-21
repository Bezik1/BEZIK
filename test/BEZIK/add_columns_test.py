import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from structure.BEZIK import BEZIK

model = BEZIK

test = "dodaj kolumny gra i cena do pliku dane o wartościach fnaf cs simsy oraz 0 0 100"
model(test)