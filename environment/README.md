# FA executions

In the following commands, the fully automated model used in our experiment can be found. It should be noted that in the second case of test case generation, the complete set of instructions is not passed, since it represents an extension of an edge case rather than the inclusion of a new feature.

```commandLine
cd ai4tdd-exp


python runner.py --file experiment.py --interaction-mode CREATE_TEST_CODE --prompt "TextFormatter takes arbitrary words and horizontally centers them into a line it contains three functions. The first is called setLineWidth and sets the length of the line. The second function receives a single word and returns the word in the centre of the line. The third function receives two words and centres the two words in the line. Use this test specification: line width=10 and word='word'"

python runner.py --file experiment.py --interaction-mode CREATE_PRODUCTION_CODE

python runner.py --file experiment.py --interaction-mode CREATE_TEST_CODE --prompt "Use this test specification: line width=10 and word='hello'"

python runner.py --file experiment.py --interaction-mode CREATE_PRODUCTION_CODE

python runner.py --file experiment.py --interaction-mode CREATE_TEST_CODE --prompt "TextFormatter takes arbitrary words and horizontally centers them into a line it contains three functions. The first is called setLineWidth and sets the length of the line. The second function receives a single word and returns the word in the centre of the line. The third function receives two words and centres the two words in the line. Use this test specification: line width=10 and words=['foo', 'bar']"

python runner.py --file experiment.py --interaction-mode CREATE_PRODUCTION_CODE
```
