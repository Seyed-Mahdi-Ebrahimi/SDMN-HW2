# define a Dockerfile based on python:3 image.
FROM python:3

#use this path as the default location for all subsequent command 
WORKDIR /SDMN_HW2

COPY MySimpleHttpServer.py /SDMN_HW2/

# copy the requirements.txt file into the working directory1 
# COPY requirements.txt requirements.txt

#to install all requirements on container
# RUN pip3 install -r requirements.txt

# we will set the container’s start command to execute the script
CMD ["python","MySimpleHttpServer.py"]
