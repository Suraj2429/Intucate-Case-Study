# AI Prompt Processing API

A Flask-based backend application that accepts user inputs, retrieves prompt templates from MongoDB, sends the processed prompts to an AI API, and stores the request and response history in MongoDB.

The application supports both single user inputs and batch processing of multiple user inputs asynchronously.

---

## Features

- Flask REST API
- MongoDB database integration using PyMongo
- Prompt templates stored in MongoDB
- Dynamic replacement of `{{userInput}}`
- AI API integration using Gemini
- Request and response history stored in MongoDB
- Single input processing
- Batch input processing
- Asynchronous processing for batch requests
- JSON request and response format
- Environment variables for API credentials

---

## Technology Stack

- Python
- Flask
- MongoDB
- PyMongo
- Gemini API
- OpenAI Python SDK
- python-dotenv
- asyncio

---

## Project Structure

```text
Case Study/
│
├── app.py
├── check_models.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The .env file contains the API key and must not be shared publicly or committed to Git.

---

## Prerequisites

Before running the project, make sure the following are installed:

- Python 3.x
- MongoDB
- Postman
- Gemini API key

---

## Installation

1. Open the project directory
```bash
cd "D:\Case Study"
```

2. Create a virtual environment
```bash
python -m venv venv
```

3. Activate the virtual environment
For Windows:
```bash
venv\Scripts\activate
```

4. Install the required dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a ```.env``` file in the project root directory.

Add the following:
```bash
GEMINI_API_KEY=your_api_key_here
```

The application loads the API key using ```python-dotenv```.

The ```.env``` file is excluded from version control using ```.gitignore```.

---

## MongoDB Configuration

The application uses MongoDB as its database.

MongoDB connection:
```bash
mongodb://localhost:27017/
```

Database:
```bash
case_study
```

Collections:

```text
case_study
│
├── prompts
└── history
```

---

## Prompts Collection

The ```prompts`` collection stores the prompt template used by the application.

Example document:
```bash
{
  "_id": "Education_Prompt",
  "template": "You are an expert in education domain. Answer the following: {{userInput}}"
}
```

The application retrieves this template from MongoDB and replaces:
```bash
{{userInput}}
```

with the user input received through the API.

For example, if the user sends:
```bash
What is Java?
``` 

the final prompt becomes:
```bash
You are an expert in education domain. Answer the following: What is Java?
```

--- 

## API Endpoints
# 1. Single Input API

Endpoint
```bash
POST /chat
``` 

URL
```bash
http://127.0.0.1:5000/chat
```

Request Body
```bash
{
  "userInput": "How much should I score in each subject to pass CA final?"
}
``` 
Processing

The ```/chat``` endpoint performs the following steps:

- Receives the user input.
- Fetches the prompt template from the MongoDB ```prompts``` collection.
- Replaces ```{{userInput}}``` with the received user input.
- Sends the final prompt to the Gemini API.
- Receives the AI-generated response.
- Stores the user input, final prompt, and response in the MongoDB history collection.
- Returns the AI response as JSON.

Response
```bash
{
  "response": "AI generated response..."
}
```

History Collection

The ```history``` collection stores the request and response information.

Example document:
```bash
{
  "_id": "ObjectId(...)",
  "userInput": "What is Java?",
  "prompt": "You are an expert in education domain. Answer the following: What is Java?",
  "response": "AI generated response..."
}
```

Each successfully processed request is stored in this collection.

# 2. Batch Input API

The batch endpoint accepts multiple user inputs in a single request.

Endpoint
```bash
POST /chat/batch
```

URL
```bash
http://127.0.0.1:5000/chat/batch
```

Request Body
```bash
{
  "userInputs": [
    "What is Java?",
    "What is MongoDB?",
    "What is Flask?"
  ]
}
```

Processing

The ```/chat/batch``` endpoint performs the following steps:

- Receives a list of user inputs.
- Fetches the prompt template from MongoDB.
- Creates a separate prompt for each input.
- Sends the AI requests asynchronously.
- Processes multiple inputs concurrently.
- Waits for all AI requests to complete.
- Stores the processed request and response information in MongoDB.
- Returns the AI responses in the same order as the input list.

Response
```bash
{
  "responses": [
    "Response for What is Java?",
    "Response for What is MongoDB?",
    "Response for What is Flask?"
  ]
}
```

The order of the responses corresponds to the order of the inputs provided in the request.