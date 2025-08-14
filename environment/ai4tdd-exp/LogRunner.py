"""
LogRunner coordinates the execution of a Python file and logs its output and error streams to uniquely indexed text files.

Key features include:
- Automatically managing log file naming and indexing.
- Saving output and error logs in a specified folder for traceability and debugging.
"""


import os
from LogCollector import LogCollector

class LogRunner():

    def __init__(self, python_version, logs_folder, file):
        self.collector = LogCollector(
            python_version=python_version,
            logs_folder=logs_folder,
            file=file
        )

    def writeFile(self, data, index, type, path_prefix):
        f = open("{}/{}_{}.txt".format(path_prefix, index, type), "a")
        f.write(data)
        f.close()

    def run(self):
        if os.path.isdir(self.collector.logs_folder) != True:
            os.mkdir(self.collector.logs_folder)

        output, error = self.collector.execute_python_file()

        index = int(len(os.listdir(self.collector.logs_folder))/2) + 1

        self.writeFile(output, index, "output", self.collector.logs_folder)
        self.writeFile(error, index, "error", self.collector.logs_folder)

        print(output)
        print("...")
        print(error)

