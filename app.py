import os
from flask import Flask, render_template, request, jsonify
from Edugenie import process_command, load_name

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

@app.get("/")
def home():
    return render_template("index.html", assistant_name=load_name())

@app.get("/api/health")
def health():
    return jsonify({"status": "success", "message": "EduGenie backend is running"})

@app.post("/api/command")
def command():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "response": "Send a valid JSON request."}), 400
    user_command = data.get("command", "")
    if not isinstance(user_command, str) or not user_command.strip():
        return jsonify({"status": "error", "response": "Please enter a command."}), 400
    if len(user_command) > 500:
        return jsonify({"status": "error", "response": "Command is too long (maximum 500 characters)."}), 400
    try:
        return jsonify(process_command(user_command))
    except Exception:
        app.logger.exception("Command failed")
        return jsonify({"status": "error", "response": "Something went wrong. Please try again."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
