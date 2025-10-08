"""
This script defines and runs a CollaborativeTDDRunner, which facilitates AI-assisted Test-Driven Development
by iteratively improving production code until tests pass.

Key functionality:
- Uses DeveloperAIHandler to collect failing test traces, prompt the AI, and integrate AI-generated solutions.
- Executes tests, assesses results, and refines the code over a series of AI interaction cycles.
- Logs test execution and AI responses for traceability and reproducibility.
"""


import argparse
import os
from DeveloperAIHandler import DeveloperAIHandler, TEST_PASSED, TEST_FAILED, TEST_PASSED_WITHOUT_AI
from utils import how_many_to_skip
from utils import str2bool

class CollaborativeTDDRunner():

    def __init__(self, key, full_context, print_context, print_message, max_number_repetitions, file, generic_prompt, logs_folder, python_version):
        self.handler = DeveloperAIHandler(
            key=key,
            role="You are part of a Test Driven Development team. Your role is the development of code such that the provided code is fulfilled.",
            full_context=full_context,
            print_context=print_context,
            print_message=print_message,
            file_path=file,
            generic_prompt=generic_prompt,
            logs_folder=logs_folder,
            python_version=python_version
        )
        self.max_number_repetitions = max_number_repetitions
        self.skip = how_many_to_skip(file, log_path=logs_folder, multiplier=1) + 1

    def run(self):
        self.handler.execute_tests(None)
        counter = 0
        while counter < (self.max_number_repetitions):
            counter += 1
            result = self.handler.send_message("{}_{}".format(self.skip, counter))
            if result == TEST_PASSED_WITHOUT_AI:
                print("The test case is already fulfilled, the code was not modified by AI.")
                counter = self.max_number_repetitions
            else:
                result = self.handler.execute_new_test("{}_{}".format(self.skip, counter))

                if result == TEST_PASSED:
                    print("Test case passed! You can inspect the updated code now!")
                    counter = self.max_number_repetitions + self.skip
                if result == TEST_FAILED:
                    print("Test failed! Resending it to AI...")


def params():
    parser = argparse.ArgumentParser(description='Description of your program.')

    # Add arguments
    parser.add_argument('--full_context', type=str2bool, help='sending the full context to OpenAI.', default=False)
    parser.add_argument('--print_context', type=str2bool, help='Printing the context before the it is send.', default=False)
    parser.add_argument('--print_message', type=str2bool, help='Printing the message received from OpenAI.', default=False)
    parser.add_argument('--max_number_repetitions', type=int, help='Maximum number of chances given to OpenAI for solving a test case.', default=5)
    parser.add_argument('--file', type=str, help='Path to the file for the test case.', required=True)
    parser.add_argument('--generic_prompt', type=str, help='Prompt which is passed to the AI together with the error trace, production code, and test code.', default="I have the above test, what would be a minimal code so that the test no longer fails. Built-in functions are not allowed.")
    parser.add_argument('--logs-folder', type=str, help='Folder to which all logs are saved.', default='./logs')
    parser.add_argument('--python-version', type=str, help='Local command to executed python, e.g., python or python3', default='python')

    return parser.parse_args()


if __name__ == '__main__':
    args = params()

    openAI_key = os.getenv('OPEN_AI_KEY')

    runner = CollaborativeTDDRunner(
        openAI_key,
        args.full_context,
        args.print_context,
        args.print_message,
        args.max_number_repetitions,
        args.file,
        args.generic_prompt,
        args.logs_folder,
        args.python_version
    )

    runner.run()