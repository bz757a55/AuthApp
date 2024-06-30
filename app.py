from flask import Flask, render_template, redirect, url_for, flash, request, session
import pyotp
import hashlib
from auth import auth_blueprint  # Assuming auth blueprint is defined

app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(auth_blueprint)

# Mock database for storing user information

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp_code = request.form.get('otp_code')
        otp_secret = session.get('otp_secret')

        if not otp_code:
            flash('Please enter your OTP code.')
            return redirect(url_for('verify_otp'))

        totp = pyotp.TOTP(otp_secret)
        if totp.verify(otp_code):
            flash('Verification successful!')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid verification code. Please try again.')
            return redirect(url_for('verify_otp'))

    return render_template('verify_otp.html')

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
