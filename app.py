from flask import Flask, request
from pymongo import MongoClient
from dotenv import load_dotenv
from openai import OpenAI
import os
import asyncio

load_dotenv()
openai_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["case_study"]

@app.route("/")
def home():
    return {"message": "Server is running"}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("userInput")
    prompt = db.prompts.find_one({"_id": "Education_Prompt"})
    template = prompt["template"]
    final_prompt = template.replace("{{userInput}}", user_input)
    response = openai_client.chat.completions.create(
        model="gemini-3.7-flash",
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    )
    response_text = response.choices[0].message.content
    db.history.insert_one({
        "userInput": user_input,
        "prompt": final_prompt,
        "response": response_text
    })

    return {
        "response": response_text
    }

@app.route("/chat/batch", methods=["POST"])
def chat_batch():
    data = request.get_json()
    user_inputs = data.get("userInputs")
    prompt = db.prompts.find_one({"_id": "Education_Prompt"})
    template = prompt["template"]

    async def get_response(user_input):
        final_prompt = template.replace("{{userInput}}", user_input)
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
    db.history.insert_many(history_records)

    return {
        "responses": [record["response"] for record in history_records]
    }

if __name__ == "__main__":
    app.run(debug=True)