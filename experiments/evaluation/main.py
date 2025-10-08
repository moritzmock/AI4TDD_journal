"""
This script is a dynamic test framework for evaluating multiple implementations of a TextFormatter class from each of the participants.
Loads dynamically the different submission of the participants.
Defines a reference TextFormatter class for comparison and test generation.
Dynamically generates unittest test cases using various configurations.
Each of the participants execution is handeled individually, and can be added or removed by commenting-in/out the corresponding lines (P1-P16)
Executes tests via a unified test suite, showing pass/fail results for each dynamically generated test method.

Before the execution the files P1-P16 and F1.zip needs to be unzipped.
The following command can be used for it:

for file in *.zip; do unzip "$file" -d "${file%.zip}"; done

Afterwards individual code blocks in the main needs to be uncommented,
such the evaluation can be performed one by one.
"""

import unittest
import os
import importlib.util
import inspect

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load_text_formatter(relative_path, module_name):
    full_path = os.path.join(base_path, *relative_path.split('/'))
    print(f"Loading from: {full_path}")
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")

    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Error loading module {module_name} from {full_path}: {e}")

    if not hasattr(module, "TextFormatter"):
        raise AttributeError(f"'TextFormatter' not found in {full_path}")

    return module.TextFormatter

'''
F1 = load_text_formatter('F1/test_case_4_4.py', 'test_case_4_4')
P1 = load_text_formatter('P1/experiment.py', 'experiment')
P2 = load_text_formatter('P2/testePython/experiment.py', 'experiment')
P3 = load_text_formatter('P3/P3/experiment.py', 'experiment')
P4 = load_text_formatter('P4/P4/experiment.py', 'experiment') # commented out a lince such that no syntax error was thrown
P5 = load_text_formatter('P5/P5/experiment.py', 'experiment')
P6 = load_text_formatter('P6/P6/experiment.py', 'experiment') # removed length from the parameter list and taken it from the class
P7 = load_text_formatter('P7/P7/experiment.py', 'experiment') # slightly changed, such that not \n are generated but spaces
P8 = load_text_formatter('P8/P8/experiment.py', 'experiment')
P9 = load_text_formatter('P9/P9/experiment.py', 'experiment')
P10 = load_text_formatter('P10/content/AI4TDD-main/experiment_1.py', 'experiment')
#P11 = load_text_formatter('P11/content/AI4TDD-main/experiment_1.py', 'experiment') # skipped because the participant created single function and not a class
P12 = load_text_formatter('P12/AI4TDD-main/experiment_1_29.py', 'experiment') # Does not compile
P13 = load_text_formatter('P13/P13/experiment.py', 'experiment')
P14 = load_text_formatter('P14/P14/experiment_8_5.py', 'experiment')
P15 = load_text_formatter('P15/P15/experiment.py', 'experiment')
P16 = load_text_formatter('P16/P16/experiment.py', 'experiment')
'''
# test_MPX = load_text_formatter("test_MPX/text_formatter.py", "text_formatter")

# test_GPT = load_text_formatter("test_GPT_5/text_formatter.py", "text_formatter")

case_1_1 = load_text_formatter("MGX/case_1_1/text_formatter.py", "text_formatter")
case_1_2 = load_text_formatter("MGX/case_1_2/text_formatter.py", "text_formatter")
case_1_3 = load_text_formatter("MGX/case_1_3/text_formatter.py", "text_formatter")

case_2_1 = load_text_formatter("MGX_new/case_2_1/text_formatter_test.py", "text_formatter")
case_2_2 = load_text_formatter("MGX_new/case_2_2/text_formatter_test.py", "text_formatter")
case_2_3 = load_text_formatter("MGX_new/case_2_3/text_formatter_test.py", "text_formatter")

case_3_1 = load_text_formatter("MGX/case_3_1/text_formatter.py", "text_formatter")
case_3_2 = load_text_formatter("MGX/case_3_2/text_formatter.py", "text_formatter")
case_3_3 = load_text_formatter("MGX/case_3_3/text_formatter.py", "text_formatter")
case_3_4 = load_text_formatter("MGX_new/case_3_4/test_text_formatter.py", "text_formatter")
case_3_5 = load_text_formatter("MGX_new/case_3_5/test_text_formatter.py", "text_formatter")
case_3_6 = load_text_formatter("MGX_new/case_3_6/test_text_formatter.py", "text_formatter")

case_again = load_text_formatter("MGX_again/test_text_formatter.py", "text_formatter")


case_F1_1 = load_text_formatter("../environment/ai4tdd-exp/working_F1_1/F1_1/experiment.py", "experiment")
case_F1_2 = load_text_formatter("../environment/ai4tdd-exp/working_F1_2/F1_2/experiment.py", "experiment")
case_F1_3 = load_text_formatter("../environment/ai4tdd-exp/working_F1_3/experiment.py", "experiment")

