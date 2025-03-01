from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import difflib

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def reset_credits():
    """ Resets user credits to 20 every midnight """
    conn = get_db_connection()
    conn.execute("UPDATE users SET credits = 20 WHERE credits < 20")
    conn.commit()
    conn.close()

@app.route("/user/profile", methods=["GET"])
def get_user_profile():
    username = request.args.get("username")
    conn = get_db_connection()
    user = conn.execute("SELECT username, credits FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user:
        return jsonify({"username": user["username"], "credits": user["credits"]})
    return jsonify({"error": "User not found"}), 404

@app.route("/scan", methods=["POST"])
def scan_document():
    username = request.json.get("username")
    content = request.json.get("content")
    conn = get_db_connection()
    user = conn.execute("SELECT credits FROM users WHERE username = ?", (username,)).fetchone()
    if user and user["credits"] > 0:
        # Deduct credit
        conn.execute("UPDATE users SET credits = credits - 1 WHERE username = ?", (username,))
        conn.commit()
        
        # Store uploaded document
        conn.execute("INSERT INTO documents (username, content) VALUES (?, ?)", (username, content))
        conn.commit()
        
        # Retrieve stored documents and match similarity
        stored_docs = conn.execute("SELECT content FROM documents").fetchall()
        matches = []
        for doc in stored_docs:
            similarity = difflib.SequenceMatcher(None, content, doc["content"]).ratio()
            if similarity > 0.6:
                matches.append({"match": doc["content"], "similarity": similarity})
        
        # Log scan activity
        conn.execute("INSERT INTO scan_logs (username, scan_time) VALUES (?, ?)", (username, datetime.now()))
        conn.commit()
        
        conn.close()
        return jsonify({"message": "Scan successful, 1 credit deducted.", "matches": matches})
    
    conn.close()
    return jsonify({"error": "Insufficient credits."}), 403

@app.route("/credits/request", methods=["POST"])
def request_credits():
    username = request.json.get("username")
    conn = get_db_connection()
    conn.execute("INSERT INTO credit_requests (username, status) VALUES (?, 'pending')", (username,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Credit request submitted."})

@app.route("/admin/credits/approve", methods=["POST"])
def approve_credits():
    data = request.json
    username = data.get("username")
    approve = data.get("approve")
    conn = get_db_connection()
    if approve:
        conn.execute("UPDATE users SET credits = credits + 10 WHERE username = ?", (username,))
        conn.execute("UPDATE credit_requests SET status = 'approved' WHERE username = ?", (username,))
    else:
        conn.execute("UPDATE credit_requests SET status = 'denied' WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Request processed."})

@app.route("/admin/analytics", methods=["GET"])
def get_analytics():
    conn = get_db_connection()
    scan_counts = conn.execute("SELECT username, COUNT(*) as scan_count FROM scan_logs GROUP BY username ORDER BY scan_count DESC").fetchall()
    top_users = [{"username": row["username"], "scans": row["scan_count"]} for row in scan_counts]
    
    common_topics = conn.execute("SELECT content, COUNT(*) as count FROM documents GROUP BY content ORDER BY count DESC LIMIT 5").fetchall()
    top_topics = [{"topic": row["content"], "count": row["count"]} for row in common_topics]
    
    credit_usage = conn.execute("SELECT username, SUM(credits) as total_used FROM users GROUP BY username ORDER BY total_used DESC").fetchall()
    credit_stats = [{"username": row["username"], "credits_used": row["total_used"]} for row in credit_usage]
    
    conn.close()
    return jsonify({"top_users": top_users, "common_topics": top_topics, "credit_stats": credit_stats})

@app.route("/test", methods=["GET"])
def test_system():
    """ Basic system check endpoint """
    return jsonify({"status": "System is running properly"})

if __name__ == "__main__":
    app.run(debug=True)
