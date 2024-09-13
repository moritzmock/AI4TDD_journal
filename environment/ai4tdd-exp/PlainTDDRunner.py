import subprocess
import os

class PlainTDDRunner():

    def __init__(self, python_version, folder_logs, test_file):
        self.python_version = python_version
        self.folder_logs = folder_logs
        self.test_file = test_file

    def executeTests(self):
        process = subprocess.Popen(
            "{} {}".format(self.python_version, self.test_file),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        return process.communicate()


    def writeFile(self, data, index, type, path_prefix):
        f = open("{}/{}_{}.txt".format(path_prefix, index, type), "a")
        f.write(data)
        f.close()

    def run(self):
        if os.path.isdir(self.folder_logs) != True:
            os.mkdir(self.folder_logs)

        output, error = self.executeTests()

        index = int(len(os.listdir(self.folder_logs))/2) + 1

        self.writeFile(output, index, "output", self.folder_logs)
        self.writeFile(error, index, "error", self.folder_logs)

        print(output)
        print("...")
        print(error)




    