# PrettyTextTestRunner
A simple Python unittest  drop-in replacement for Python's TextTestRunner.

## Why Did You Write This? Can't You Just Use &lt;insert latest/hotest framework here&gt;?
While I (and others) could learn the new framework dé jour, I'm much more interested in getting things working and just getting things done. I needed to start testing a Flask application, and found that Python's unittest is a tad limited out of the box.   [Viniciusd's TestRunner.py](https://gist.github.com/viniciusd/73e6eccd39dea5e714b1464e3c47e067) is a great hack,  found the text output to be great but was still hacking HTMLTestRunner (of which it was based) and didn't need to output actual report files still being generated.

I wanted to quickly see what worked, what didn't, and why when it didn't. Therefore I wrote this library, to properly override methods in the TestResult and TextTestRunner classes and output text tables or a simple micro result.

## Okay, Okay What Makes This So Great?
Importing over `TextTestRunner` is all you need to do.
```
# from unittest import TextTestRunner 
from PrettyTextTestRunner import PrettyTextTestRunner 
from unittest import TestLoader, TestSuite

# Import your TestCase files
import test_suite_file1
import test_suite_file2

# Load your TestCases
testcase1 = TestLoader().loadTestsFromTestCase(test_suite_file1.testcase1)
testcase2 = TestLoader().loadTestsFromTestCase(test_suite_file2.testcase2)

# Make a Suite
suite = TestSuite([testcase1, testcase2])

# Run it
runner = PrettyTexyTestRunner()
runner.run(suite)
```

That's it. It's difficult enough when starting out writting test cases to have to learn a new tool, library, or framework to get things done.  Focus on writting better test cases, and look to get easier (and more informative!) results to read out of the box.
```
Summary
------------------------------------------------------------------------------------------
| Test Suite/Test Case         | Count | Pass  | Fail  | Error | Skip  | Unexp  | Expect |
|                              |       |       |       |       |       | Sucess | Fails  |
------------------------------------------------------------------------------------------
| test_case.samples            |   3   |   3   |   0   |   0   |   0   |   0    |   0    |
| Totals                       |   3   |   3   |   0   |   0   |   0   |   0    |   0    |
------------------------------------------------------------------------------------------
test_case.samples
     ------------------------------------------------------------------------------------------------------
     | Test Name                    | Output                                           |           Status |
     ------------------------------------------------------------------------------------------------------
     | test_sample_case             |                                                  |     (0.01s) PASS |
     |                              |                                                  |                  |
     | test_sample_case2            |                                                  |    (0.004s) PASS |
     |                              |                                                  |                  |
     | test_sample_case3            |                                                  |    (0.004s) PASS |
     ------------------------------------------------------------------------------------------------------
runtime: 0.037s
```

## Make Those Reports Yours
Don't like that the test reports have border or have a margin between rows? You do you, and make it how you like it, quickly and easily.  The method `setProps` allows you to update the default style to something more condusive for you.
```
newStyle = {
	"titles": ["column title", ... ],
	"colWidths": [x, ... ],  # In characters
	"colJustify": ["right"|"center"|"left", ... ],
	"padding": 1,  # In characters
	"indent": 5,   # Indent entire text block by `x` characters
	"margins": {"top":0, "bottom": 0, "left": 0, "right": 0},
	"border": "solid"|"columnDelimit"
}

runner.setProps(summary=newStyle, testReport=newStyle)
```

## That's Still Too Much Information Being Displayed!
What's that? You want more but less? Can do! Setting the object property `mode = "simple"` gets you the bare minimum to scratch the itch of every dev-ops stats nerd our there.
```
runner.mode = "simple"
runner.run(suite)
>>> ...FFFF. pass: 3, failed: 0, errors: 0, runtime: 0.035s
```
Sure you don't get error messages, or output content from test cases, but maybe you don't need that.
