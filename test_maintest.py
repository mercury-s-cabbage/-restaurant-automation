import unittest

'''Запустить все тесты'''

loader = unittest.TestLoader()
suite = loader.discover('Tst')

runner = unittest.TextTestRunner()
runner.run(suite)