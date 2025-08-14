"""
LogCollector is a utility class designed to execute Python files and capture their standard output and error logs.

Key features include:
- Running Python scripts using a specified Python version.
- Automatically creating a folder to store logs if it doesn't exist.
- Providing a simple interface to collect and return execution logs.
"""


import subprocess
import os

class LogCollector():

    def __init__(self, python_version = None, logs_folder = None, file = None, **kwargs):
        super().__init__(**kwargs)
        self.python_version = python_version
        self.logs_folder = logs_folder
        self.file = file
        self.generate_logs_folder()

    def generate_logs_folder(self):
        if not os.path.isdir(self.logs_folder):
            os.makedirs(self.logs_folder, exist_ok=True)

    def execute_python_file(self, file_path = None):
        """
        Executes a python file and collects its logs.
        :param file_path: path of the python file
        :return: tuple(stdout, stderr)
        """
        if file_path is not None: self.file = file_path
        assert self.file is not None; "Test file was not passed!"

        process = subprocess.Popen(
            "{} {}".format(self.python_version, self.file),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        return process.communicate()
