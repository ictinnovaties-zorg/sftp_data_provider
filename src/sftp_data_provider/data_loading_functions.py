import pandas as pd
import paramiko
import importlib.util
import io
import os
from dotenv import load_dotenv
import msoffcrypto
import logging
from functools import partial, reduce
import pathlib

'''
This file provides a set of functions that can load data from an SFTP server. The core of the 
system is the `get_sftp_data` function, which establishes a connection to the SFTP server, 
loads the data into a BytesIO stream and then calls a loader function to load the data into a
pandas dataframe.

Each source of data consists of two functions:
- A get function that returns a pandas dataframe
- A loader function that converts the BytesIO stream from the SFTP server to a pandas 
  dataframe. This can be as simple as a call to pd.read_csv, but can also invlove more 
  complex steps. 

The configuration of the SFTP server is read from a configuration file (.env), this
file should be placed in the main folder of the project. This nicely separates the
configuration of the SFTP server from the code that uses it. Getting the configuration
information to the SSH connection is not done via passing the values as parameters to
the functions. This has the advantage of making the interfaces less bloated, but has the
disadvantage that the functions below cannot really be run outside of the context of this file.
'''

# Load the environment variables that configure the SFTP server
load_dotenv()
HOSTNAME = os.getenv("SFTP_HOSTNAME")
USERNAME = os.getenv("SFTP_USERNAME")
PASSWORD = os.getenv("SFTP_PASSWORD")

# Raise a meaningful error if the environment variables are not set
if HOSTNAME == None or USERNAME == None or PASSWORD == None:
    raise ValueError("Could not find the configuration of the SFTP server. You probably forgot to put the required .env file in your projects main folder. ")

def get_sftp_data(fname, loader_function, silent_fail=False):
    '''Get a file from the server and load it using the loader_function. Returns a pandas dataframe

    This is a worker function that is used as a basis to write the actual functions
    that get the data. It is not intended to be used directly. The loader function takes
    the file from the server in the form of a bytesIO stream and returns a valid pandas dataframe. 
    This can be as simple as a call to pd.read_csv or pd.read_excel, but can also be more complex if need be. 

    Parameters
    ----------
    fname : str
        The name of the file to get
    loader_function : function
        A function that takes a file-like object and returns a pandas dataframe
    silent_fail : bool
        If True, the function will hide the error message if the file is not found on the server.

    returns
    -------
    pandas.DataFrame
        The data from the file as a pandas dataframe
    or None is the file does not exist
    '''
    with paramiko.SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD, allow_agent=False)
        sftp_client = ssh_client.open_sftp()
        with ssh_client.open_sftp() as sftp_client:
            try:
                with sftp_client.open(fname, 'rb') as f:
                    return loader_function(io.BytesIO(f.read()))
            except FileNotFoundError:   # Provide more informative error message
                if not silent_fail:
                    file_list = '\n - '.join(sftp_client.listdir())
                    logging.error(f'Could not find file {fname} on the server. The following files are available:\n - {file_list}')
                    return None

#### HELPER FUNCTIONS ####
def compose(*func):
    '''
    Based on the composite_function from https://www.geeksforgeeks.org/function-composition-in-python/
    '''
    def compose_helper(f, g):  
        return lambda x : g(f(x)) # Swapped f and g to change the order of execution of the list of functions in *func
    return reduce(compose_helper, func, lambda x : x)

def decrypt_excel_bytes(bytes_io, password):
    ''''
    Take the bytesIO stream containing the encrypted excel file and return a decrypted bytesIO stream
    '''
    decrypted = io.BytesIO()
    file = msoffcrypto.OfficeFile(bytes_io)
    file.load_key(password=password)  # Use password
    file.decrypt(decrypted)
    return decrypted

### This is where the actual work is done ###

### TEST FUNCTIONS ###
get_test_file = partial(get_sftp_data, 'scripts/test.csv', loader_function=pd.read_csv)
get_non_existing_data = partial(get_sftp_data, 'non_existing_file.xlsx', loader_function=pd.read_excel)