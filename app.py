from flask import Flask, request
from pymongo import MongoClient
from dotenv import load_dotenv
from openai import OpenAI
import os
import asyncio

# Load environment variables and create Gemini API client
load_dotenv()
openai_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["case_study"]

@app.route("/")
def home():
    return {"message": "Server is running"}

# Endpoint to handle single user input and return AI response
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("userInput")

    # Fetch prompt from MongoDB and replace the user input
    prompt = db.prompts.find_one({"_id": "Education_Prompt"})
    template = prompt["template"]
    final_prompt = template.replace("{{userInput}}", user_input)
    response = openai_client.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    )
    response_text = response.choices[0].message.content

    # Store request and response in history
    db.history.insert_one({
        "userInput": user_input,
        "prompt": final_prompt,
        "response": response_text
    })

    return {
        "response": response_text
    }

# Endpoint to handle batch user inputs and return AI responses
@app.route("/chat/batch", methods=["POST"])
def chat_batch():
    data = request.get_json()
    user_inputs = data.get("userInputs")

    # Fetch the prompt template once for all inputs
    prompt = db.prompts.find_one({"_id": "Education_Prompt"})
    template = prompt["template"]
    async def get_response(user_input):
        final_prompt = template.replace("{{userInput}}", user_input)

        # Run blocking AI calls asynchronously
        response = await asyncio.to_thread(
            openai_client.chat.completions.create,
            model="gemini-3.6-flash",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )
        response_text = response.choices[0].message.content

        return {
            "userInput": user_input,
            "prompt": final_prompt,
            "response": response_text
        }

    async def process_all():
        tasks = [get_response(user_input) for user_input in user_inputs]
        return await asyncio.gather(*tasks)
    history_records = asyncio.run(process_all())

    # Store all batch results in history
    db.history.insert_many(history_records)

    return {
        "responses": [record["response"] for record in history_records]
    }

if __name__ == "__main__":
    app.run(debug=False)