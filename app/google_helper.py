from app.constants import CLIENT_ID, CLIENT_SECRET
from app.models import User, db

from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import httplib2

def get_drive_service(token):
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
  service = build('drive', 'v3', credentials=creds)
  return service

def get_docs_service(token):
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
  return service

def refresh_access_token(creds, user):
  creds.refresh(httplib2.Http())
  user.token=creds.token
  user.refresh_token=creds.refresh_token
  user.expiry=creds.expiry
  db.session.commit()