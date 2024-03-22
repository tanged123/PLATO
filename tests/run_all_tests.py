#tests/run_all_tests.py

import sys
import os
import unittest

# Assuming the script is run from the PLATO/tests directory
# Add the parent directory (PLATO/tests) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

if __name__ == '__main__':
    # Set the environment variable to indicate we're in test mode
    os.environ['RUNNING_TESTS'] = 'True'

    # Define test directories
    test_dirs = ['unit', 'integration']
    
    # Loader to gather tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Loop through the directories and discover tests
    for test_dir in test_dirs:
        discovered_tests = loader.discover(start_dir=test_dir, pattern="test_*.py")
        suite.addTests(discovered_tests)

    # Run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)

    # Clean up: Remove the environment variable after tests are done
    # This ensures the environment variable doesn't affect subsequent operations
    del os.environ['RUNNING_TESTS']