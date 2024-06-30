from flask import Blueprint, render_template, redirect, url_for, flash, request, session
import pyotp
import qrcode
import os
from models import get_user, verify_password, create_user

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if create_user(username, password, email):
            flash('Registration successful! Please log in.')
            return redirect(url_for('auth.login'))
        else:
            flash('User already exists.')
    return render_template('register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and verify_password(user['password'], password):
            session['username'] = username
            flash('Login successful! Please check your email for the verification code.')
            return redirect(url_for('auth.setup_otp', username=username))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@auth_blueprint.route('/setup_otp/<username>', methods=['GET', 'POST'])
def setup_otp(username):
    if request.method == 'POST':
        otp_secret = pyotp.random_base32()
        otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=username, issuer_name='YourApp')
        qr = qrcode.make(otp_uri)
        qr_file = f'static/{username}_qr.png'
        qr.save(qr_file)
        session['otp_secret'] = otp_secret
        return redirect(url_for('auth.show_qr', username=username))
    return render_template('setup_otp.html', username=username)

@auth_blueprint.route('/qr_code/<username>')
def show_qr(username):
    return render_template('qr_code.html', username=username)

@auth_blueprint.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        otp_code = request.form.get('otp_code')  # Use get() to handle missing keys gracefully
        otp_secret = session.get('otp_secret')

        if not otp_code:
            flash('Please enter your OTP code.')
            return redirect(url_for('auth.verify_otp'))

        totp = pyotp.TOTP(otp_secret)
        if totp.verify(otp_code):
            flash('Verification successful!')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid verification code. Please try again.')
            return redirect(url_for('auth.verify_otp'))

    return render_template('verify_otp.html')
@auth_blueprint.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome {session['username']}!"
    return redirect(url_for('auth.login'))

@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('otp_secret', None)
    return redirect(url_for('auth.login'))
