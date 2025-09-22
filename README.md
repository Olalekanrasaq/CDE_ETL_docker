# ETL Pipeline with Docker

In this project, a ETL pipeline was written with python, that extract data from a csv file, transform the data, and then load into a postgres database.

# Reproducibility

- Have docker installed on your system
- Clone the project repository into your system
- Open a bash terminal from the project directory and run the [bash script](./etl_script.sh) `etl_script.sh`

# Project Details

The project contains the following files:
- The [`Dockerfile`](./Dockerfile) - containing the instructions for building the docker image. The base image used is python:3.12-slim.
- [Requirement text file](./requirements.txt) `requirements.txt` - containing the python libraries to be intalled and built into docker image.
- [Python file](./docker_etl.py) `docker_etl.py` - the python codes for the pipeline.
- [Bash Script](./etl_script.sh) `etl_script.sh` - containing the bash shell commands (majorly docker commands) for running the pipeline.

# ETL Process 
- Extraction: The extract function read a csv file from a specified [url]("https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2023-financial-year-provisional/Download-data/annual-enterprise-survey-2023-financial-year-provisional.csv") into a panda dataframe.
- Transformation: The extracted dataframe was transformed by;
  - converting all column names to lower case
  - selecting only interested columns of data
- Loading: The transformed data was loaded into a postgres database.
