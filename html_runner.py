import unittest
from HtmlTestRunner import HTMLTestRunner

test_suite = unittest.TestLoader().discover('tests')
runner = HTMLTestRunner(output='report')
runner.run(test_suite)