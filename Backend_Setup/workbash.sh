#run each one time
python app.py

curl -X POST http://127.0.0.1:5000/auth/register -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "securepassword"}'

curl -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "securepassword"}'

{"access_token": "your_jwt_token_here"}

