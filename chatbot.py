from database import get_connection

def get_response(message):
    message = message.lower().strip()

    emergency_words = [
        "chest pain",
        "difficulty breathing",
        "can't breathe",
        "cannot breathe",
        "severe bleeding",
        "unconscious",
        "stroke",
        "heart attack"
    ]

    for word in emergency_words:
        if word in message:
            return (
                "This may be an emergency. Please seek immediate medical "
                "attention or contact your local emergency services."
            )

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT symptom_id, symptom_name, response FROM symptoms"
    )

    symptoms = cursor.fetchall()

    matched_symptoms = []

    for symptom in symptoms:
        if symptom["symptom_name"].lower() in message:
            matched_symptoms.append(symptom)

    if not matched_symptoms:
        cursor.close()
        connection.close()

        return (
            "I could not identify that symptom. Please describe your "
            "symptoms clearly. For concerning or persistent symptoms, "
            "please consult a healthcare professional."
        )

    responses = []
    symptom_names = []

    for symptom in matched_symptoms:
        responses.append(symptom["response"])
        symptom_names.append(symptom["symptom_name"])

    placeholders = ",".join(["%s"] * len(symptom_names))

    cursor.execute(
        f"""
        SELECT doctor_id, doctor_name, specialization, phone, symptom
        FROM doctors
        WHERE symptom IN ({placeholders})
        """,
        tuple(symptom_names)
    )

    doctors = cursor.fetchall()

    cursor.close()
    connection.close()

    result = " ".join(responses)

    if doctors:
        result += "\n\nRecommended Doctors for Appointment:\n"

        for doctor in doctors:
            result += (
                f"\nDr. {doctor['doctor_name']}\n"
                f"Specialization: {doctor['specialization']}\n"
                f"Phone: {doctor['phone']}\n"
            )

        result += (
            "\nYou can book an appointment from the "
            "Book Appointment option."
        )

    return result