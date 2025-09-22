#!/bin/bash

# This script runs the ETL process inside a Docker container.
echo "Starting the ETL process inside a Docker container..."

# Define the Docker image and container names
IMAGE_NAME="cde_etl_img"
ETL_CONTAINER="cde_etl_cont"
POSTGRES_CONTAINER="cde_etl_postgrescont"

echo -e "\nBuilding the Docker image..."
# Build the Docker image
docker build -t $IMAGE_NAME .

echo -e "\nDocker image built successfully!!!"

# create a network for the containers
docker network create etl_network

echo -e "\nStarting PostgreSQL container..."

# Ensure the PostgreSQL container is running
docker run \
  --name $POSTGRES_CONTAINER \
  --network etl_network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=cde_database \
  -d postgres

sleep 10  # Wait for PostgreSQL to initialize

echo -e "\nPostgreSQL container is running."

echo -e "\nRunning the ETL container..."

# Run the Docker ETL container
docker run \
  --name $ETL_CONTAINER \
  --network etl_network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_HOST=$POSTGRES_CONTAINER \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_DB=cde_database \
  $IMAGE_NAME

echo -e "\nETL process completed successfully!!!"