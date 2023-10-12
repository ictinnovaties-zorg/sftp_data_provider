import unittest
from module_loading_functions import get_vicodin_module
import pandas as pd

isdataframe = lambda x: isinstance(x, pd.DataFrame)

# TODO: create additional layer of subclassing to
#        test the different types of accounts
# TODO: add option to choose if `data_loading_functions.py` will
#       be read locally or from the server
# TODO: add way to switch accounts by changing the .env
#       file that is loaded
# TODO: maybe add two test accounts on the server to test this
#       functionality. Now we rely on a specific project, which
#       might not be present next time we run the test. 
class TestPSMAaccount(unittest.TestCase):

    def test_test_data(self):
        # Note that we use the local file here for testing, this is intentional as the standard use case is to test a newly developed data_loading_functions.py file
        data_loading_module = get_vicodin_module('scripts/data_loading_functions.py', local_file="data_loading_functions.py")
        test_data = data_loading_module.get_test_file()
        self.assertTrue(isdataframe(test_data))
    
    def test_psma_data(self):
        data_loading_module = get_vicodin_module('scripts/data_loading_functions.py', local_file="data_loading_functions.py")
        psma_data = data_loading_module.get_psma_file()
        self.assertTrue(isdataframe(psma_data))
    
    def test_lymfoma_data(self):
        data_loading_module = get_vicodin_module('scripts/data_loading_functions.py', local_file="data_loading_functions.py")
        lymfoma_data = data_loading_module.get_lymfoma_non_radiomics(silent_fail=True)
        self.assertTrue(lymfoma_data is None)
    
    def test_data_loading(self):
        try:
            data_loading_module = get_vicodin_module('scripts/data_loading_functions.py')
        except:
            self.fail("Could not load data_loading_functions.py")

if __name__ == '__main__':
    unittest.main()