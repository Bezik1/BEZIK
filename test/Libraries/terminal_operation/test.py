import subprocess

subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "echo 'To jest testowa instrukcja'; exec bash"])