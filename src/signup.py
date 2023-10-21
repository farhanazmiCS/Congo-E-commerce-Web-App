from __main__ import app
from flask import Flask, request, abort, render_template
from werkzeug.security import generate_password_hash
from PostGresControllerV2.PostGresControllerV2 import initialise_crud

create, read, update, delete = initialise_crud()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_success = False
    error_message = None

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 == password2:
            # Hash the password using Werkzeug
            hashed_password = generate_password_hash(password1)

            # Create a dictionary with the user data
            user_data = {
                'username': username,
                'userpassword': hashed_password,
                'usertype': 'customer',
                'useremail': email,
                'useraddress': address
            }

            # Use create.insert() to insert the user data into the database
            query = create.insert(table='user', columns=list(user_data.keys()), values=list(user_data.values()))
            signup_success = True
        else:
            error_message = "Passwords do not match."

    return render_template('signup.html', signup_success=signup_success, error_message=error_message)
