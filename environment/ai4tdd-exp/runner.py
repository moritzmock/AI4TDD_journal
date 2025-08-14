"""
This module automates an AI-assisted Test-Driven Development (TDD) workflow using AI.

Runners included:
- FullyAutomatedTDDRunner: Iteratively creates both tests and production code based on user prompts.
- CollaborativeTDDRunner: Engages interactively with AI using detailed error traces and developer guidance.
- LogRunner: Executes test cases and captures outputs without AI involvement.

Environment variables:
- PARTICIPANT_ID: Controls which runner is executed.
- OPEN_AI_KEY: Required to access OpenAI API.
"""


import os
import argparse
import sys
sys.path.append("../")
from LogRunner import LogRunner
from CollaborativeTDDRunner import CollaborativeTDDRunner
from FullyAutomatedTDDRunner import FullyAutomatedTDDRunner, CREATE_TEST_CODE, CREATE_PRODUCTION_CODE
from utils import str2bool


def params():
    parser = argparse.ArgumentParser(description='Description of your program.')

    parser.add_argument('--full_context', type=str2bool, help='sending the full context to OpenAI.', default=False)
    parser.add_argument('--print_context', type=str2bool, help='Printing the context before the it is send.', default=False)
    parser.add_argument('--print_message', type=str2bool, help='Printing the message received from OpenAI.', default=False)
    parser.add_argument('--max_number_repetitions', type=int, help='Maximum number of chances given to OpenAI for solving a test case.', default=5)
    parser.add_argument('--file', type=str, help='Path to the file for the test case.', required=True)
    parser.add_argument('--generic_prompt', type=str, help='Prompt which is passed to the AI together with the error trace, production code, and test code.', default="I have the above test, what would be a minimal code so that the test no longer fails. Built-in functions are not allowed.")
    parser.add_argument('--logs-folder', type=str, help='Folder to which all logs are saved.', default='./logs')
    parser.add_argument('--python-version', type=str, help='Local command to executed python, e.g., python or python3', default='python')
    parser.add_argument('--interaction-mode', type=str, help=f'Choose between the two modes {CREATE_TEST_CODE} and {CREATE_PRODUCTION_CODE}', choices=[CREATE_TEST_CODE, CREATE_PRODUCTION_CODE], default=None)
    parser.add_argument('--prompt', type=str, default=None)

    return parser.parse_args()


if __name__ == '__main__':
    args = params()

    try:
        participant_id = int(os.getenv('PARTICIPANT_ID'))
    except:
        print("Missing or invalid participant ID.")
        quit()

    openAI_key = os.getenv('OPEN_AI_KEY')

    if participant_id == -1:
        assert args.interaction_mode is not None, f"Interaction mode needs to be set! --interaction-mode <{CREATE_TEST_CODE} or {CREATE_PRODUCTION_CODE}>"
        assert (args.prompt is not None or args.interaction_mode != CREATE_TEST_CODE), f"A prompt needs to be passed! --prompt <custom prompt of test case specification>"

        runner = FullyAutomatedTDDRunner(
            openAI_key,
            args.print_context,
            args.print_message,
            args.file,
            args.prompt,
            args.logs_folder,
            args.python_version,
            args.interaction_mode
        )

    elif participant_id % 2 == 1:
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

    else:
        runner = LogRunner(args.python_version, args.logs_folder, args.file)

    runner.run()
