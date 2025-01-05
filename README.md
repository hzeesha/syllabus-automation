# syllabus-automation
This project automates the process of extracting course-related deadlines (e.g., assignments, quizzes, exams) from a syllabus PDF and adding them as events to your Google Calendar.

## Files

### findDates.py
- Extracts text from a PDF (using pdfminer.six).
- Searches for dates and times with regex patterns.
- Builds a list (due_dates) of properly formatted events (including optional start/end times).

### addDates.py
- Reads due_dates from findDates.py.
- Authenticates with Google Calendar using OAuth 2.0.
- Inserts each event into your primary Google Calendar.

## Prequisites
- Python 3.9+ recommended.
- A Google Cloud project with Calendar API enabled. Download your OAuth credentials file as credentials.json and place it in the same directory.
- Dependencies listed in requirements.txt.

## Installation
- Clone this repo
Bash:
git clone git@github.com:hzeesha/syllabus-automation.git
- Navigate to the repo
- Install dependencies
Bash:
pip install -r requirements.txt
- Ensure you have credentials.json (Google API client secrets) in the project folder

## Usage 
### Edit findDates.py:
- Update course_code (e.g. "CS1234") with your actual course code.
- Update text = extract_text("syllabus.pdf") if your file is named something else.

### Run findDates.py
### Run addDates.py
- On the first run, it will open a browser window to authorize the Calendar API.
- It saves a token.json file for future runs.
- If successful, it creates events in your default Google Calendar.

## Google Calendar Credentials
- Make sure you have credentials.json from the Google Cloud Console (with Calendar API enabled).
- The script automatically handles OAuth flow and saves a token.json so you won’t need to re-authorize every time.

## Customization
### Regex Patterns 
- In findDates.py, the date_pattern and time_pattern can be modified if your syllabus date/time formats differ.
### Events and Reminders
- The appendShort function in findDates.py defines how events are created and which reminders to set (e.g. 1-day and 2-day notifications).

## Limitations
### Syllabus Format Variations:
This script relies on specific date/time patterns to match. If a syllabus uses highly unusual date formatting or is a scanned PDF containing images rather than text, the parsing may fail or produce incorrect results. You may need to adjust the regex patterns or use different OCR tools for image-based PDFs.
### Date Range Assumptions:
The convertDate function assumes that dates from January to April belong to the next calendar year. This may not hold for all academic calendars.

## Troubleshooting
- Missing or Unfound Dates: If your PDF uses unusual date formats or is scanned as images, pdfminer.six may fail to extract text or the regex may miss matches
- Permission Errors: Ensure your Google Cloud project has Calendar API enabled. Check that your credentials.json is valid.

## Contributing
- Pull requests are welcome. For significant changes, please open an issue first to discuss what you’d like to modify.
