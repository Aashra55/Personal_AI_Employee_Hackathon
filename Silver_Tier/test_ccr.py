import subprocess
import os
try:
    print("Running ccr code...")
    result = subprocess.run(["ccr.cmd", "code", "Write a Hello World"], capture_output=True, text=True, shell=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("RETURNCODE:", result.returncode)
except Exception as e:
    print("EXCEPTION:", e)
