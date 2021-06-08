def translate_to_doc(item):
    newline = '\n'
    if item['type'] == 'check':
        checkbox = '[ ]' if 'data' in item else '[X]'
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

def translate_from_doc(item, paragraph):
    text_run = item.get('textRun')
    text = text_run.get('content') if text_run else ''

    text_type = ''
    data = []

    if text.startswith(("[ ]", "[X]")):
      text_type = 'check'
      text = text[:3]
    elif paragraph.get('paragraphStyle').get('namedStyleType') == 'HEADING_1':
      text_type = 'h1'
    elif paragraph.get('paragraphStyle').get('namedStyleType') == 'HEADING_2':
      text_type = 'h2'
    elif text.startswith("Input requested from "):
      text_type = 'request'
    elif text.startswith(tuple(UNICODE_EMOJI['en'].keys())):
      text_type = 'emoji'
      data = text[1:]
      text = text[:1]
    else:
      text_type = 'text'

    return {'text': text, 'type': text_type, 'data': data}
