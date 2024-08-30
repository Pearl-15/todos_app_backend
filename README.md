# ToDo Application Backend

## Overview
This backend system supports the ToDo application, providing essential functionalities for managing to-do items. It leverages AWS Lambda functions, DynamoDB, and API Gateway, with authentication managed through AWS Cognito.

## Technological Stack
- **Serverless Framework:** Facilitates deployment and management of AWS resources.
- **AWS Lambda (Python):** Executes backend logic.
- **DynamoDB:** Stores to-do items.
- **API Gateway:** Exposes RESTful HTTP endpoints.
- **AWS Cognito:** Handles user authentication.

## Endpoints

### 1. Get To-Do Item
- **Endpoint:** `GET /todos/{id}`
- **Description:** Retrieves a to-do item by its ID.
- **Function:** `get`
- **Handler:** `todos/get.get`

### 2. Create To-Do Item
- **Endpoint:** `POST /create`
- **Description:** Creates a new to-do item with the specified date, title, and content.
- **Function:** `create`
- **Handler:** `todos/create.create`

### 3. List To-Do Items
- **Endpoint:** `GET /list`
- **Description:** Lists all to-do items.
- **Function:** `list`
- **Handler:** `todos/list.list`

### 4. Update To-Do Item
- **Endpoint:** `PUT /todos/{id}`
- **Description:** Updates an existing to-do item identified by its ID. Allows modification of title, content, and date.
- **Function:** `update`
- **Handler:** `todos/update.update`

### 5. Delete To-Do Item
- **Endpoint:** `DELETE /todos/{id}`
- **Description:** Deletes a to-do item by its ID.
- **Function:** `delete`
- **Handler:** `todos/delete.delete`

## Authentication
- **AWS Cognito:** Secures the API endpoints. All requests require a valid Cognito token for access. The token is verified using the `CognitoAuthorizer`.

## Resources

### DynamoDB Table
- **Table Name:** `TODOTABLE`
- **Primary Key:**
  - **Partition Key:** `user_id` (String)
  - **Sort Key:** `id` (String)

### Cognito User Pool
- **User Pool Name:** `TodoUserPool`
- **Attributes:**
  - **Username:** Email
  - **Auto-Verified Attributes:** Email

### Cognito User Pool Client
- **Client Name:** `TodoUserPoolClient`
- **Auth Flows:** Admin authentication without SRP (Secure Remote Password)

## Deployment
- **Serverless Framework:** Manages deployment and updates of AWS Lambda functions, API Gateway, and DynamoDB table.

## Local Development
1. **Install Dependencies:**
   ```bash
   npm install -g serverless
