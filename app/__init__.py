from __future__ import print_function
from flask import Flask, request, redirect, url_for, session, jsonify, render_template
from flask_cors import CORS
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from flask_sqlalchemy import SQLAlchemy
import requests
from app.doc_translator import translate_from_doc, translate_to_doc
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'the random string'
SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
  if not os.environ.get('FLASK_ENV') == 'development'
  else os.environ.get('DATABASE_URL'))
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

ROOT_DOMAIN = ('https://limitless-sierra-24357.herokuapp.com'
  if not os.environ.get('FLASK_ENV') == 'development'
  else 'http://localhost:5000')

credentials_json = ('client_secret_prod.json'
  if not os.environ.get('FLASK_ENV') == 'development'
  else 'client_secret_dev.json')

cors = CORS(app)
db = SQLAlchemy(app)

SCOPES = [
  'https://www.googleapis.com/auth/documents',
  'https://www.googleapis.com/auth/userinfo.email',
  'https://www.googleapis.com/auth/drive',
]
CLIENT_ID = ("73937624438-b70smv6ui0j29m29akdjv3vg36oh0htf.apps.googleusercontent.com"
  if not os.environ.get('FLASK_ENV') == 'development'
  else "73937624438-ivv2g6bb7gsp0c4tq0nku5vj9u0t42uu.apps.googleusercontent.com")
CLIENT_SECRET = os.environ.get('GOOGLE_SECRET')

DOCUMENT_ID = '1M3erMHjZqOhPhs_SnrceyZK4KqqBarFaxhFlQ0vdKGo' if not os.environ.get('DOCUMENT_ID') else os.environ.get('DOCUMENT_ID')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.String, unique=False, nullable=True)
    refresh_token = db.Column(db.String, unique=False, nullable=True)
    expiry = db.Column(db.String, unique=False, nullable=True)
    access_token = db.Column(db.String, unique=False, nullable=True)
    github_oauth_token = db.Column(db.String, unique=False, nullable=True)
    

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
  return render_template("index.html")

@app.route("/db")
def db_create():
  db.create_all()
  return "<h1>Welcome to Parchment</h1>"

@app.route("/delete")
def delete():
  email = request.args.get('email')
  user = User.query.filter_by(email=email).first()
  db.session.delete(user)
  db.session.commit()
  return "Successfully deleted user: " + email

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
  except Exception as e:
      print(e.message)
  return "<div>Done!</div>"

@app.route("/checkRegistration", methods=["POST"])
def check_registration():
  token = request.json.get('idToken')
  app.logger.info(token)
  try:
    # Specify the CLIENT_ID of the app that accesses the backend:
    idinfo = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)
    email = idinfo['email']
    user = User.query.filter_by(email=email).first()
    if user:
      return 'User registered', 200
    else:
      return 'User not registered', 404
  except ValueError as err:
    return str(err), 500

@app.route("/document", methods=["GET"])
def sync_document():
  token = request.args.get('idToken')
  try:
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

@app.route("/createNew", methods=["POST"])
def create_new_document():
  token = request.json.get('idToken')
  if not token:
    return 'No token sent', 500
  idinfo = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)
  email = idinfo['email']
  user = User.query.filter_by(email=email).first()
  creds_info = {
    'refresh_token': user.refresh_token,
    'token': user.access_token,
    'expiry': user.expiry.replace(' ', 'T'),
    'client_secret': CLIENT_SECRET,
    'client_id': CLIENT_ID,
    'token_uri': 'https://oauth2.googleapis.com/token',
  }
  creds = None
  creds = Credentials.from_authorized_user_info(creds_info)
  service = build('docs', 'v1', credentials=creds)
  doc = service.documents().create().execute()
  app.logger.info(doc)
  return { 'documentId': doc.get('documentId') }

