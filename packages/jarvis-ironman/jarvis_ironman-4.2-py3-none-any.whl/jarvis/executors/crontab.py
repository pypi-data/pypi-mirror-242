import os
import subprocess

from jarvis.modules.logger import multiprocessing_logger

LOG_FILE = os.path.join('logs', 'cron_%d-%m-%Y.log')  # Used by api functions that run on cron schedule


def executor(statement: str, log_file: str = None) -> None:
    """Executes a cron statement.

    Args:
        statement: Cron statement to be executed.
        log_file: Log file for crontab execution logs.

    Warnings:
        - Executions done by crontab executor are not stopped when Jarvis is stopped.
        - On the bright side, almost all executions made by Jarvis are short-lived.
    """
    if not log_file:
        log_file = multiprocessing_logger(filename=LOG_FILE)
    with open(log_file, 'a') as file:
        file.write('\n')
        try:
            subprocess.call(statement, shell=True, stdout=file, stderr=file)
        except Exception as error:
            if isinstance(error, subprocess.CalledProcessError):
                result = error.output.decode(encoding='UTF-8').strip()
                file.write(f"[{error.returncode}]: {result}\n")
            else:
                file.write(f"{error}\n")
