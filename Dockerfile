# Build basic image
FROM python:3.10

# Set your working directory
WORKDIR /home/user/Scrivania/CNR/VRE/CODE/aeflow/

# Copy the necessary files
COPY ./aeflow.py .
COPY ./get_data.py .
COPY ./config.yaml .
COPY ./requirements.txt .
#COPY ~/.cdsapirc .

# Install the necessary packages
RUN pip install -r ./requirements.txt

# Creating working directories
RUN mkdir -p ./data
RUN mkdir -p ./graphs

# Run the app
ENTRYPOINT ["python3", "aeflow.py"]

#