@app.route("/signin", methods=["GET"])
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
              credentials_json, SCOPES)
          flow.redirect_uri = ('https://api.speckdoc.com/signin/success'
            if not os.environ.get('FLASK_ENV') == 'development'
            else 'http://localhost:5000/signin/success')
          # Generate URL for request to Google's OAuth 2.0 server.
          # Use kwargs to set optional request parameters.
          authorization_url, _ = flow.authorization_url(
              # Enable offline access so that you can refresh an access token without
              # re-prompting the user for permission. Recommended for web server apps.
              access_type='offline',
              # Enable incremental authorization. Recommended as a best practice.
              include_granted_scopes='true',
              # force approval prompt to get access token
              approval_prompt='force')
          return redirect(authorization_url)
          # creds = flow.run_local_server(port=8000)

@app.route("/signin/success", methods=["GET"])
def create_doc():
  flow = Flow.from_client_secrets_file(
      credentials_json,
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
    user.token=creds.token
    user.refresh_token=creds.refresh_token
    user.expiry=creds.expiry
    db.session.commit()
  else:
    user = User(
      email=email,
      token=creds.token,
      refresh_token=creds.refresh_token,
      expiry=creds.expiry,
    )
    db.session.add(user)
    db.session.commit()
  if (os.environ.get('FLASK_ENV') != 'development' and user.refresh_token):
    return 'You can close this tab'
  return jsonify({
    'email': user.email,
    'refresh_token': user.refresh_token,
    'client_id': creds.client_id,
  })

@app.route("/document/create", methods=["POST"])
def generate_doc():
  token = request.json.get('idToken')
  if not token:
    return 'No token sent', 500
  document_data = request.json.get('documentData')
  document_id = request.json.get('documentId')
  document_title = request.json.get('title')
  if not document_id:
    document_id = DOCUMENT_ID
    app.logger.warn('No document ID provided. Using default document.')
  idinfo = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)
  email = idinfo['email']
  user = User.query.filter_by(email=email).first()
  creds_info = {
    'refresh_token': user.refresh_token,
    'token': user.access_token,
    'expiry': user.expiry.replace(' ', 'T'),
    'client_secret': CLIENT_SECRET,
    'client_id': CLIENT_ID,
    'token_uri': 'https://oauth2.googleapis.com/token',
  }
  creds = Credentials.from_authorized_user_info(creds_info)
  service = build('docs', 'v1', credentials=creds)

  # Retrieve the documents contents from the Docs service.
  document = service.documents().get(documentId=document_id).execute()

  end_index = document.get('body').get('content')[-1].get('endIndex')
  requests = []

  for item in document_data:
      docs_item = translate_to_doc(item)
      requests += docs_item

  if end_index > 2:
    requests += [{
      'deleteContentRange': {
        'range': {
          'startIndex': 1,
          'endIndex': document.get('body').get('content')[-1].get('endIndex')-1,
        }
      }
    }]

  result = service.documents().batchUpdate(
      documentId=document_id, body={'requests': requests[::-1]}).execute()

  drive_service = build('drive', 'v3', credentials=creds)
  drive_service.files().update(fileId=document_id, body={'name': document_title}, fields='name').execute()

  return creds.to_json()

@app.route("/document/sync", methods=["POST"])
def sync_from_doc():
  app.logger.info(request.json)
  token = request.json.get('idToken')
  if not token:
    return 'No token sent', 500
  # document_data = request.json['documentData']
  document_id = request.json.get('documentId')
  if not document_id:
    document_id = DOCUMENT_ID
    app.logger.warn('No document ID provided. Using default document.')
  idinfo = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)
  email = idinfo['email']
  user = User.query.filter_by(email=email).first()
  creds_info = {
    'refresh_token': user.refresh_token,
    'token': user.access_token,
    'expiry': user.expiry.replace(' ', 'T'),
    'client_secret': CLIENT_SECRET,
    'client_id': CLIENT_ID,
    'token_uri': 'https://oauth2.googleapis.com/token',
  }
  creds = None
  creds = Credentials.from_authorized_user_info(creds_info)
  service = build('docs', 'v1', credentials=creds)

  # Retrieve the documents contents from the Docs service.
  document = service.documents().get(documentId=document_id).execute()
  doc_content = document.get('body').get('content')
  doc_title = document.get('title')
  app.logger.info(doc_title)
  document_data = []
  for value in doc_content:
    if 'paragraph' in value:
      elements = value.get('paragraph').get('elements')
      for elem in elements:
        translated_value = translate_from_doc(elem, value.get('paragraph'))
        if translated_value:
          document_data.append(translated_value)
  return { 
    'title': doc_title,
    'body': document_data,
  }

