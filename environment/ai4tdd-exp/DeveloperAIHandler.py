"""
This module defines DeveloperAIHandler, a class that automates AI-assisted debugging and code refinement
based on test failures within a TDD workflow.

Key functionality:
- Extends LogCollector and AIHandler to log test runs, maintain context, and interact with AI.
- Generates and merges AI-generated code into test files while preserving existing structure and imports.
- Automates execution and validation of new code using Python's subprocess module.
- Tracks test execution results and error traces for iterative refinement.
"""

import sys
sys.path.append("..")
from utils import reshuffle_code
from LogCollector import LogCollector
from AIHandler import AIHandler

TEST_PASSED = "TEST_PASSED"
TEST_FAILED = "TEST_FAILED"
TEST_PASSED_WITHOUT_AI = "TEST_PASSED_WITHOUT_AI"


def get_next_filename(filename, idx):
    return filename + "_" + str(idx)


class DeveloperAIHandler(LogCollector, AIHandler):
    def __init__(self, full_context, print_context, file, generic_prompt, **kwargs):
        super().__init__(**kwargs)
        self.current_test_file = file
        self.full_context = full_context
        self.print_context = print_context
        self.generic_prompt = generic_prompt

    def get_path(self, filename, idx, filetype="py"):
        return "{}.{}".format(self.logs_folder+"/"+filename.replace(".py", "") + "_" + str(idx), filetype)

    def get_next_message(self, idx):
        trace = self.get_traces_of_last_run()
        if trace == TEST_PASSED:
            return TEST_PASSED
        test_and_trace = trace + "\n" + self.get_tests()

        return test_and_trace + "\n\n" + self.generic_prompt

    def send_message(self, idx):
        context = self.create_context()
        next_message = self.get_next_message(idx)
        if next_message == TEST_PASSED:
            return TEST_PASSED_WITHOUT_AI
        context.append({"role": "user", "content": next_message})

        if not self.full_context:
            context = [
                   {"role": "system", "content": self.role},
                   {"role": "user", "content": next_message}
               ]

        filename = self.current_test_file

        path = self.get_path(filename, idx, "txt").replace(".txt", "_context_developer.txt")

        self.save_context(context, path)

        if self.print_context:
            print("------ CONTEXT START -------")
            print(context)
            print("------ CONTEXT END -------")

        response = self.client.chat.completions.create(
           model="gpt-3.5-turbo-16k",
           messages=context
        )

        self.messages_send.append(next_message)
        message = response.choices[0].message.content

        path = self.get_path(self.current_test_file, idx, "txt").replace(".txt", "_response_developer.txt")

        self.save2file(message, path)

        self.messages_received.append(message)
        self.messages_received_parsed_code.append(self._parse_message(message))

    def execute_new_test(self, idx):
        self.merge_files(idx)
        self.execute_tests(idx)
        if self.errors[-1] == TEST_PASSED:
            self.merge_files(idx, update_original_file=True)
            return TEST_PASSED
        return TEST_FAILED

    def get_tests_without_previous_code(self):
        old_code = self.get_tests().split("\n")
        for idx in range(len(old_code)):
            line = old_code[idx]
            if line.startswith("import unittest"):
                return "\n".join(old_code[idx:])

        return "\n".join(old_code)

    def get_code_without_test_case(self):
        code = self.messages_received_parsed_code[-1].split("\n")

        for idx in range(len(code)):
            line = code[idx]
            if line.startswith("import unittest"):
                return "\n".join(code[:idx])
        return "\n".join(code)

    def merge_files(self, idx, update_original_file=False):
        code = self.get_code_without_test_case()
        test_cases = self.get_tests_without_previous_code()
        complete_code = code + "\n\n" + test_cases

        if update_original_file:
            self.save2file(reshuffle_code(complete_code), self.current_test_file)

        if not update_original_file:
            path = self.get_path(self.current_test_file, idx)
            self.save2file(reshuffle_code(complete_code), path)


    def execute_tests(self, idx):
        path = self.get_path(self.current_test_file, idx)
        path = path if idx is not None else self.current_test_file
        print(path)
        result_sub_process = self.execute_python_file(file_path=path)
        print(result_sub_process[1])
        if "OK" not in result_sub_process[1].split("\n")[-2]:
            self.errors.append([result_sub_process[1]])
        else:
            self.errors.append(TEST_PASSED)

    def get_traces_of_last_run(self):
        if self.errors[-1] == TEST_PASSED:
            return TEST_PASSED
        return "\n".join(self.errors[-1])

    def get_tests(self):
        return self.readFromFile(self.current_test_file)