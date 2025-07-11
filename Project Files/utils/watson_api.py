import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
BASE_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-13b-instruct-v2"   



def get_access_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_ai_response(prompt):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "sample",
             "temperature": 0.7,              # add creativity but stay grounded
    "top_k": 40,
    "top_p": 0.95,
            "max_new_tokens": 300
        },
        "project_id": PROJECT_ID
    }

    url = f"{BASE_URL}/ml/v1/text/generation?version=2024-05-01"

    print("\n📤 REQUEST PAYLOAD:")
    print(json.dumps(payload, indent=2))
    print("\n🔗 URL:", url)

    try:
        response = requests.post(url, headers=headers, json=payload)
        print("\n📥 RAW RESPONSE:")
        print(response.text)
        response.raise_for_status()
        return response.json()["results"][0]["generated_text"]
    except requests.exceptions.HTTPError as err:
        return f"\n❌ HTTP Error: {err}\nStatus: {response.status_code}\nDetails: {response.text}"
    except Exception as e:
        return f"\n❌ Other Error: {str(e)}"