class TextFormatter:
    def setLineWidth(self, length):
        self.length = length

    def singleWord(self, word):
        p = int((self.length - len(word)) / 2)
        rest = 0 if self.length == p * 2 + len(word) else 1
        return p * " " + word + (p + rest) * " "

    def twoWords_version_1(self, a, b):
        if self.length <= len(a) + len(b):
            return self.singleWord(f"{a}{b}")
        return self.singleWord(f"{a} {b}")

    def twoWords_version_2(self, a, b):
        if self.length <= len(a) + len(b):
            return self.singleWord(f"{a}{b}")
        available_length = self.length - len(a) - len(b)
        one_part = int(available_length / 3)
        padding = 0 if available_length % 3 != 2 else 1
        return self.singleWord(a + " " * (padding + one_part) + b)



def generate_test_case_class(name, class_name, formatter_class, global_setup, method_name, test_specs):
    class DynamicTestCase(unittest.TestCase):
        pass  # no setUp; instantiation moved inside test method

    for i, spec in enumerate(test_specs):
        args = spec["args"]
        expected = spec["expected"]
        test_name = spec.get("name", f"test_{name}_{method_name}_{i}")
        setup = spec.get("setup", {})

        def make_test_func(method_name, args, expected_output, setup):
            def test_method(self):
                line_width = setup.get("lineWidth", None)
                method_name_for_width = setup.get("widthMethod", None)

                # Handle constructor vs. setter logic dynamically
                if method_name_for_width:
                    # Try to init without args and call the setter if it exists
                    try:
                        self.formatter = formatter_class()
                        method = getattr(self.formatter, method_name_for_width, None)
                        if callable(method):
                            method(line_width)
                        else:
                            self.formatter = formatter_class(line_width)
                    except TypeError:
                        # Fallback to constructor-based initialization
                        self.formatter = formatter_class(line_width)
                else:
                    self.formatter = formatter_class(line_width)

                method = getattr(self.formatter, method_name)
                result = method(*args)
                self.assertEqual(result, expected_output)
            return test_method

        setattr(DynamicTestCase, test_name, make_test_func(method_name, args, expected, setup))

    DynamicTestCase.__name__ = class_name
    return DynamicTestCase


def generate_tests(name, formatter_class, method_tests, global_setup=None):
    test_classes = []
    for method_name, tests in method_tests.items():
        class_name = f"Test_{formatter_class.__name__}_{method_name}_{name}"
        test_class = generate_test_case_class(
            name=name,
            class_name=class_name,
            formatter_class=formatter_class,
            global_setup=global_setup,
            method_name=method_name,
            test_specs=tests
        )
        test_classes.append(test_class)
    return test_classes


def generateMethods(func_1, func_2, setLineWidth, array = False):
    return {
        f"{func_1}": [
            {"args": ["word"], "expected": "   word   ", "setup": {"lineWidth": 10, "widthMethod": f"{setLineWidth}"}},
            {"args": ["hello"], "expected": "  hello   ", "setup": {"lineWidth": 10, "widthMethod": f"{setLineWidth}"}},
            {"args": ["hello"], "expected": "hello", "setup": {"lineWidth": 5, "widthMethod": f"{setLineWidth}"}},
            {"args": ["hello"], "expected": "hel", "setup": {"lineWidth": 3, "widthMethod": f"{setLineWidth}"}}, # error - manually validated if that case if checked
            {"args": [""], "expected": " " * 10, "setup": {"lineWidth": 10, "widthMethod": f"{setLineWidth}"}}
        ],
        f"{func_2}": [
            {"args": ["a", "b"] if array is False else [["a", "b"]], "expected": "a        b", "setup": {"lineWidth": 10, "widthMethod": f"{setLineWidth}"}},
            {"args": ["ab", "b"] if array is False else [["ab", "b"]], "expected": "ab       b", "setup": {"lineWidth": 10, "widthMethod": f"{setLineWidth}"}},
            {"args": ["a", "b"] if array is False else [["a", "b"]], "expected": "ab", "setup": {"lineWidth": 2, "widthMethod": f"{setLineWidth}"}},
            {"args": ["a", "b"] if array is False else [["a", "b"]], "expected": "a", "setup": {"lineWidth": 1, "widthMethod": f"{setLineWidth}"}}, # error - manually validated if that case if checked
            {"args": ["a", ""] if array is False else [["a", ""]], "expected": "a         ", "setup": {"lineWidth": 10, "widthMethod": f"{setLineWidth}"}},
            {"args": ["", "b"] if array is False else [["", "b"]], "expected": "         b", "setup": {"lineWidth": 10, "widthMethod": f"{setLineWidth}"}},
            {"args": ["", ""] if array is False else [["", ""]], "expected": " " * 10, "setup": {"lineWidth": 10, "widthMethod": f"{setLineWidth}"}}
        ]
    }


