from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection
from chatbot import get_response

app = Flask(__name__)

app.secret_key = "healthcare_chatbot_secret_key"


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("chat"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (name, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, hashed_password)
            )

            connection.commit()

        except Exception:

            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
                "register.html",
                error="Email already exists."
            )

        cursor.close()
        connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["user_id"]
            session["name"] = user["name"]

            return redirect(url_for("chat"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


@app.route("/chat")
def chat():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT user_message, bot_response, created_at
        FROM chat_history
        WHERE user_id = %s
        ORDER BY created_at ASC
        """,
        (session["user_id"],)
    )

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "chat.html",
        name=session["name"],
        history=history
    )


@app.route("/send_message", methods=["POST"])
def send_message():

    if "user_id" not in session:
        return jsonify(
            {"error": "Please login first."}
        ), 401

    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify(
            {"error": "Message cannot be empty."}
        ), 400

    response = get_response(message)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (user_id, user_message, bot_response)
        VALUES (%s, %s, %s)
        """,
        (
            session["user_id"],
            message,
            response
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify(
        {"response": response}
    )


@app.route("/book_appointment", methods=["GET", "POST"])
def book_appointment():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        doctor_id = request.form["doctor_id"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]

        cursor.execute(
            """
            INSERT INTO appointments
            (user_id, doctor_id, appointment_date, appointment_time)
            VALUES (%s, %s, %s, %s)
            """,
            (
                session["user_id"],
                doctor_id,
                appointment_date,
                appointment_time
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("appointments"))

    cursor.execute(
        """
        SELECT doctor_id, doctor_name, specialization
        FROM doctors
        ORDER BY doctor_name
        """
    )

    doctors = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "book_appointment.html",
        doctors=doctors
    )


@app.route("/appointments")
def appointments():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            appointments.appointment_id,
            doctors.doctor_name,
            doctors.specialization,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status
        FROM appointments
        JOIN doctors
        ON appointments.doctor_id = doctors.doctor_id
        WHERE appointments.user_id = %s
        ORDER BY
            appointments.appointment_date,
            appointments.appointment_time
        """,
        (session["user_id"],)
    )

    appointments_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "appointments.html",
        appointments=appointments_data
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)