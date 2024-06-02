import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from structure.Executor import Executor

executor = Executor()
executor.execute("excel [ name, len ] [ lew, elf, delf ] [ =LEN(A2), =LEN(A3), =LEN(A4) ]".split(" "))