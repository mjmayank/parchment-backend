from __future__ import print_function
from flask import Flask, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
import sys
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'the random string'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
cors = CORS(app)
db = SQLAlchemy(app)

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/userinfo.email']

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.String, unique=False, nullable=True)
    refresh_token = db.Column(db.String, unique=False, nullable=True)
    expiry = db.Column(db.String, unique=False, nullable=True)
    access_token = db.Column(db.String, unique=False, nullable=True)
    

def get_user_info(creds):
  """Send a request to the UserInfo API to retrieve the user's information.

  Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
  Returns:
    User information as a dict.
  """
  user_info_service = build('oauth2', 'v2', credentials=creds)
  user_info = None
  try:
    user_info = user_info_service.userinfo().get().execute()
  except ValueError as e:
    app.logger.error('An error occurred: %s', e)
  if user_info and user_info.get('id'):
    app.logger.info(user_info)
    return user_info.get('email')

@app.route("/")
def home_view():
  db.create_all()
  return "<h1>Welcome to Parchment</h1>"

@app.route("/test")
def test_view():
  email = request.args.get('email')
  user = User.query.filter_by(email=email).first()
  if user:
    if not user.refresh_token:
      return {
      'email': user.email,
      'token': user.token,
      'access_token': user.access_token
    }
    return {
      'email': user.email,
      'token': user.token,
      'access_token': user.access_token,
      'refresh_token': user.refresh_token,
    }
  else:
    return { 'email': 'notfound' }

@app.route("/send/review", methods=["GET"])
def send_review_request():
  email = request.args.get('email')
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails=email)
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
  email = request.args.get('email')
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails=email)
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
  email = request.args.get('email')
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails=email)
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
  email = request.args.get('email')
  message = Mail(
      from_email='mjmayank@gmail.com',
      to_emails=email)
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

@app.route("/document", methods=["GET"])
def sync_document():
  token = request.args.get('idToken')
  try:
    CLIENT_ID = "73937624438-b70smv6ui0j29m29akdjv3vg36oh0htf.apps.googleusercontent.com"
    DOCUMENT_ID = '1M3erMHjZqOhPhs_SnrceyZK4KqqBarFaxhFlQ0vdKGo'
    # Specify the CLIENT_ID of the app that accesses the backend:
    idinfo = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)
    email = idinfo['email']
    user = User.query.filter_by(email=email).first()
    user.access_token = token
    db.session.commit()
    return jsonify(user)
  except ValueError as err:
    # Invalid token
    app.logger.info(err)
    pass
  return idinfo

@app.route("/document2", methods=["GET"])
def sign_in():
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.json'):
      creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = Flow.from_client_secrets_file(
              'credentials.json', SCOPES)
          flow.redirect_uri = 'https://limitless-sierra-24357.herokuapp.com/document3'
          # flow.redirect_uri = 'http://localhost:5000/document3'
          # Generate URL for request to Google's OAuth 2.0 server.
          # Use kwargs to set optional request parameters.
          authorization_url, _ = flow.authorization_url(
              # Enable offline access so that you can refresh an access token without
              # re-prompting the user for permission. Recommended for web server apps.
              access_type='offline',
              # Enable incremental authorization. Recommended as a best practice.
              include_granted_scopes='true')
          return redirect(authorization_url)
          # creds = flow.run_local_server(port=8000)

@app.route("/document3", methods=["GET"])
def create_doc():
  # The ID of a sample document.
  DOCUMENT_ID = '1M3erMHjZqOhPhs_SnrceyZK4KqqBarFaxhFlQ0vdKGo'

  flow = Flow.from_client_secrets_file(
      'credentials.json',
      scopes=SCOPES)
  flow.redirect_uri = url_for('create_doc', _external=True)
  app.logger.info('redirecturi', flow.redirect_uri)

  authorization_response = request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store the credentials in the session.
  # ACTION ITEM for developers:
  #     Store user's access and refresh tokens in your data store if
  #     incorporating this code into your real app.
  creds = flow.credentials
  session['credentials'] = {
    'token': creds.token,
    'refresh_token': creds.refresh_token,
    'token_uri': creds.token_uri,
    'client_id': creds.client_id,
    'client_secret': creds.client_secret,
    'scopes': creds.scopes
  }
  email = get_user_info(creds)
  user = User.query.filter_by(email=email).first()
  if user:
    new_user = user
    if not user.refresh_token:
      user.token=creds.token
      user.refresh_token=creds.refresh_token
      user.expiry=credits.expiry
      db.session.commmit()
  else:
    new_user = User(
      email=email,
      token=creds.token,
      refresh_token=creds.refresh_token,
      expiry=creds.expiry,
    )
    db.session.add(new_user)
    db.session.commit()
  return jsonify({ 'email': new_user.email })

