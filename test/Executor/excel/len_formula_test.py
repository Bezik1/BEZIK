import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from structure.Executor import Executor

executor = Executor()
executor.execute("excel columns [ id, name ] [ 1, 2, 3 ] [ Gabriela, Hubert, Iga ]".split(" "))