document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');

    if (registerForm) {
        registerForm.addEventListener('submit', (event) => {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (username.trim() === '' || password.trim() === '') {
                alert('Username and password are required.');
                event.preventDefault();
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const otp = document.getElementById('otp').value;

            if (username.trim() === '' || password.trim() === '' || otp.trim() === '') {
                alert('All fields are required.');
                event.preventDefault();
            }
        });
    }
});
