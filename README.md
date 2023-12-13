# NYU DevOps Project - Promotions

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![CI Build](https://github.com/CSCI-GA-2820-FA23-003/promotions/actions/workflows/tdd-tests.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA23-003/promotions/actions/workflows/tdd-tests.yml)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-FA23-003/promotions/graph/badge.svg?token=RMHC0YICQ1)](https://codecov.io/gh/CSCI-GA-2820-FA23-003/promotions)

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
Dockerfile          - instructions for building a Docker image for the application
setup.cfg           - configuration file for automated tasks like linting, testing, etc.
.coverage           - Coverage report file

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── __init__.py        - package initializer
    ├── cli_commands.py    - Flask CLI extension for database management commands
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── factories.py     - factories for creating mock objects in tests
├── test_cli_commands.py     - test suite for CLI command extensions
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes

features/                     - BDD feature files and accompanying test steps
├── steps/                    - Step definition modules for feature tests
│   ├── promotions_steps.py   - Step definitions for promotions feature tests
│   ├── web_detail_steps.py   - Step definitions for web detail feature tests
│   ├── web_steps.py          - Step definitions for web feature tests
│   └── environment.py        - Setup and teardown hooks for BDD tests
└── promotions.feature        - Feature file describing promotion scenarios

k8s/                         - Kubernetes deployment configurations
├── deployment.yaml          - Defines the deployment to manage application pods
├── ingress.yaml             - Configuration for ingress resource to manage external access to the services
├── postgresql.yaml          - Deployment and service configuration for the PostgreSQL database
├── pv.yaml                  - Defines persistent volumes for durable storage
└── service.yaml             - Service configuration to expose the application pods

```

## Sprint 1 & 2

## Description

This service is designed to manage promotions. It offers endpoints to create, retrieve, update, and delete promotions.

---

## Data Model / DB Schema

### Promotion Schema

| Field    | Type  | Description    |
| ------- | ------- | -------- |
| id | int | The promotion id |
| code | str | The Promotion code |
| name | str | The Promotion label (description) |
| start | date | Active date |
| expired | date | Expired date |
| available | int | Code available to use |
| whole_store | bool | Whether is whole store promotion|
| promo_type | int | The Promotion type |
| value | double | Promotion value according to the type |
| created_at | Date | Date the Promotion was created |
| updated_at | Date | Model lasted updated timestamp |

> **Note**: promotion_type is an integer value that represents the type of promotion. The value can be one of the following:
>
> - 1: Percentage
> - 2: Fixed Amount
> - 3: Buy X Get Y Free
> - 4: Buy X Get Y at Z% Off
> - 5: Buy X Get Y at Z% Off (same product)

### Product Schema

| Field    | Type  | Description    |
| ------- | ------- | -------- |
| id | int | The Promotion Id |
| created_at | str | Date the Promotion applies to the product |
| updated_at | Date | Model lasted updated timestamp |

### Promotion - Product Schema

| Field    | Type  | Description    |
| ------- | ------- | -------- |
| promotion_id | int | The Promotion id |
| product_id | int | The Product Id |
| created_at | str | Date the Promotion applies to the product |
| updated_at | Date | Model lasted updated timestamp |

## API Endpoints

### 1. Root URL

- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: A basic endpoint that provides information about the Promotion Demo REST API Service.
- **Response**:
  - `200 OK`: Returns the service name, version, and the URL for listing promotions.

Example Response:

```json
{
    "name": "Promotion Demo REST API Service",
    "version": "1.0",
    "paths": "<URL for listing promotions>"
}
```

---

### 2. Create Promotion

- **Endpoint**: `/promotions`
- **Method**: `POST`
- **Description**: Create a new promotion using the data provided.
- **Request Body**: `JSON`
    > | Field    | Type  | Required  | Des    |
    > | ------- | ------- | -------- | -------- |
    > | code | str | True | The Promotion code |
    > | name | str | True | The Promotion label (description) |
    > | start | date | True | Active date |
    > | expired | date | True | Expired date |
    > | available | int | Code available to use |
    > | whole_store | bool | False (Default to False) | Whether is whole store promotion|
    > | promo_type | int | True | The Promotion type |
    > | value | double | False (Default to 0.0) | Promotion value according to the type |
- **Response**:
  - `201 Created`: Returns the created promotion `JSON`.
    > | Field    | Type  | Des    |
    > | ------- | ------- | -------- |
    > | id | int | The promotion id |
    > | code | str | The Promotion code |
    > | name | str | The Promotion label (description) |
    > | start | date | Active date |
    > | expired | date | Expired date |
    > | available | int | Code available to use |
    > | whole_store | bool | Whether is whole store promotion|
    > | promo_type | int | The Promotion type |
    > | value | Date | Promotion value according to the type |
    > | created_at | str | The Promotion code |
    > | updated_at | Date | Model lasted updated timestamp |
  - `415 Unsupported Media Type`: If the request is not JSON.

---

### 3. Delete Promotion

- **Endpoint**: `/promotions/<int:promotion_id>`
- **Method**: `DELETE`
- **Description**: Delete a specific promotion by its ID.
- **Response**:
  - `404 Not Found`: If the promotion with the given ID doesn't exist.
  - `400 Bad Request`: If the confirmation parameter is missing or false.
  - `204 No Content`: This status is returned regardless of whether the promotion existed or not. The delete operation is idempotent, ensuring consistent behavior.

---

### 4. Update Promotion

- **Endpoint**: `/promotions/<int:promotion_id>`
- **Method**: `PUT`
- **Description**: Update the information of a specific promotion using its ID.
- **Request Body**: `JSON`
    > | Field    | Type  | Required  | Des    |
    > | ------- | ------- | -------- | -------- |
    > | code | str | True | The Promotion code |
    > | name | str | True | The Promotion label (description) |
    > | start | date | True | Active date |
    > | expired | date | True | Expired date |
    > | available | int | Code available to use |
    > | whole_store | bool | False (Default to False) | Whether is whole store promotion|
    > | promo_type | int | True | The Promotion type |
    > | value | double | False (Default to 0.0) | Promotion value according to the type |
- **Response**:
  - `200 OK`: Returns the updated promotion `JSON`.
    > | Field    | Type  | Des    |
    > | ------- | ------- | -------- |
    > | id | int | The promotion id |
    > | code | str | The Promotion code |
    > | name | str | The Promotion label (description) |
    > | start | date | Active date |
    > | expired | date | Expired date |
    > | available | int | Code available to use |
    > | whole_store | bool | Whether is whole store promotion|
    > | promo_type | int | The Promotion type |
    > | value | Date | Promotion value according to the type |
    > | created_at | str | The Promotion code |
    > | updated_at | Date | Model lasted updated timestamp |
  - `404 Not Found`: If the promotion with the given ID doesn't exist.
  - `405 Method Not Allowed`: If the promotion is already expired.
  - `415 Unsupported Media Type`: If the request is not JSON.
  - `400 Bad Request`: For data validation errors.

---

### 5. List All Promotions

- **Endpoint**: `/promotions`
- **Method**: `GET`
- **Description**: Retrieves a list of all promotions with optional filters.
- **Query Parameters**:
  - `name` (optional): Filter promotions by name.
  - `code` (optional): Filter promotions by code.
  - `promo_type` (optional): Filter promotions by type.
- **Response**:
  - `200 OK`: Returns a list of promotions as JSON.

---

### 6. Retrieve a Specific Promotion

- **Endpoint**: `/promotions/<int:promotion_id>`
- **Method**: `GET`
- **Description**: Retrieves the details of a specific promotion using its ID.
- **Response**:
  - `200 OK`: Returns the requested promotion as JSON.
  - `404 Not Found`: If the promotion with the given ID doesn't exist.

---

## Action Routes

### 7. Apply Promotion

- **Endpoint**: `/promotions/<int:promotion_id>/apply`
- **Method**: `POST`
- **Description**: Apply a specific promotion using its ID.
- **Response**:
  - `200 OK`: Returns the requested promotion as JSON.
  - `404 Not Found`: If the promotion with the given ID doesn't exist.
  - `405 Method Not Allowed`: If the promotion is already expired or not available.

### 8. Cancel Promotion

- **Endpoint**: `/promotions/<int:promotion_id>/cancel`
- **Method**: `POST`
- **Description**: Cancel a specific promotion using its ID.
- **Response**:
  - `200 OK`: Returns the requested promotion as JSON.
  - `404 Not Found`: If the promotion with the given ID doesn't exist.

---

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
