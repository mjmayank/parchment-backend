import os

ROOT_DOMAIN = ('https://api.speckdoc.com'
  if not os.environ.get('FLASK_ENV') == 'development'
  else 'http://localhost:5000')

credentials_json = ('client_secret_prod.json'
  if not os.environ.get('FLASK_ENV') == 'development'
  else 'client_secret_dev.json')

SCOPES = [
  'https://www.googleapis.com/auth/documents',
  'https://www.googleapis.com/auth/userinfo.email',
  'https://www.googleapis.com/auth/drive',
]
CLIENT_ID = ("73937624438-b70smv6ui0j29m29akdjv3vg36oh0htf.apps.googleusercontent.com"
  if not os.environ.get('FLASK_ENV') == 'development'
  else "73937624438-ivv2g6bb7gsp0c4tq0nku5vj9u0t42uu.apps.googleusercontent.com")
CLIENT_SECRET = os.environ.get('GOOGLE_SECRET')

DOCUMENT_ID = ('1M3erMHjZqOhPhs_SnrceyZK4KqqBarFaxhFlQ0vdKGo' 
  if not os.environ.get('DOCUMENT_ID')
  else os.environ.get('DOCUMENT_ID'))

GITHUB_API_URL = 'https://api.github.com'