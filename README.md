# Intro
This repo contains the code needed to load sensitive data from an SFTP server. This is to prevent data from having to be stored locally, which is a security risk. In addition, being sure everyone deletes the data after the project is hard. 

# Relevant files
### labbook.ipynb

The labbook notebook contains a development diary which documents how the tool was developed. It is a little rough around the edges, but it clearly shows the thoughts I had and choices I made. 

### design.md
This present a more coherent design of the tool: what where the requirments, and how did we develop the tool to actually meets those requirements. The design is based in part of the documentation in labbook.ipynb. 

### sftp_docs
This provides a ZettelKasten based version of the design in `design.md`. This is in the form of a Obsidian vault. You need to install Obsidian to read this version of the documentation. 

### module_loading_functions.py
The code needed to be able to read the data processing code from the SFTP server. See the design for more details. 

### data_loading_functions.py
This files contains the code needed to actually read the data from the SFTP server. See the design for more details. 

### tests.py 
Provides testing for the tool. This is quite barebones at the moment. TODO: expand these tests!
