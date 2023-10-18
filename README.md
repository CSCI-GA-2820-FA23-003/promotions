# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## Spint 1 

## Description
This service is designed to manage promotions. It offers endpoints to create, retrieve, update, and delete promotions.

---

## API Endpoints

### 1. Root URL

- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: A basic endpoint to check if the service is up and running.
- **Response**:
  - `200 OK`: Reminder: return some useful information in json format about the service here.

---

### 2. Create Promotion

- **Endpoint**: `/promotions`
- **Method**: `POST`
- **Description**: Create a new promotion using the data provided.
- **Request Body**:
  - JSON containing the promotion data.
- **Response**:
  - `201 Created`: Returns the created promotion as JSON.
  - `415 Unsupported Media Type`: If the request is not JSON.

---

### 3. Delete Promotion

- **Endpoint**: `/promotions/<int:promotion_id>`
- **Method**: `DELETE`
- **Description**: Delete a specific promotion by its ID.
- **Response**:
  - `404 Not Found`: If the promotion with the given ID doesn't exist.
  - `400 Bad Request`: If the confirmation parameter is missing or false.

---

### 4. Update Promotion

- **Endpoint**: `/promotions/<int:promotion_id>`
- **Method**: `PUT`
- **Description**: Update the information of a specific promotion using its ID.
- **Request Body**:
  - JSON containing the updated promotion data.
- **Response**:
  - `200 OK`: Returns the updated promotion as JSON.
  - `404 Not Found`: If the promotion with the given ID doesn't exist.
  - `405 Method Not Allowed`: If the promotion is already expired.
  - `415 Unsupported Media Type`: If the request is not JSON.
  - `400 Bad Request`: For data validation errors.

---

### 5. List All Promotions

- **Endpoint**: `/promotions`
- **Method**: `GET`
- **Description**: Retrieves a list of all promotions.
- **Response**:
  - `200 OK`: Returns a list of all promotions as JSON.

---

### 6. Retrieve a Specific Promotion

- **Endpoint**: `/promotions/<int:promotion_id>`
- **Method**: `GET`
- **Description**: Retrieves the details of a specific promotion using its ID.
- **Response**:
  - `200 OK`: Returns the requested promotion as JSON.
  - `404 Not Found`: If the promotion with the given ID doesn't exist.

---





## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
