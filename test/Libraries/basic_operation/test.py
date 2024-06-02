import subprocess

file = open("test_file.py", "w")
file.write('while True:\n   print("Test")')
file.close()

subprocess.call(["python", "test_file.py"],creationflags=subprocess.CREATE_NEW_CONSOLE)