from __main__ import app
from congoDB import create, read, update, delete
from controller.mongodbController import MongoDBController
from flask import Flask, redirect, request, abort, render_template, session, url_for
from werkzeug.security import generate_password_hash

@app.route('/update-profile', methods=['GET', 'POST'])
def update_profile():

    if 'user_id' not in session:
        session['error_message'] = "You must be logged in to update your profile!"
        return redirect(url_for('login'))
    
    user_id = session['user_id']  # Replace with the user's ID; you can get it from the user session
    
    update_success = None
    error_message = None

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Check if the new email already exists in the database
        user_exists = read.select(
            table='public."user"',
            where=[f'useremail = \'{email}\'']
        )

        if user_exists:
            error_message = "Email already exists. Please choose another email."
        elif new_password and new_password != confirm_password:
            error_message = "Passwords do not match."
        else:
            update_data = {
                'username': username,
                'useremail': email,
                'useraddress': address,
            }

            # Only update password if user enters a value
            if new_password:
                hashed_password = generate_password_hash(new_password, method='scrypt')
                update_data['userpassword'] = hashed_password

            query = update.update(
                table='user',
                colvalues=update_data,
                where=[f'userid = {user_id}']
            )

            update_success = "Profile updated successfully."

    user_info = read.select(
        table='public."user"',
        columns=['username', 'useremail', 'useraddress'],
        where=[f'userid = {user_id}']
    )

    if not user_info:
        return redirect(url_for('homepage'))
    
    return render_template('update-profile.html', user_info=user_info, update_success=update_success, error_message=error_message)