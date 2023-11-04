from __main__ import app
from ricefield import create, read, update, delete
from mongodbcontrollerV2 import MongoDBController
from flask import Flask, request, abort, render_template
from werkzeug.security import generate_password_hash

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_success = False  # Initialize these variables with default values
    error_message = None

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if the username or email already exists
        user_exists = read.select(table='public.user', where=[f"useremail = '{email}'"])

        if user_exists:
            error_message = "Email already exists."
        elif password1 == password2:
            # Hash the password using scrypt
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

            # create user's cart in MongoDB
            # get user ID from created user's username
            user_id = read.select(table='public.user', where=[f"username = '{username}'"])
            if (user_id):

                cart_data = {
                    'user_id': user_id[0][0],
                    'products': []
                }

                controller = MongoDBController() 
                controller.create('Cart', cart_data)
                controller.close_connection()

            else:
                error_message = "User ID not found to create cart."

            signup_success = True

            error_message = None  # Reset error message on success
        else:
            error_message = "Passwords do not match."

    return render_template('signup.html', signup_success=signup_success, error_message=error_message)
