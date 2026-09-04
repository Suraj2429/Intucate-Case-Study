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