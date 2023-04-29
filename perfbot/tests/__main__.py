# RUNME as 'python -m somepackage.tests.__main__'
import unittest
import perfbot.tests

def main():
    "Run all of the tests when run as a module with -m."
    suite = perfbot.tests.get_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()