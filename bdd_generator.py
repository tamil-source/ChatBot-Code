import requests
import os

OLLAMA_API_URL = "http://localhost:11434/api/chat"

def generate_bdd_files(prompt):
    payload = {
        "model": "llama3",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    content = response.json().get("message", {}).get("content", "")

    feature_text = ""
    step_def_text = ""
    inside_feature = False
    inside_steps = False

    for line in content.splitlines():
        if line.strip().startswith("Feature:"):
            inside_feature = True
            inside_steps = False
        elif line.strip().startswith("```js"):
            inside_feature = False
            inside_steps = True
            continue
        elif line.strip().startswith("```"):
            inside_steps = False
            continue

        if inside_feature:
            feature_text += line + "\n"
        elif inside_steps:
            step_def_text += line + "\n"

    os.makedirs("features/steps", exist_ok=True)

    with open("features/chatbot.feature", "w", encoding="utf-8") as f:
        f.write(feature_text.strip())

    with open("features/steps/chatbot.steps.js", "w", encoding="utf-8") as f:
        f.write(step_def_text.strip())

    return {"status": "success", "message": "BDD files generated."}
