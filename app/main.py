from flask import Flask
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
  
app = Flask(__name__)
  
@app.route("/")
def home_view():
        return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/send")
def send_email():
  message = Mail(
      from_email='from_email@example.com',
      to_emails='to@example.com',
      subject='Sending with Twilio SendGrid is Fun',
      html_content='<strong>and easy to do anywhere, even with Python</strong>')
  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)