if __name__ == "__main__":
    suite = unittest.TestSuite()
    '''
    # dummy test
    test_classes = generate_tests("dummy", TextFormatter, generateMethods("singleWord", "twoWords_version_1", "setLineWidth"))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    '''

    # F1
    #test_classes = generate_tests("F1", F1, generateMethods("center_text", "spread_words", "__init__", True))
    #for cls in test_classes:
    #    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P1
    #test_classes = generate_tests("P1", P1, generateMethods("centerWord", "spreadWords", "setLineWidth", False))
    #for cls in test_classes:
    #   suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P2
    #test_classes = generate_tests("P2", P2, generateMethods("wordCenter", "wordSpread", "setLineWidth", False))
    #for cls in test_classes:
    #   suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P3
    #test_classes = generate_tests("P3", P3, generateMethods("singleWord", "twoWords", "setLineWidth", False))
    #for cls in test_classes:
    #   suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P4
    #test_classes = generate_tests("P4", P4, generateMethods("center", "spread", "setLineWidth", False))
    #for cls in test_classes:
    #   suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P5
    #test_classes = generate_tests("P5", P5, generateMethods("centerWord", "spreadWords", "setlinewidth", False))
    #for cls in test_classes:
    #   suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P6
    #test_classes = generate_tests("P6", P6, generateMethods("setCenterWord", "setCenterWords", "setLineWidth", False))
    #for cls in test_classes:
    #   suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P7
    #test_classes = generate_tests("P7", P7, generateMethods("get_word_in_center", "space_center", "set_line_width", False))
    #for cls in test_classes:
    #   suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P8
    #test_classes = generate_tests("P8", P8, generateMethods("centerWord", "spreadWord", "setLineWidth", False))
    #for cls in test_classes:
    #    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P9
    #test_classes = generate_tests("P9", P9, generateMethods("centerWord", "spreadWords", "setLineWidth", False))
    #for cls in test_classes:
    #    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P10
    #test_classes = generate_tests("P10", P10, generateMethods("centerWord", "spreadWords", "setLineWidth", False))
    #for cls in test_classes:
    #   suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P12
    #test_classes = generate_tests("P12", P12, generateMethods("centerWord", "equalSpread", "__init__", False))
    #for cls in test_classes:
    #    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P13
    #test_classes = generate_tests("P13", P13, generateMethods("centerWordInLine", "splitWordsInLine", "setLineWidth", False))
    #for cls in test_classes:
    #    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P14
    #test_classes = generate_tests("P14", P14, generateMethods("alignCenter", "alignSpread", "setLineWidth", False))
    #for cls in test_classes:
    #    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P15
    #test_classes = generate_tests("P15", P15, generateMethods("getWordInCenterOfLine", "getWordsInTheEdgesOfLine", "setLineWidth", False))
    #for cls in test_classes:
    #    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    # P16
    #test_classes = generate_tests("P16", P16, generateMethods("findCentralWord", "spreadWords", "setLineWidth", False))
    #for cls in test_classes:
    #    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    '''
    # test_MPX
    test_classes = generate_tests("test_MPX", test_MPX, generateMethods("centerSingleWord", "centerTwoWords", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    

    # test case_1_1
    test_classes = generate_tests("case_1_1", case_1_1, generateMethods("center", "center_two", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    

    # test case_1_2
    test_classes = generate_tests("case_1_2", case_1_2,
                                  generateMethods("centerWord", "centerTwoWords", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    

    # test case_1_3
    test_classes = generate_tests("case_1_3", case_1_3,
                                  generateMethods("center_single", "center_two", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    
    
    # test case_F1_1
    test_classes = generate_tests("case_F1_1", case_F1_1,
                                  generateMethods("center", "center_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
        
    # test case_F1_2
    test_classes = generate_tests("case_F1_2", case_F1_2,
                                  generateMethods("centerWord", "centerWords", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    
    '''
    # test case_F1_3
    test_classes = generate_tests("case_F1_3", case_F1_3,
                                  generateMethods("centerWord", "centerTwoWords", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    '''
    # test case_2_1
    test_classes = generate_tests("case_2_1", case_2_1,
                                  generateMethods("center", "center_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    
    
    # test case_2_3
    test_classes = generate_tests("case_2_3", case_2_3,
                                  generateMethods("center_word", "center_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    
    # test case_3_1
    test_classes = generate_tests("case_3_1", case_3_1,
                                  generateMethods("center_single_word", "center_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    

    # test case_3_2
    test_classes = generate_tests("case_3_2", case_3_2,
                                  generateMethods("centerSingleWord", "centerTwoWords", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    
    # test case_3_3
    test_classes = generate_tests("case_3_3", case_3_3,
                                  generateMethods("center_single_word", "center_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    
    # test case_3_4
    test_classes = generate_tests("case_3_4", case_3_4,
                                  generateMethods("centerWord", "centerTwoWords", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    
    
    # test case_3_5_1
    test_classes = generate_tests("case_3_4", case_3_4,
                                  generateMethods("center_single_word", "center_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    
    # test case_3_5_1
    test_classes = generate_tests("case_3_5", case_3_5,
                                  generateMethods("center_single_word", "center_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
        

    # test case_3_6
    test_classes = generate_tests("case_3_6", case_3_6,
                                  generateMethods("format_single_word", "format_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))

    


    # test case_again
    test_classes = generate_tests("case_again", case_again,
                                  generateMethods("center_single_word", "center_two_words", "setLineWidth", False))
    for cls in test_classes:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    '''
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)