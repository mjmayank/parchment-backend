import os
import requests
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from app.models import User
from app.constants import CLIENT_ID, GITHUB_API_URL
from unidiff import PatchSet
from urllib.parse import urlparse
from flask import current_app

def get_github_token(google_token):
  if os.environ.get('FLASK_ENV') == 'development':
    github_token = os.environ.get('GITHUB_OAUTH')
  else:
    if not google_token:
      return 'No Google token sent', 500
    idinfo = id_token.verify_oauth2_token(google_token, Request(), CLIENT_ID)
    email = idinfo['email']
    user = User.query.filter_by(email=email).first()
    github_token = user.github_oauth_token or os.environ.get('GITHUB_OAUTH')
  return github_token

def github_request(url, github_token):
  current_app.logger.info(url)
  current_app.logger.info(github_token)
  r = requests.get(url, headers={'Authorization': 'token {token}'.format(token=github_token)})
  current_app.logger.info(r)
  return r

def github_diff_request(url, github_token):
  r = requests.get(
      url,
      headers={
        'Authorization': 'token {token}'.format(token=github_token),
        'Accept': 'application/vnd.github.diff',
      }
    )
  patch = PatchSet(r.text)
  g_doc = str(patch[0][0]).split('@@')[2][2:]
  file_id = urlparse(g_doc).path.split('/')[3]
  return [g_doc, file_id]

def parse_github_url(url):
  parsed_repo_url = urlparse(url)
  github_api_url = (GITHUB_API_URL
    if parsed_repo_url.netloc in ['www.github.com', 'github.com']
    else 'https://' + parsed_repo_url.netloc + '/api/v3')
  split_path = parsed_repo_url.path.split('/')
  owner = split_path[1]
  repo = split_path[2]
  return [owner, repo, github_api_url]