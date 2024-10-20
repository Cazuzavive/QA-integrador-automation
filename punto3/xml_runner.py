import unittest
import xmlrunner 

test_suite = unittest.TestLoader().discover('tests')
runner = xmlrunner.XMLTestRunner(output='test-reports')
runner.run(test_suite)