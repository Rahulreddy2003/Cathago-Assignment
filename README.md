# Cathago-Assignment
# Document Scanning and Matching System

## Overview
This project is a self-contained document scanning and matching system with a built-in credit system. Each user gets 20 free scans per day, and additional scans require admin approval for extra credits. The system allows users to upload plain text documents, scans them for similarity, and provides analytics for administrators.

## Features
### 1. **User Management & Authentication**
- User registration and login.
- User roles: Regular Users & Admins.
- Profile section displaying user credits and scan history.

### 2. **Credit System**
- Each user gets **20 free scans per day** (auto-reset at midnight).
- Users must request credits if they exceed their limit.
- Admins can approve or deny credit requests.
- Each document scan deducts 1 credit.

### 3. **Document Scanning & Matching**
- Users upload a plain text document for scanning.
- System scans and compares it against stored documents.
- Basic text similarity algorithm (Levenshtein distance, word frequency).

### 4. **Smart Analytics Dashboard**
- Tracks the number of scans per user per day.
- Identifies most commonly scanned document topics.
- Displays top users by scans and credit usage.
- Provides credit usage statistics for admins.

## API Endpoints
| Method | Endpoint | Description |
|--------|----------------|----------------------------------------|
| POST   | /auth/register | User registration |
| POST   | /auth/login    | User login |
| GET    | /user/profile  | Get user profile & credits |
| POST   | /scan          | Upload document for scanning (uses 1 credit) |
| GET    | /matches/:docId| Get matching documents |
| POST   | /credits/request | Request admin to add credits |
| POST   | /admin/credits/approve | Approve/deny credit requests |
| GET    | /admin/analytics | Get analytics for admins |

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript (No frameworks)
- **Backend:** Python (Flask) without external libraries
- **Database:** SQLite (or JSON files for small-scale storage)
- **File Storage:** Local storage for documents
- **Authentication:** Basic username-password login (hashed passwords)
- **Text Matching Logic:** Custom algorithm using Levenshtein distance, word frequency

## Setup Instructions
### 1. Install Dependencies
```bash
pip install flask sqlite3
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access API
Use Postman or cURL to test API endpoints.

## Bonus (AI-Powered Matching)
- Optional AI-based document similarity analysis using OpenAI, Gemini, or DeepSeek.
- NLP models like spaCy, BERT, or Llama2 can be integrated.




