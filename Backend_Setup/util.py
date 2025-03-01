@app.route("/user/profile", methods=["GET"])
@jwt_required()
def profile():
    username = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role, credits FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"username": user["username"], "role": user["role"], "credits": user["credits"]})
    else:
        return jsonify({"error": "User not found"}), 404
