# Machine-Learning-Systems-Engineering

This project covers the end-to-end development, validation, and deployment of a machine learning system from to a production enviorment in Azure. 

Below is a quick gide to this Github's structure:

Project Documention.txt - A quick guide on how to spin up the project on Azure and the commands necessary

projectfiles - The main folder that holds all the components of this project including the API, machine learning model, Kubernates configuration files and the Poetry files detailing the specific dependencies needed for the project

Key subdirectories within projectfiles:

.k8s - the .yaml files specifying how the service should be instantiated, mantatined, and scaled to accomidate loads on Azure

src - houses the API endpoints and defines the routes in the architecture

tests - used to validate the model and endpoints work as expected prior to deployment

trainer - used to train and save the model leveraged in making predictions

Dockerfile - specified how to containeraize and deploy the API

poetry.toml - details the packages + versions used in the project
