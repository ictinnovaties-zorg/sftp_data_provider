FROM continuumio/anaconda3

# Copy the package into the container to be able to make
# a editable install. This enables us to quickly test the 
# state of the package. 
WORKDIR /tmp
COPY . .
RUN pip install -e .