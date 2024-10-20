from flask import Flask, request, jsonify
import os
from openai import AzureOpenAI

app = Flask(__name__)

client = AzureOpenAI(
  azure_endpoint = "https://keisuke-openai.openai.azure.com/", 
  api_key=os.getenv("OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

@app.route('/classify', methods=['POST'])
def classify_message():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    message = data['message']

    try:
        response = client.chat.completions.create(
            # Updated parameter: use 'deployment_id' instead of 'engine'
            model="gpt4o-global",  # Replace with your deployment name
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that classifies messages into 'business' or 'private'. Respond only with the category name."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=5,
            temperature=0
        )
        category = response.choices[0].message.content.strip().lower()
        if category not in ['business', 'private']:
            category = 'unknown'
        return jsonify({'category': category})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
