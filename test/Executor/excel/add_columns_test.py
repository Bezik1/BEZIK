import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from structure.Executor import Executor

executor = Executor()
executor.execute("excel add zbiór [ typ, gracze ] [ strzelanka, rpg, symulator, skradanka ] [ 1000, 20000, 100, 400 ]".split(" "))