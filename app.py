@app.get("/")
def home():
    return render_template(
        "index.html",
        assistant_name=load_name()
    )

@app.get("/api/health")
def health():
    return jsonify({
        "status": "success",
        "message": "EduGenie backend is running"
    })
