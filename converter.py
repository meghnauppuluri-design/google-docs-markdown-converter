"""
Markdown to Google Docs Converter

Converts structured markdown meeting notes into a formatted Google Doc
using the Google Docs API.
"""

import re
from googleapiclient.discovery import build
from google.auth import default


def authenticate_docs_service():
    """Authenticate and return Google Docs service."""
    creds, _ = default()
    return build("docs", "v1", credentials=creds)


def create_document(service, title):
    """Create a new Google Doc and return its document ID."""
    doc = service.documents().create(body={"title": title}).execute()
    return doc["documentId"]


def insert_text(requests, text, style=None):
    """Insert text with optional paragraph style."""
    requests.append({
        "insertText": {
            "location": {"index": 1},
            "text": text + "\n"
        }
    })

    if style:
        requests.append({
            "updateParagraphStyle": {
                "range": {
                    "startIndex": 1,
                    "endIndex": 1 + len(text)
                },
                "paragraphStyle": style,
                "fields": ",".join(style.keys())
            }
        })


def parse_markdown(md_text):
    """Convert markdown text into Google Docs API requests."""
    requests = []
    lines = md_text.splitlines()

    for line in lines:
        line = line.rstrip()

        if line.startswith("# "):
            insert_text(requests, line[2:], {"namedStyleType": "HEADING_1"})

        elif line.startswith("## "):
            insert_text(requests, line[3:], {"namedStyleType": "HEADING_2"})

        elif line.startswith("### "):
            insert_text(requests, line[4:], {"namedStyleType": "HEADING_3"})

        elif re.match(r"- \[ \]", line):
            text = re.sub(r"- \[ \]\s*", "", line)
            insert_text(requests, text)
            requests.append({
                "createParagraphBullets": {
                    "range": {"startIndex": 1, "endIndex": 1 + len(text)},
                    "bulletPreset": "BULLET_CHECKBOX"
                }
            })

            for match in re.finditer(r"@\w+", text):
                start = 1 + match.start()
                end = 1 + match.end()
                requests.append({
                    "updateTextStyle": {
                        "range": {"startIndex": start, "endIndex": end},
                        "textStyle": {
                            "bold": True,
                            "foregroundColor": {
                                "color": {"rgbColor": {"blue": 1}}
                            }
                        },
                        "fields": "bold,foregroundColor"
                    }
                })

        elif line.lstrip().startswith(("* ", "- ")):
            text = line.lstrip()[2:]
            insert_text(requests, text)
            requests.append({
                "createParagraphBullets": {
                    "range": {"startIndex": 1, "endIndex": 1 + len(text)},
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
                }
            })

        elif line.startswith("Meeting recorded by") or line.startswith("Duration"):
            insert_text(requests, line)
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": 1, "endIndex": 1 + len(line)},
                    "textStyle": {"italic": True},
                    "fields": "italic"
                }
            })

        elif line.strip():
            insert_text(requests, line)

    return requests


def main(markdown_path):
    service = authenticate_docs_service()

    with open(markdown_path, "r") as f:
        md_text = f.read()

    document_id = create_document(service, "Product Team Sync")
    requests = parse_markdown(md_text)

    service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": requests}
    ).execute()

    print(f"Document created: https://docs.google.com/document/d/{document_id}")


if __name__ == "__main__":
    main("sample_notes.md")
