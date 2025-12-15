"""
Simple Groq LLM connectivity test.
Sends a tiny prompt to the configured Groq LLM and prints the response.
"""
import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    from groq import Groq
except Exception as e:
    print(f"ERROR: could not import groq SDK: {e}")
    sys.exit(2)

API_KEY = os.getenv('GROQ_API_KEY')
if not API_KEY:
    print('ERROR: GROQ_API_KEY not set in environment (.env).')
    sys.exit(2)

client = Groq(api_key=API_KEY)

prompt = (
    "You are a helpful assistant. Return a JSON object with a field 'ping' set to 'pong', "
    "and a field 'note' with a short message. Keep it minimal."
)

try:
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {"role": "system", "content": "You are a compact JSON responder."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=60
    )

    # Extract content
    content = resp.choices[0].message.content.strip()
    print('=== RAW RESPONSE ===')
    print(content)
    print('\n=== ATTEMPT PARSE AS JSON ===')

    # Try parsing JSON from the output
    parsed = None
    try:
        # If the model returned a fenced block, remove backticks
        if content.startswith('```'):
            content = '\n'.join(content.split('\n')[1:-1])
        parsed = json.loads(content)
        print(json.dumps(parsed, indent=2))
        sys.exit(0)
    except Exception:
        print('Could not parse response as JSON. Raw output above.')
        sys.exit(1)

except Exception as exc:
    print(f'ERROR: chat completion failed: {exc}')
    sys.exit(3)
