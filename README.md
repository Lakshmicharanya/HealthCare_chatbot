# Healthcare Chatbot

## 📌 Project Overview

The **Healthcare Chatbot** is a web-based application developed using **Python and Flask**. It helps users get basic health-related suggestions based on the symptoms they enter.

The application provides a simple interface where users can register, log in, enter symptoms, and receive predefined health recommendations.

## 🚀 Features

* User Registration and Login
* Secure user authentication
* Symptom-based health recommendations
* Chat interface for interacting with the chatbot
* Stores user information and chat history
* MySQL database integration
* Simple and responsive web interface
* Input validation and error handling

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **HTML5**
* **CSS3**
* **JavaScript**
* **MySQL**
* **Git & GitHub**

## 📂 Project Structure

```text
HealthCare_chatbot/
│
├── app.py
├── database.py
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── chat.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md
```

## ⚙️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Lakshmicharanya/HealthCare_chatbot.git
```

### 2. Open the project folder

```bash
cd HealthCare_chatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 5. Install the required packages

```bash
pip install -r requirements.txt
```

### 6. Configure MySQL

Create the required MySQL database and update the database connection details in the project configuration.

### 7. Run the application

```bash
python app.py
```

### 8. Open in browser

```text
http://127.0.0.1:5000
```

## 🔄 Application Flow

```text
Register
   ↓
Login
   ↓
Chat Interface
   ↓
Enter Symptoms
   ↓
Process Symptoms
   ↓
Display Health Recommendation
```

## 🎯 Purpose

The main purpose of this project is to demonstrate the development of a **Python Flask web application** with user authentication, database integration, and a symptom-based chatbot interface.

## ⚠️ Disclaimer

This application is intended for **educational purposes only**. The recommendations provided by the chatbot should not be considered professional medical advice. Users should consult qualified healthcare professionals for medical diagnosis and treatment.

## 👩‍💻 Developed By

**Lakshmi Charanya**

B.Tech – Artificial Intelligence and Data Science
