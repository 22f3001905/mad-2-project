from flask import current_app as app
from flask_security import current_user, auth_required, roles_required, roles_accepted

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
