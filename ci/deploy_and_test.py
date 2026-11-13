import os, subprocess

ws, ds = os.environ["TEST_WS"], os.environ["TEST_DS"]
steps = [
    ["python", "ci/deploy.py", "--env", "TEST"],
    ["python", "ci/refresh.py", "--ws", ws, "--ds", ds],
    ["python", "ci/run_tests.py", "--ws", ws, "--ds", ds],
]
for cmd in steps:
    print(">", " ".join(cmd))
    subprocess.check_call(cmd)          # stops at the first failing step
