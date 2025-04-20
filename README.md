# Machine-Learning-Systems-Engineering

This project covers the end-to-end development, validation, and deployment of a machine learning system from to a production environment in Azure. 

Below is a quick guide to GitHub's structure:

Project Documentation.txt - A quick guide on how to spin up the project on Azure and the commands necessary

projectfiles - The main folder that holds all the components of this project, including the API, machine learning model, Kubernetes configuration files, and the Poetry files detailing the specific dependencies needed for the project

Key subdirectories within projectfiles:

.k8s - the .yaml files specifying how the service should be instantiated, maintained, and scaled to accommodate loads on Azure

src - houses the API endpoints and defines the routes in the architecture

tests - used to validate that the model and endpoints work as expected before deployment

trainer - used to train and save the model leveraged in making predictions

Dockerfile - specifies how to containerize and deploy the API

poetry.toml - details the packages + versions used in the project
