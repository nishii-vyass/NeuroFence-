import subprocess
import sys


def start_sandbox_process(script_path):

    process = subprocess.Popen(
        [
            sys.executable,
            script_path
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return process


def stop_sandbox_process(process):

    if process is not None:

        process.terminate()

        try:
            process.wait(timeout=5)

        except subprocess.TimeoutExpired:

            process.kill()