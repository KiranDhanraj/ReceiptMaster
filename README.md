# Receipt Analytics Platform

A full-stack receipt processing and analytics platform that allows users to:

* Create accounts and authenticate securely
* Upload scanned Walmart receipts/images
* Extract OCR text from receipts
* Detect and process barcodes
* Store structured receipt/product data in PostgreSQL
* Visualize analytics in Power BI
Visit the vercel app: https://receipt-master-nu.vercel.app/

---

# Features

## Authentication

* User registration
* Secure password hashing
* JWT authentication
* Protected API routes

## Receipt Processing

* Upload receipt images
* OCR text extraction using Tesseract
* Barcode extraction and processing
* Product categorization and metadata extraction

## Database Storage

* Store users
* Store receipt OCR text
* Store barcode/product data
* Relational PostgreSQL schema

## Analytics

* Product/category trends
* Upload statistics
* Brand analytics

---
# Example Receipt Processing

## Demo
After uploading a receipt:
![Example Walmart Receipt](receipt2.jpg)

It gets processed and the data from the receipt can be viewed on the Dashboard:
![Dashboard](Dashboard_Example.png)


# Tech Stack

## Frontend

* React
* TypeScript
* Axios
* Vite

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* JWT Authentication

## Database

* PostgreSQL

## OCR / Image Processing

* Tesseract OCR
* Pillow
* OpenCV

## Analytics


## Deployment

* Render (backend)
* Vercel (frontend)
* [PostgreSQL](https://receipt-master-nu.vercel.app/) 

---

# Project Architecture

```text
React + TypeScript Frontend
            ↓
FastAPI Backend
            ↓
PostgreSQL Database
            ↓
Power BI Dashboards
```

---

# Database Design

## Users Table

Stores user authentication information.

| Column   | Type    |
| -------- | ------- |
| id       | Integer |
| username | String  |
| email    | String  |
| password | String  |

---

## Receipts Table

Stores uploaded receipt OCR data.

| Column     | Type        |
| ---------- | ----------- |
| id         | Integer     |
| user_id    | Foreign Key |
| ocr_text   | Text        |
| created_at | DateTime    |

---

## Receipt Items Table

Stores barcode/product information extracted from receipts.

| Column      | Type        |
| ----------- | ----------- |
| id          | Integer     |
| receipt_id  | Foreign Key |
| barcode     | String      |
| category    | String      |
| brand       | String      |
| description | String      |

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

---

# Backend Setup

## 2. Navigate to Backend

```bash
cd backend
```

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Create Environment Variables

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=postgresql://postgres:password@localhost/receipt_app
JWT_SECRET=your_secret_key
```

---

## 6. Run Backend Server

```bash
uvicorn main:app --reload
```

Backend will run on:

```text
http://127.0.0.1:8000
```

FastAPI Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

## 7. Navigate to Frontend

```bash
cd frontend
```

## 8. Install Dependencies

```bash
npm install
```

## 9. Run Frontend

```bash
npm run dev
```

Frontend will run on:

```text
http://localhost:5173
```

---

# PostgreSQL Setup

## 10. Install PostgreSQL

Download PostgreSQL:

[https://www.postgresql.org/download/](https://www.postgresql.org/download/)

Optional database GUI:

* pgAdmin
* DBeaver

---

## 11. Create Database

```sql
CREATE DATABASE receipt_app;
```

---

# OCR Setup

## 12. Install Tesseract OCR

Download:

[https://tesseract-ocr.github.io/](https://tesseract-ocr.github.io/)

Make sure Tesseract is added to PATH.

---

# API Endpoints

## Authentication

| Method | Endpoint  | Description   |
| ------ | --------- | ------------- |
| POST   | /register | Register user |
| POST   | /login    | Login user    |

---

## Receipt Processing

| Method | Endpoint  | Description          |
| ------ | --------- | -------------------- |
| POST   | /upload   | Upload receipt image |
| GET    | /receipts | Get user receipts    |

---



## Example OCR + Barcode Processing Flow

```text
User uploads receipt image
↓
FastAPI processes image
↓
OCR extracts text
↓
Barcode data extracted
↓
Structured data stored in PostgreSQL
↓
Power BI visualizes analytics
```

---


# Example Upload Flow

```text
User uploads receipt image
↓
FastAPI processes image
↓
OCR extracts text
↓
Barcode data extracted
↓
Structured data stored in PostgreSQL
↓
Power BI visualizes analytics
```

---

# Example Barcode Data

```json
{
  "barcode": "0123456789",
  "category": "Snacks",
  "brand": "Lays",
  "name : Lays Classic Potato Chips"
  "price : 3.00
  "description": "Classic Potato Chips"

}
```

---

# Security Features

* JWT authentication
* Protected routes
* Environment variable configuration
* Secure database credentials

---

# Future Improvements

* More Extensive Barcode Lookup
* Better UI
* Receipt categorization AI
* Better OCR preprocessing
* Admin dashboard
* User analytics
* Real-time processing

---

# Libraries Used

## Backend Python Libraries

| Library          | Purpose                  |
| ---------------- | ------------------------ |
| fastapi          | Backend framework        |
| uvicorn          | ASGI server              |
| sqlalchemy       | ORM/database layer       |
| psycopg2-binary  | PostgreSQL driver        |
| asyncpg          | Async PostgreSQL support |
| python-multipart | File uploads             |
| python-jose      | JWT handling             |
| passlib          | Password hashing         |
| bcrypt           | Password encryption      |
| pillow           | Image processing         |
| pytesseract      | OCR                      |
| opencv-python    | Computer vision          |
| pydantic         | Data validation          |
| python-dotenv    | Environment variables    |
| alembic          | Database migrations      |
| httpx            | HTTP requests            |

---

## Frontend Libraries

| Library    | Purpose            |
| ---------- | ------------------ |
| react      | Frontend framework |
| typescript | Type safety        |
| axios      | API requests       |
| vite       | Frontend tooling   |

---

# Deployment

## Frontend

* Vercel

## Backend

* Render

## Database

* PostgreSQL cloud hosting
* Supabase
* Neon

---

# Learning Goals

This project demonstrates:

* Full-stack web development
* REST API development
* Authentication systems
* OCR/image processing
* Relational database design
* PostgreSQL integration
* Analytics engineering
* Power BI dashboarding
* FastAPI backend development

---

# License

This project is licensed under the MIT License.
