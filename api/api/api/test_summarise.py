import requests

url = "http://localhost:5000/summarize"
payload = {
    "text": "This is the text you want to summarize.",
    "provider": "openai"
}

response = requests.post(url, json=payload)
print(response.json())

