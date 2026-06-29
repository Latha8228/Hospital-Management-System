from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("HOSP_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/ADMIN/<path:filename>")
def admin_files(filename):
    return send_from_directory("ADMIN", filename)

@app.route("/<path:filename>")
def user_files(filename):
    return send_from_directory(".", filename)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        response = model.generate_content(
            f"""
You are an AI Hospital Assistant. provide better answers for hospital relared any queries.
Answer hospital-related questions, medical or medicines related questions and remedies and suggestions for curing .
If not related to hospital or above mentioned , say you can help only with hospital queries or medical purpose .

User question: {user_message}
"""
        )
        return jsonify({"reply": response.text})
    except:
        return jsonify({"reply": "Error processing request"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
