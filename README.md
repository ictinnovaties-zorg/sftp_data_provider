# sftp_data_provider
A python package that allows you to read data stored on an SFTP server directly into a Pandas dataframe. By storing the data on an SFTP server and letting the data be loaded directly from the server, there is no need for the data to be on the local computer of the user. This is preferable for sensitive information to for example emailing the data to all the users. The user management system of the SFTP server ensures that only authorized users can access the data. 

In this readme file we provide a simple usage tutorial, for more details regarding the software we refer to the [design documentation](design.md). We also kept [a development diary](labbook.ipynb), which can be used to see in detail what choices we made in developing this software. 

# Authors
- [Paul Hiemstra](mailto:p.h.hiemstra@windesheim.nl)

# Installation
You can install the package using:

    TODO add here, probably `pip install git-repo-url`

# Usage
### Directly loading data
Once you have the library installed, there are two possible ways of getting the data. The first uses the `get_sftp_data` directly:

    from sftp_data_provider import get_sftp_data
    import pandas as pd

    get_sftp_data("data_file.xlsx", pd.read_excel)

where the file `data_file.xlsx` is stored in the root of the SFTP user directory that the user has access to. Note that the SFTP credentials are not passed via `get_vicodin_data`, but are stored in a `.env` file in the working directory on the local machine. The `.env` file has the following three variables that need to be set:

    SFTP_HOSTNAME='123.44.55.66.77'
    SFTP_USERNAME='testuser'
    SFTP_PASSWORD='password'

these are the hostname of the SFTP server (name or ip-address), and the username and password for the SFTP server. 

### Loading data via hidden getter
The second option is not to use `get_sftp_data` directly, but also load the code from the SFTP server. This is useful in case loading the data contains sensitive information such as the password to an Excel file. Take for example this code:

    import pandas as pd
    from sftp_data_provider import get_sftp_data , decrypt_excel_bytes

    def psma_loader(bytes_io):
        '''
        Decrypts the BytesIO stream containing the PSMA data and returns a pandas dataframe
        '''
        decrypted = decrypt_excel_bytes(bytes_io, password="password")
        return pd.read_excel(decrypted, sheet_name='Data', nrows=60, skiprows=1)

    def get_psma_file():
        '''The function you can use to get the psma data
        
        The only requirement is to have a valid username and password stored in the .env file
        '''
        return get_sftp_data('database_psma_met_functies.xlsm', loader_function=psma_loader)

Here we do not use `pd.read_excel` as the loader function, but write our own custom loader function that decrypts the Excel file that was password protected. We do not want this password to be visible to the user. What we can do then is to store the code above in a `.py` file on the server, and load it using 

    from sftp_data_provider import get_sftp_module

    data_loading_module = get_sftp_module('scripts/load_code.py') 
    data_loading_module.get_psma_file()

In this case the end-user only sees this piece of code, all other details are hidden on the SFTP server. 

# Other files

### sftp_docs
This provides a ZettelKasten based version of the design in `design.md`. This is in the form of a Obsidian vault. You need to install Obsidian to read this version of the documentation. 

### tests/
Provides testing for the tool. This is quite barebones at the moment. TODO: expand these tests!

### Dockerfile
The container definition I use to test the package. 