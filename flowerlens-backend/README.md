# Backend Overview for FlowerLens

FlowerLens is a robust, AI-powered web application designed for flower identification and analysis. This document provides an overview of the backend architecture, highlighting its key functionalities, integration with the CNN model, and interactions with the frontend.

## Backend Architecture

Built on the Django framework, our backend serves as the backbone for the application, handling data processing, user requests, and communication with the Convolutional Neural Network (CNN) model and the PostgreSQL database.

![Flower Flowchart](FlowerLensBackend/media/flower%20flowchart.jpg)


### Key Components:

-   **Django Framework**: Leveraging Django's powerful features for rapid development, security, and scalability.
-   **RESTful API**: Facilitating communication between the frontend and backend with RESTful endpoints.
-   **Pipe-and-Filter Architecture**: Adopting a pipe-and-filter pattern for API calls to process and route requests efficiently.
-   **Integration with CNN Model**: Interfacing with the AI model for flower prediction and analysis.
-   **PostgreSQL Database**: Storing and managing application data reliably and efficiently.

## Core Functionalities

### User and Admin Interactions:

-   **User Endpoints (`pipe_filter_user`)**: Handles user-related requests such as uploading photos for flower identification. Utilizes the `upload_photo` function to process user uploads, interact with the CNN model, and retrieve predictions along with additional flower information.

-   **Admin Endpoints (`pipe_filter_admin`)**: Dedicated endpoints for administrative tasks including listing, training, evaluating AI models, fetching confusion matrices, rolling back, and deploying models. Functions like `train_ai_model` and `deploy_model` are part of this suite.


### AI Model Management:

-   **CNN Model Communication (`cnn_model_pipefilter`)**: A specialized endpoint to handle requests related to the CNN model, like saving trained models. It uses the `save_model` function to save model data, including performance metrics and confusion matrices.

### Authentication:

-   **Login and Logout**: Secure endpoints for admin login and logout, ensuring controlled access to administrative functionalities. The authentication library used is jwt. The jwt token is generated in the backend and it's sent to the frontend.

### Flower information
- The information about the flowers is stored in JSON files. The information was generated using Open AI's ChatGPT and verified using [The Royal Horticultural Society](https://www.rhs.org.uk/plants/) and wikipedia . When a flower prediction is made, the respective json file that contains the information about it is sent to the frontend as a response.

## Testing and CI Pipeline

-   **Automated Tests**: Comprehensive tests covering various backend functionalities to ensure code integrity and reliability.
-   **Continuous Integration (CI) Pipeline**: Automated pipeline set up for continuous integration, ensuring that new code commits are automatically built, tested, and reported.

# Getting Started


## Steps to run the server and database:

### Create a virtual environment

#### Windows 
- [ ] First, check if Python 3 is installed
```
python

```
- [ ] Create a virtual environment
```
mkdir ~/.virtualenvs 
cd path/to/virtualenvs
python -m venv venv

```

- [ ] Activate environment 
```
venv\Scripts\activate

```
- [ ] Deactivate environenment 
```
deactivate

```

### Run application 

- [ ] Open the project 
```
cd path/to/backened/application

```
it should end with "flowerlens-backend/"
- [ ] Install all requirements, make sure the environement is activated 
```
pip install -r requirements.txt

```
- [ ] Run the application 
```
cd flowerlens-backend/FlowerLensBackend/
python manage.py runserver

```

### Database administration 
#### Create a user 
- [ ] You have to register/make an account
```
python manage.py createsuperuser

```
In the console, register 
- Name
- Email 
- Password 
- Password again 

#### Start the admin dashboard 
- [ ] In the console you should see something like this: 
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 22, 2023 - 12:21:18
Django version 4.2.7, using settings 'FlowerLensBackend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```
- [ ] Click on the server "http..." 
- [ ] On the web browser add "/admin" like this "http://127.0.0.1:8000/admin


## Contributions

##### Albin Karlsson 

##### Erik Lindmaa