@app.route("/github/read", methods=["POST"])
def read_from_github():
  repo_url = request.json.get('repo')
  parsed_repo_url = urlparse(repo_url)
  app.logger.info(parsed_repo_url)
  GITHUB_URL = 'https://api.github.com'
  app.logger.info(parsed_repo_url.netloc in ['www.github.com', 'github.com'])
  if not parsed_repo_url.netloc in ['www.github.com', 'github.com']:
    GITHUB_URL = 'https://' + parsed_repo_url.netloc + '/api/v3'
  split_path = parsed_repo_url.path.split('/')
  app.logger.info(split_path)
  owner = split_path[1]
  repo = split_path[2]
  google_token = None
  if request.json:
    google_token = request.json.get('idToken')
  github_token = None
  if os.environ.get('FLASK_ENV') == 'development':
    github_token = os.environ.get('GITHUB_OAUTH')
  else:
    if not google_token:
      return 'No Google token sent', 500
    idinfo = id_token.verify_oauth2_token(google_token, Request(), CLIENT_ID)
    email = idinfo['email']
    user = User.query.filter_by(email=email).first()
    github_token = user.github_oauth_token or os.environ.get('GITHUB_OAUTH')
  if not github_token:
    return {
      'data': '/github-add_auth [replace this with your github token]',
    }, 403
  pulls = []
  app.logger.info(owner)
  app.logger.info(repo)
  url = GITHUB_URL + '/repos/{owner}/{repo}/pulls'.format(owner=owner, repo=repo)
  r = requests.get(url, headers={'Authorization': 'token {token}'.format(token=github_token)})
  for pr in r.json():
    pulls.append([pr.get('title'), pr.get('number'), pr.get('user').get('login')])
  users = []
  for pr in pulls:
    data = [pr[0], [pr[2]]]
    url = GITHUB_URL + '/repos/{owner}/{repo}/pulls/{pull_number}/reviews'.format(owner=owner, repo=repo, pull_number=pr[1])
    r = requests.get(url, headers={'Authorization': 'token {token}'.format(token=github_token)})
    for reviewer in r.json():
      if reviewer:
        data[1].append(reviewer.get('user').get('login'))
    url = GITHUB_URL + '/repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers'.format(owner=owner, repo=repo, pull_number=pr[1])
    r = requests.get(url, headers={'Authorization': 'token {token}'.format(token=github_token)})
    for reviewer in r.json().get('users'):
      if reviewer:
        data[1].append(reviewer.get('login'))
    data[1] = list(dict.fromkeys(data[1]))
    users.append(data)
  document_data = []
  for data in users:
    document_data.append({
      'type': 'h2',
      'text': data[0],
    })
    for user in data[1]:
      document_data.append({
        'type': 'p',
        'text': user,
      })
  return { 'data': document_data }

@app.route("/github/sync", methods=["POST"])
def sync_github():
  github_token = request.json.get('token')
  google_token = request.json.get('idToken')
  if not google_token:
    return 'No Google token sent', 500
  idinfo = id_token.verify_oauth2_token(google_token, Request(), CLIENT_ID)
  email = idinfo['email']
  user = User.query.filter_by(email=email).first()
  user.github_oauth_token = github_token
  db.session.add(user)
  db.session.commit()
  return "Github token saved successfully", 200