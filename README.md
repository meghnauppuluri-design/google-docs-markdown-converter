# Markdown to Google Docs Converter

## Description
This project converts structured markdown meeting notes into a well-formatted Google Doc using the Google Docs API. It is designed to run in Google Colab and supports headings, nested bullet lists, Google Docs checkboxes, styled assignee mentions, and distinct footer formatting.

## Features
- Google Docs API integration
- Heading levels (H1, H2, H3)
- Nested bullet points
- Google Docs checkboxes for action items
- Styled @mentions for assignees
- Distinct footer styling
- Google Colab compatible

## Repository Structure
├── convert_markdown_to_gdoc.ipynb   # Main Colab notebook
├── converter.py                     # Script version of the same logic
├── requirements.txt                 # Python dependencies
├── sample_notes.md                  # Sample markdown input
└── README.md

## Prerequisites
- A Google account
- Access to Google Colab
- Google Drive enabled

No API keys are required. Authentication is handled via Google Colab.

## Setup Instructions

### Run in Google Colab (Recommended)
1. Open Google Colab
2. Upload the following files:
   - convert_markdown_to_gdoc.ipynb
   - sample_notes.md
3. Open the notebook
4. Run all cells from top to bottom
5. Authenticate with your Google account when prompted

After successful execution, a new Google Doc will be created in your Google Drive and a link to the document will be printed in the notebook output.

### Run Locally (Optional)
1. Clone the repository:
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
2. Install dependencies:
   pip install -r requirements.txt
3. Authenticate using Google Application Default Credentials
4. Run the script:
   python converter.py

## Input Format
The input markdown file (sample_notes.md) follows standard markdown syntax:
- # for the main title
- ## for section headers
- ### for sub-section headers
- * or - for bullet points
- - [ ] for checkboxes
- @name for assignee mentions

## Output
- A new Google Doc created in the user's Google Drive
- Proper heading hierarchy
- Nested bullet lists
- Action items rendered as checkboxes
- Assignee mentions styled for visibility
- Footer information visually distinct

## Error Handling
- Authentication failures are surfaced immediately
- Google Docs API errors are caught and reported
- The script exits gracefully with meaningful error messages

## Notes
- No credentials are stored in this repository
- Authentication is handled securely by Google Colab
- This project is intended for evaluation and demonstration purposes

## License
This project is provided for assessment and demonstration purposes only.
