import requests
import json

prompt = """
Act as a Senior Planning Engineer's Executive Assistant. 
Generate a professional email draft responding to this:
FROM: Client_X <client@example.com>
SUBJECT: Urgent: Need Schedule Update for Phase 2
BODY: Hi Tahir,

We need an urgent update on the Primavera schedule for Phase 2 of the project. Can you please provide an estimated completion date for the FEED verification?

Regards,
Client X

Style: Professional, Concise, Executive.
Sign-off: Tahir Yamin, PMP | Senior Planning Engineer.
Rule: Mention that this is an automated draft flagged for senior review.
"""

print("Sending request to Ollama...")
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:3b-small",
        "prompt": prompt,
        "stream": False
    }
)
print("Response received:")
print(response.json().get("response"))
