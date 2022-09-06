# -*- coding: utf-8 -*-
import subprocess
import os
import signal

def check(name):
    try:
        return int(subprocess.check_output(["pidof", name]))
    except Exception:
        return 0

def stop_proc():
    number = check("client_by_openconnect")
    if number != 0:
        os.kill(number, signal.SIGINT)
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    stop_proc()
