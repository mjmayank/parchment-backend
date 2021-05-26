from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1M3erMHjZqOhPhs_SnrceyZK4KqqBarFaxhFlQ0vdKGo'

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


def main():
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    document_data = [
        {
            'text': "Document created by MayankDoc",
            'type': "watermark",
        },
        {
            'text': "Growth Roadmap Review: 10:30am-11:30am",
            'type': "event",
        },
        { 
            'text': "Growth Roadmap Review",
            'type': "h1",
        },
        {
            'text': "Agenda",
            'type': "h2",
        },
        {
            'text': "Roadmap Study Hall - 15 minutes",
            'type': "p",
        },
        {
            'text': "Roadmap Discussion - 20 minutes",
            'type': "p",
        },
        {
            'text': "Backlog Review - 20 minutes",
            'type': "p",
        },
        {
            'text': "Follow Ups",
            'type': "h2",
        },
        {
            'text': "",
            'type': "check",
        },
        {
            'text': "Roadmap",
            'type': "h2",
        },
        {
            'text': "Channels",
            'type': "p",
        },
        {
            'text': "Rose Liu",
            'type': "request",
        },
        {
            'text': "👍",
            'type': 'emoji',
            'data': ['Mayank Jain', 'Yee Chen', 'Mike Jiao'],
        },
        {
            'text': "Core Growth",
            'type': "p",
        },
        {
            'text': "Mike Jiao",
            'type': "request",
        },
        {
            'text': "👍",
            'type': 'emoji',
            'data': [],
        },
        {
            'text': "International",
            'type': "p",
        },
        {
            'text': "Jason Lee",
            'type': "request",
        },
        {
            'text': "👍",
            'type': 'emoji',
            'data': [],
        },
        {
            'text': "SEO",
            'type': "p",
        },
        {
            'text': "Chuck Kao",
            'type': "request",
        },
        {
            'text': "👍",
            'type': 'emoji',
            'data': [],
        },
        {
            'text': "Key Discussion",
            'type': "h2",
        },
        {
            'text': "Can we do anything to accelerate subreddit notifications?",
            'type': "discussion",
        },
        {
            'text': "Action Items",
            'type': "h2",
        },
        {
            'text': "",
            'type': "check",
        },
        {
            'text': "Signoff",
            'type': "h2",
        },
        {
            'text': "KD Bhulani",
            'type': "signoff",
        },
        {
            'text': "Vee Sahgal",
            'type': "signoff",
        },
        {
            'text': "Yee Chen",
            'type': "signoff",
        }
    ]

    requests = []

    for item in document_data:
        docs_item = translate_to_doc(item)
        requests += docs_item

    print(requests[::-1])

    result = service.documents().batchUpdate(
        documentId=DOCUMENT_ID, body={'requests': requests[::-1]}).execute()

    print('The title of the document is: {}'.format(document.get('title')))


if __name__ == '__main__':
    main()
