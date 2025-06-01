from flask import Flask, render_template, request, jsonify
from bdd_generator import generate_bdd_files
import requests

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/chat"

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No input message provided"}), 400

    conversation_history.append({"role": "user", "content": user_input})

    payload = {
        "model": "llama3",
        "messages": conversation_history,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result.get("message", {}).get("content", "")
        conversation_history.append({"role": "assistant", "content": answer})
        return jsonify({"response": answer})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-bdd", methods=["POST"])
def generate_bdd():
    test_prompt = request.json.get("prompt", "")
    if not test_prompt:
        return jsonify({"error": "No BDD prompt provided"}), 400

    try:
        result = generate_bdd_files(test_prompt)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

#  from flask import Flask, render_template, request, jsonify
# from langchain_community.llms.ollama import Ollama as OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate

# app = Flask(__name__)  

# # LangChain setup
# template = """
# Answer the question below.

# Here is the conversation history: {context}

# Question: {question}

# Answer:
# """
# model = OllamaLLM(model="llama3")
# prompt = ChatPromptTemplate.from_template(template)
# chain = prompt | model

# # Store context in memory (for demo purpose)
# conversation_context = ""

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     global conversation_context
#     user_input = request.json.get("message", "")
#     if not user_input:
#         return jsonify({"error": "No input message provided"}), 400

#     result = chain.invoke({"context": conversation_context, "question": user_input})
    
#     print("Model result:", result)

#     conversation_context += f"\nUser: {user_input}\nAI: {result}"
#     return jsonify({"response": str(result)})

# if __name__ == "__main__":
#     app.run(debug=True)
