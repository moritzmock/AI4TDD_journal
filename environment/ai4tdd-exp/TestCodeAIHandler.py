"""
TestCodeAIHandler extends LogCollector and AIHandler to automate the generation of unit tests and production code using AI in a Test-Driven Development workflow.

Key features include:
- Integrating with OpenAI to generate unit tests based on natural language prompts and existing code.
- Tracking and managing sequential test cases with file naming and indexing.
- Persisting AI context, responses, and logs for traceability.
"""

import subprocess
import sys
from LogCollector import LogCollector
from AIHandler import AIHandler
from utils import how_many_to_skip
from utils import reshuffle_code
from utils import extract_classes_from_file

sys.path.append("..")

TEST_PASSED = "TEST_PASSED"


class TestCodeAIHandler(LogCollector, AIHandler):

    def __init__(self, file_path, prompt, print_context, **kwargs):
        super().__init__(**kwargs)
        self.file = file_path
        self.incorrect_test_cases_created = 0
        self.prompt = prompt
        self.print_context = print_context


    def get_last_test_case_number(self):
        return how_many_to_skip("{}/test_case.py".format(self.logs_folder), multiplier=1)

    def get_last_test_case_path(self):
        number = self.get_last_test_case_number() - self.incorrect_test_cases_created
        return "test_case_" + str(number) + ".py"

    def get_base_filename_for_context(self):
        number = self.get_last_test_case_number()
        base_filename = "test_case_" + str(number + 1)
        return base_filename

    def get_filename_for_context(self):
        base_filename = self.get_base_filename_for_context()
        return base_filename + "_context_tester.txt"

    def get_previous_code(self):
        return self.readFromFile(self.file)

    def get_next_message(self):

        number = self.get_last_test_case_number()
        if self.file is None:
            number = number - self.incorrect_test_cases_created
            self.file = self.logs_folder + '/' + self.get_last_test_case_path() if number > 0 else None


        previous_code = self.get_previous_code()
        previous_code = "" if previous_code == "" else "Given the below existent code:\n" + previous_code

        return {"role": "user",
                "content": previous_code + "\nGiven the following textual description of the test case, provide a minimal test case:\n"+
                           ("Use " if previous_code == "" else "Keep the existing tests and add one by using ") +
                           "the Assertion First pattern in TDD to develop the first barely minimal test and production code for the feature: " + self.prompt + " Do not provide a solution for other input classes. \n\nAssume that the class will be written in the same file!"}


    def clean_code(self):
        code = self.messages_received_parsed_code[-1].split("\n")

        result = []
        for idx in range(len(code)):
            line = code[idx]
            if not line.startswith("from"):
                result.append(line)

        return "\n".join(result)

    def create_test_code(self):
        context = self.create_context()
        next_message = self.get_next_message()
        context.append(next_message)

        path = self.logs_folder + "/" + self.get_filename_for_context()

        self.save_context(context, path)

        if self.print_context:
            print("------ CONTEXT START -------")
            print(context)
            print("------ CONTEXT END -------")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=context
        )

        self.messages_send.append(next_message)
        message = response.choices[0].message.content
        self.messages_received.append(message)
        self.messages_received_parsed_code.append(self._parse_message(message))

        path = self.logs_folder + "/" + self.get_base_filename_for_context() + "_response_tester.txt"
        self.save2file(message, path)

        code = self.clean_code()
        old_code = extract_classes_from_file(self.file)
        path = self.logs_folder + "/" + self.get_base_filename_for_context() + ".py"
        reshuffled_code = ("" if len(old_code) == 0 else old_code[0]) + reshuffle_code(code, self.logs_folder + "/" + self.get_last_test_case_path(), keep_production_code=False)

        self.save2file(reshuffled_code, path)
        self.save2file(reshuffled_code, self.file)

        print("Generated test case is stored in file: " + path)
        print(self.file + ", was updated with the next test code.")

    def generate_production_code(self):

        result_sub_process = subprocess.run(
            ["python", "CollaborativeTDDRunner.py", "--file", self.file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        print("Return value from generating code!")
        print("out")
        print(result_sub_process.stdout)
        print("err")
        print(result_sub_process.stderr)