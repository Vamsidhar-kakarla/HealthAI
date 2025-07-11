from utils.watson_api import get_ai_response

prompt = "What are the symptoms of high blood pressure?"
response = get_ai_response(prompt)
print(response)
