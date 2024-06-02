import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from structure.Executor import Executor

executor = Executor()
executor.execute("webdriver search https://paderewski-konkurs-hnol.vercel.app Tournée".split(" "))