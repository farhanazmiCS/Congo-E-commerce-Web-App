from __main__ import app
from ricefield import create, read, update, delete
from flask import Flask, redirect, request, abort, render_template, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/login', methods=["GET", "POST"])
def login():
    error_message = None  # Initialize an error message variable
    error_message = session.get('error_message') # Get the error message from the session
    session.pop('error_message', None) # Clear the error message from the session

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Replace 'user_password' with the correct column name for the hashed password in your database
        user_data = read.select(table='public.user', where=[f"useremail = '{email}'"])
        
        if user_data:
            for row in user_data:
                stored_password = row[2]  # Access the password from the tuple by index
                if check_password_hash(stored_password, password):
                    # Passwords match, login is successful
                    session['user_id'] = row[0]  # Access the user ID from the tuple by index
                    session['user_name'] = row[1]
                    session['user_type'] = row[3]
                    session['cart'] = []
                    return redirect(url_for('homepage'))

        # If the loop completes without a successful login, show an error message
        error_message = "Invalid email or password"

    return render_template('login.html', error_message=error_message)