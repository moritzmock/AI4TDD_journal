"""
FullyAutomatedTDDRunner automates a Test-Driven Development workflow by coordinating between a user-defined prompt and an AI-powered test/code generator.

Key features include:
- Initializing an AI handler configured for generating unit tests or production code based on textual prompts.
- Supporting different interaction modes: generating test code or generating production code.
- Automatically determining how many prior test cases to skip based on file state.
"""


from TestCodeAIHandler import TestCodeAIHandler
from utils import how_many_to_skip

CREATE_TEST_CODE = "CREATE_TEST_CODE"
CREATE_PRODUCTION_CODE = "CREATE_PRODUCTION_CODE"

class FullyAutomatedTDDRunner():

    def __init__(self, key, print_context, print_message, file, prompt, logs_folder, python_version, interaction_mode):
        self.handler = TestCodeAIHandler(
            key=key,
            role="You are part of a Test Driven Development team. Your role is the tester, create out of a textual description a test case using the library 'unittest'.",
            print_context=print_context,
            print_message=print_message,
            file=file,
            prompt=prompt,
            logs_folder=logs_folder,
            python_version=python_version
        )
        self.interaction_mode = interaction_mode
        self.skip = how_many_to_skip(file) + 1

    def run(self):
        if self.interaction_mode == CREATE_TEST_CODE:
            self.handler.create_test_code()
        elif self.interaction_mode == CREATE_PRODUCTION_CODE:
            self.handler.generate_production_code()