@app.route("/document/create", methods=["POST"])
def generate_doc():
  print(request.json)
  token = request.json['idToken']
  document_data = request.json['documentData']
  CLIENT_ID = "73937624438-b70smv6ui0j29m29akdjv3vg36oh0htf.apps.googleusercontent.com"
  DOCUMENT_ID = '1M3erMHjZqOhPhs_SnrceyZK4KqqBarFaxhFlQ0vdKGo'
  # Specify the CLIENT_ID of the app that accesses the backend:
  idinfo = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)
  email = idinfo['email']
  user = User.query.filter_by(email=email).first()
  print(user.email)
  creds_info = {
    'refresh_token': user.refresh_token,
    'token': user.access_token,
    'expiry': user.expiry.replace(' ', 'T'),
    'client_secret': '-K5PjHqNEc-aKLRVj0JiNG0y',
    'client_id': CLIENT_ID,
    'token_uri': 'https://oauth2.googleapis.com/token',
  }
  creds = None
  creds = Credentials.from_authorized_user_info(creds_info)
  service = build('docs', 'v1', credentials=creds)

  # Retrieve the documents contents from the Docs service.
  document = service.documents().get(documentId=DOCUMENT_ID).execute()

  requests = []

  for item in document_data:
      docs_item = translate_to_doc(item)
      requests += docs_item

  print(requests[::-1])

  result = service.documents().batchUpdate(
      documentId=DOCUMENT_ID, body={'requests': requests[::-1]}).execute()

  print('The title of the document is: {}'.format(document.get('title')))
  return creds.to_json()

def translate_to_doc(item):
    newline = '\n'
    checkbox = '[ ]'
    if item['type'] == 'check':
        return [
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex':  len(item['text']) + 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                    },
                    'fields': 'namedStyleType'
                }
            },
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': checkbox + ' ' + item['text'] + newline
                }
            }
        ]
    elif item['type'] == 'h1' or item['type'] == 'h2':
        namedStyleType = 'HEADING_1' if item['type'] == 'h1' else 'HEADING_2'
        return [
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex':  len(item['text']) + 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': namedStyleType,
                    },
                    'fields': 'namedStyleType'
                }
            },
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': item['text'] + newline
                }
            },
        ]
    elif item['type'] == 'watermark':
        formatting = [
            {
                'bold': False,
                'fontSize': {
                    'magnitude': 10,
                    'unit': 'PT',
                },
                'weightedFontFamily': {
                    'fontFamily': 'Roboto',
                }
            },
            'bold, fontSize, weightedFontFamily',
        ]
        return [
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': len(item['text']) + 1
                    },
                    'textStyle': formatting[0],
                    'fields': formatting[1]
                }
            },
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': item['text'] + newline + newline
                }
            }
        ]
    elif item['type'] == 'request':
        text = 'Input requested from ' + item['text']
        formatting = [
            {
                'bold': False,
                'fontSize': {
                    'magnitude': 12,
                    'unit': 'PT',
                },
                'weightedFontFamily': {
                    'fontFamily': 'Roboto',
                }
            },
            'bold, fontSize, weightedFontFamily',
        ]
        return [
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': len(text) + 1
                    },
                    'textStyle': formatting[0],
                    'fields': formatting[1]
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex':  len(text) + 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                    },
                    'fields': 'namedStyleType'
                }
            },
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': text + newline
                }
            }
        ]
    elif item['type'] == 'emoji':
        text = item['text']
        for name in item['data']:
            text += name + ', '
        formatting = [
            {
                'bold': False,
                'fontSize': {
                    'magnitude': 12,
                    'unit': 'PT',
                },
                'weightedFontFamily': {
                    'fontFamily': 'Roboto',
                }
            },
            'bold, fontSize, weightedFontFamily',
        ]
        return [
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex':  len(text) + 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                    },
                    'fields': 'namedStyleType'
                }
            },
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': text + newline
                }
            }
        ]
    else:
        formatting = [
            {
                'bold': False,
                'fontSize': {
                    'magnitude': 12,
                    'unit': 'PT',
                },
                'weightedFontFamily': {
                    'fontFamily': 'Roboto',
                }
            },
            'bold, fontSize, weightedFontFamily',
        ]
        return [
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex':  len(item['text']) + 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
                    },
                    'fields': 'namedStyleType'
                }
            },
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': item['text'] + newline
                }
            }
        ]
