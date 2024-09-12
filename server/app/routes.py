from flask import current_app as app, jsonify
from flask_security import current_user, auth_required, roles_required, roles_accepted

from app.utils import hard_coded_info

# @roles_required("Student", "Instructor") -> User should have both Student and Instructor. { AND condition }
# @roles_accepted("Student", "Instructor") -> User should have either Student or Instructor. { OR condition }

@app.route("/admin")
@auth_required("token")
@roles_required("Admin")
def admin_dash():
    # current_user: Proxy of the logged in user. Comes from the Session.
    email = current_user.email
    return f"Hello, Admin!\nEmail: {email}"

# @app.route("/student")
# @auth_required("token")
# @roles_accepted("Student", "Instructor")
# def student_home():
#     return {
#         "email": current_user.email,
#         "roles": [role.name for role in current_user.roles]
#     }

@app.route("/registration-form-data")
def registration_form_data():

    return jsonify(hard_coded_info())
