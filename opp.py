# A simple server-side script using Flask to handle form submissions.
# This script listens for a POST request, retrieves the form data,
# and sends an email with the content of the message.

# IMPORTANT: You need to install Flask and Flask-Mail first.
# Run this command in your terminal:
# pip install Flask Flask-Mail

from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os

# Create the Flask application instance
app = Flask(__name__)

# ====================================================================
# STEP 1: CONFIGURE YOUR EMAIL SETTINGS
#
# You MUST replace these placeholder values with your own information.
# Using environment variables is the most secure way to do this
# in a production environment.
# ====================================================================

# Replace with your own email account details
# If you are using Gmail, you may need to enable "Less secure app access"
# or use an app-specific password.
# See documentation for your email provider for specific settings.
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # REPLACE WITH YOUR EMAIL
app.config['MAIL_PASSWORD'] = 'your_email_password'     # REPLACE WITH YOUR PASSWORD

# The email address that the messages will be sent to.
RECIPIENT_EMAIL = 'your_recipient_email@example.com'  # REPLACE WITH YOUR RECIPIENT EMAIL

# Initialize the Mail instance
mail = Mail(app)

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    This function handles the form submission.
    It expects a POST request with JSON data.
    """
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'Invalid request: No data provided.'}), 400

        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Basic validation
        if not all([name, email, subject, message]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        # Create the email message
        msg = Message(
            subject=f"New message from portfolio: {subject}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[RECIPIENT_EMAIL]
        )
        msg.body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """

        # Send the email
        mail.send(msg)
        print("Email sent successfully!")
        return jsonify({'success': True, 'message': 'Message sent successfully!'}), 200

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error sending email: {e}")
        return jsonify({'success': False, 'message': 'Failed to send message.'}), 500

# This block runs the application when the script is executed directly.
if __name__ == '__main__':
    # When deploying, set debug=False. It's only for local development.
    app.run(debug=True, port=5000)

