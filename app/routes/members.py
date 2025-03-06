from flask import request, jsonify, Blueprint
from helpers.helper import *
import datetime as dt
import uuid

members = Blueprint('members', __name__)


@members.route('/create', methods=['POST'])
def create_member():
    """
    API endpoint for creating a new member.
    """
    try:
        # Get the database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get required form fields
        required_fields = [
            "first_names", "last_names", "gender_id", "date_of_birth", "address",
            "is_baptized", "is_born_again", "foundation_school_status_id", "joined_on",
            "professional_status_id", "emergency_contact_name", "emergency_contact_phone",
            "emergency_contact_relation_id"
        ]

        form_data = {}
        for field in required_fields:
            value = request.form.get(field)
            if value is None or value.strip() == "":
                return jsonify({"status": "Error", "message": f"Missing required field: {field}"}), 400
            form_data[field] = value

        # Convert necessary fields
        form_data["gender_id"] = int(form_data["gender_id"])
        form_data["date_of_birth"] = dt.datetime.strptime(form_data["date_of_birth"], "%Y-%m-%d").date()
        form_data["joined_on"] = dt.datetime.strptime(form_data["joined_on"], "%Y-%m-%d").date()
        form_data["foundation_school_status_id"] = int(form_data["foundation_school_status_id"])
        form_data["professional_status_id"] = int(form_data["professional_status_id"])
        form_data["emergency_contact_relation_id"] = int(form_data["emergency_contact_relation_id"])

        # Get optional fields
        optional_fields = [
            "phone_number", "whatsapp_number", "email", "school_name", "occupation",
            "cell_id", "department_id", "fellowship_center_id", "emergency_contact_whatsapp"
        ]
        for field in optional_fields:
            form_data[field] = request.form.get(field) or None

        # Convert optional integer fields
        for int_field in ["cell_id", "department_id", "fellowship_center_id"]:
            if form_data[int_field]:
                form_data[int_field] = int(form_data[int_field])

        # Handle file upload
        if 'profile_photo' not in request.files or request.files['profile_photo'].filename == '':
            return jsonify({"status": "Error", "message": "Missing required field: profile_photo"}), 400

        profile_photo = request.files['profile_photo']
        if not allowed_file(profile_photo.filename):
            return jsonify({"status": "Error", "message": "Invalid image type"}), 400

        profile_photo_data = profile_photo.read()

        # Generate timestamps
        created_on = dt.datetime.now()
        last_updated = dt.datetime.now()

        # Generate UUID for ID
        member_id = str(uuid.uuid4())

        # Insert into the database
        cursor.execute("""
            INSERT INTO members (
                id, first_names, last_names, phone_number, whatsapp_number, email, gender_id, 
                date_of_birth, address, is_baptized, is_born_again, cell_id, fellowship_center_id, 
                department_id, foundation_school_status_id, joined_on, professional_status_id, 
                occupation, school_name, emergency_contact_name, emergency_contact_relation_id, 
                emergency_contact_phone, emergency_contact_whatsapp, profile_photo, created_on, last_updated
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            member_id, form_data["first_names"], form_data["last_names"], form_data["phone_number"],
            form_data["whatsapp_number"], form_data["email"], form_data["gender_id"],
            form_data["date_of_birth"], form_data["address"], form_data["is_baptized"],
            form_data["is_born_again"], form_data["cell_id"], form_data["fellowship_center_id"],
            form_data["department_id"], form_data["foundation_school_status_id"], form_data["joined_on"],
            form_data["professional_status_id"], form_data["occupation"], form_data["school_name"],
            form_data["emergency_contact_name"], form_data["emergency_contact_relation_id"],
            form_data["emergency_contact_phone"], form_data["emergency_contact_whatsapp"],
            profile_photo_data, created_on, last_updated
        ))

        # Commit and close connection
        close_db_connection()

        return jsonify({"status": "Success", "message": "Member successfully created"}), 201

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500
