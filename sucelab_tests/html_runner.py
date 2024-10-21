import unittest
from HtmlTestRunner import HTMLTestRunner

test_suite = unittest.TestLoader().discover('tests')
runner = HTMLTestRunner(output='report', report_title='Pruebas SauceLab', combine_reports= True)
runner.run(test_suite)