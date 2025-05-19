from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    if not data:
        return jsonify({"output": "Error: No JSON data received"}), 400
    
    code = data.get("code", "")
    input_data = data.get("input", "")

    with open("temp_code.py", "w", encoding="utf-8") as f:
        f.write(code)

    try:
        result = subprocess.run(
            ["python", "temp_code.py"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Error: Code execution timed out."

    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)