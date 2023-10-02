# tests/__init__.py

import unittest

# Import test modules
from .test_models import *
from .test_views import *

if __name__ == '__main__':
    # Initialize the test runner
    runner = unittest.TextTestRunner()
    
    # Discover and run all tests
    unittest.main(testRunner=runner)