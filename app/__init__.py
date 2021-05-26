from flask import Flask
from flask_cors import CORS
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
  
app = Flask(__name__)
cors = CORS(app)
  
@app.route("/")
def home_view():
        return "<h1>Welcome to Parchment</h1>"

@app.route("/send/review", methods=["GET"])
def send_review_request():
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails='mjmayank@gmail.com')
  message.template_id = 'd-fe954c63b4b6489dab6074dde908b216'
  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)
  return "<div>Done!</div>"

@app.route("/send/reminder", methods=["GET"])
def send_reminder_request():
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails='mjmayank@gmail.com')
  message.template_id = 'd-b0830da153e44dfc804cd1b33622dd59'
  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)
  return "<div>Done!</div>"

@app.route("/send/premeeting", methods=["GET"])
def send_premeeting():
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails='mjmayank@gmail.com')
  message.template_id = 'd-1ed6ddbaacb54c0fa15841f52b02b890'
  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)
  return "<div>Done!</div>"

@app.route("/send/postmeeting", methods=["GET"])
def send_postmeeting():
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails='mjmayank@gmail.com')
  message.template_id = 'd-75860aa6fd8b4535b88d4aa5146bf7fe'
  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)
  return "<div>Done!</div>"