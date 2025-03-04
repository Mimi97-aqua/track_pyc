from flask import request, jsonify, Blueprint
from helpers.helper import *
import datetime

members = Blueprint('members', __name__)

conn = get_db_connection()
cursor = conn.cursor()

@members.route('/create', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE', 'OPTIONS'])
def create_members():
    """
    API endpoint for creating a new member and storing their details in the db.

    Expected form data:
        - first_names (string): Member's first name(s) - REQUIRED
        - last_names (string): Member's last name(s) - REQUIRED
        - phone_number (string): Member's phone number
        - whatsapp_number (string): Member's whatsapp number
        - email (string): Member's email
        - gender (string): Member's gender (either F or M) - REQUIRED
        - date_of_birth (date): Member's date of birth - REQUIRED
        - address (string): Member's address - REQUIRED
        - is_baptized (boolean): Member's is_baptized - REQUIRED
        - is_born_again (boolean): Member's is_born_again - REQUIRED
        - cell_id (int): Member's cell (id)
        - fellowship_center_id (int): Member's fellowship center (id)
        - department_id (int): Member's department (id)
        - foundation_school_status (string): Member's foundation school status - REQUIRED
        - joined_on (date): Date member joined the church - REQUIRED
        - professional_status (string): Member's professional status (such as employed, unemployed, etc.)
        - occupation (string): Member's occupation
        - school_name (string): Member's school name
        - emergency_contact_name (string): Member's emergency contact name - REQUIRED
        - emergency_contact_phone (string): Member's emergency contact phone number - REQUIRED
        - emergency_contact_whatsapp (string): Member's emergency contact email
        - created_on (timestamptz): The date member created member account - REQUIRED
        - last_updated (timestamptz): The date member info was last updated in the db - REQUIRED
        - profile_photo (bytea): Profile photo of member - REQUIRED

    Returns:
        JSON response with success or error message based on data inputted.
    """
    if request.method == 'POST':
        try:
            first_names = request.form.get('first_names')
            last_names = request.form.get('last_names')
            phone_number = request.form.get('phone_number')
            whatsapp_number = request.form.get('whatsapp_number')
            email = request.form.get('email')
            gender_id = request.form.get('gender_id')
            date_of_birth = request.form.get('date_of_birth')
            address = request.form.get('address')
            is_baptized = request.form.get('is_baptized')
            is_born_again = request.form.get('is_born_again')
            foundation_school_status_id = request.form.get('foundation_school_status_id')
            joined_on = request.form.get('joined_on')
            professional_status = request.form.get('professional_status')
            occupation = request.form.get('occupation')
            school_name = request.form.get('school_name')
            emergency_contact_name = request.form.get('emergency_contact_name')
            emergency_contact_relation = request.form.get('emergency_contact_relation')
            emergency_contact_phone = request.form.get('emergency_contact_phone')
            emergency_contact_whatsapp = request.form.get('emergency_contact_whatsapp')
            cell_id = request.form.get('cell_id')
            department_id = request.form.get('department_id')
            fellowship_center_id = request.form.get('fellowship_center_id')
            profile_photo = request.files.get('profile_photo')

            if (not first_names or not last_names or not gender_id or not date_of_birth or not address or not is_baptized
                    or not is_born_again or not foundation_school_status_id or not joined_on or professional_status or not
                    emergency_contact_phone or not profile_photo):
                return jsonify({
                    'status': 'Error',
                    'message': 'Some required fields are missing'
                }), 400

            profile_photo_data = None
            if profile_photo and profile_photo.filename != '':
                if not allowed_file(profile_photo.filename):
                    return jsonify({
                        'status': 'Error',
                        'message': 'File not allowed'
                    }), 400
                profile_photo_data = profile_photo.read()

            created_on = datetime.datetime.now()
            last_updated = datetime.datetime.now()

            cursor.execute(
                """
                insert into members (
                    first_names, last_names, phone_number, whatsapp_number, email, gender_id, date_of_birth, address, 
                    is_baptized, is_born_again, cell_id, fellowship_center_id, department_id, foundation_school_status_id,
                    joined_on, professional_status, occupation, school_name, emergency_contact_name, emergency_contact_relation,
                    emergency_contact_phone,emergency_contact_whatsapp, profile_photo, created_on, last_updated
                )
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (first_names, last_names, phone_number, whatsapp_number, email, gender_id, date_of_birth, address,
                    is_baptized, is_born_again, cell_id, fellowship_center_id, department_id, foundation_school_status_id,
                    joined_on, professional_status, occupation, school_name, emergency_contact_name, emergency_contact_relation,
                    emergency_contact_phone,emergency_contact_whatsapp, profile_photo, created_on, last_updated)
            )

            close_db_connection()

            return jsonify({
                'status': 'Success',
                'message': 'Member successfully created'
            }), 201
        except Exception as e:
            return jsonify({
                'status': 'Error',
                'message': str(e)
            }), 500
    else:
        return jsonify({
            'status': 'Error',
            'message': 'Invalid HTTP method.'
        }), 405

