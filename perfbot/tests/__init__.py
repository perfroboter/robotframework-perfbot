# see https://github.com/ctb/SomePackage
# implement a basic test under somepackage.tests
import unittest
        
def get_suite():
    "Return a unittest.TestSuite."
    import perfbot.tests
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(perfbot.tests)
    return suite
