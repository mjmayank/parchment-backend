from flask import Flask
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
  
app = Flask(__name__)
  
@app.route("/")
def home_view():
        return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/send", methods=["GET"])
def send_email():
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails='mjmayank@gmail.com',
      template_id='d-fe954c63b4b6489dab6074dde908b216')
  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)
  return "<div>Done!</div>"