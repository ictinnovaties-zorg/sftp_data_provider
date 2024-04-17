FROM continuumio/anaconda3

# Copying the local sftp_data_provider package to the container and installing it
# ARG package_version=0.5
# COPY ../dist/sftp_data_provider-$package_version.tar.gz /tmp/sftp_data_provider-$package_version.tar.gz
# RUN pip install /tmp/sftp_data_provider-$package_version.tar.gz
RUN pip install git+https://github.com/ictinnovaties-zorg/sftp_data_provider.git