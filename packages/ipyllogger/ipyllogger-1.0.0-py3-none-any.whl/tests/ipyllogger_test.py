import os
import sys
from random import randint

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from ipyllogger import Logger
from ipyllogger import level

error_logs = []
Warning_logs = []

logger = Logger()

for i in range(10):
    if randint(0, 1) == 0:
        log_data = logger.log(f"Message - {i}", level.ERROR)
        error_logs.append(log_data)
    else:
        log_data = logger.log(f"Message - {i}", level.WARNING)
        Warning_logs.append(log_data)


for logentry in logger.get_logs(level.ERROR):
    if logentry not in error_logs:
        raise Exception(
            "Test failed. %s not in %s logs" %
            (logentry, level.ERROR)
        )

for logentry in logger.get_logs(level.WARNING):
    if logentry not in Warning_logs:
        raise Exception(
            "Test failed. %s not in %s logs" %
            (logentry, level.WARNING)
        )
    
os.remove(f"{root_path}/logs/error.log")
os.remove(f"{root_path}/logs/warning.log")
os.rmdir(f"{root_path}/logs")
print("ALL TESTS PASSED")
