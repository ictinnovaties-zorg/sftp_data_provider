import tempfile
import importlib.util
import paramiko
from dotenv import load_dotenv
import os
from pathlib import Path

# TODO: schrijf de print messages in deze file om n

'''
This file provides a set of functions that can load code from an SFTP server
into a Python module like structure. For example, if you have a source file that 
contains the function a(), after loading the module like this:

    module = get_sftp_module("source_file_with_function_a.py")
    module.a()

you can call the function a() using module.a(). 

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

def make_module(fname):
    ''''Load a module from a file

    Parameters
    ----------
    fname : str
        The name of the file on the SFTP server that contains the code to be wrapped in a module
    
    Returns
    -------
        A list(-like) object that contains the functions provided by the module
    '''
    spec = importlib.util.spec_from_file_location("load_sftp_data", fname)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_sftp_module(fname, local_file=None):
    '''Load a module from the SFTP server. 
    
       Note that the configuration of the SFTP is read from a configuration file (.env), 
       and stored in the variables HOSTNAME, USERNAME and PASSWORD. This function is not
       meant to be run without the code that reads the environment variables from the config
       file. 

       In addition, I conciously do not use NamedTemporaryFile here, because it leads to errors
       under windows 10. The old code openend a temporary file with the code we want to load, and 
       then loaded the file again using make_module from importlib. This worked fine under windows 11
       but showed permission errors under windows 10. The solution is to simply open a file manually
       check that the file does not exist, and then write the code to the file.

    Parameters
    ----------
    fname : str
        The name of the file on the SFTP server that contains the code to be wrapped in a module
    local_file : str, optional
        If this parameter is not None, the module will be loaded from the local file system instead of the SFTP server.
    '''
    if local_file is not None:
        module = make_module(local_file)
    else:
        try:  # Note I use the try only for the `finally` clause.
            # TODO: Update to using GUID based filename?
            tmp_path = Path('blurpbla.py')   # I do not use NamedTemporaryFile here, because it leads to errors under windows 10. See documentation at the start of this function
            with tmp_path.open('wb') as tmp_file:
                with paramiko.SSHClient() as ssh_client:
                    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh_client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD, allow_agent=False)
                    sftp_client = ssh_client.open_sftp()
                    with ssh_client.open_sftp() as sftp_client:
                        with sftp_client.open(fname) as f:
                            tmp_file.write(f.read())
            module = make_module(tmp_path)
        finally: # include finally to ensure the temp file is removed in all cases
            tmp_path.unlink() # remove the temporary file

    return module