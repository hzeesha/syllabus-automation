import re
from pdfminer.high_level import extract_pages, extract_text
from datetime import datetime, timedelta
import tzlocal
from dateutil import parser

course_code = "CS1234" # Enter course code here. Current input is a sample
timeZone = tzlocal.get_localzone()

text = extract_text("syllabus.pdf") # Enter .pdf file here. Current input is a sample

date_pattern = r'|'.join([
    r'\b(?:Jan\.|Feb\.|Mar\.|Apr\.|May|Jun\.|Jul\.|Aug\.|Sep\.|Oct\.|Nov\.|Dec\.)\s*\d{1,2}',  # Format: "Oct. 9"
    r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}',  # Format: "October 9"
    r'\b\d{1,2}/\d{1,2}',  # Format: "10/9"
    r'\b\d{1,2}(?:st|nd|rd|th)\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',  # Format: "9th Oct"
    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),?\s+\d{1,2}\b', # Format: Oct, 9
    r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{1,2}(?:st|nd|rd|th)?' # Format: October, 9th
])

# Adjusted time pattern to capture time ranges with hyphens
time_pattern = r"(\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)(?:\s*-\s*(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?))?"

def convertDate(date):
    """
        Converts a date string into the format 'YYYY-MM-DD'.
        If the month is January through April, the year is incremented to the next year.

        Args:
            date (str): Date string to convert.

        Returns:
            str: Formatted date string in 'YYYY-MM-DD'.
    """
    current_year = datetime.now().year
    tempDate = parser.parse(date)
    if tempDate.month <= 4:
        current_year += 1
    full_date = f"{date} {current_year}"
    parsed_date = parser.parse(full_date)
    return parsed_date.strftime("%Y-%m-%d")


def convertDateTime(date, time):
    date = datetime.strptime(date, "%Y-%m-%d")

    # Insert a space between the time and AM/PM if missing
    time = re.sub(r'(\d)([APMapm]{2})', r'\1 \2', time)

    time_parts = time.split()
    time_str = time_parts[0]
    am_pm = time_parts[1] if len(time_parts) > 1 else ''

    hours, minutes = map(int, time_str.split(":"))
    if am_pm.upper() == "PM" and hours != 12:
        hours += 12
    if am_pm.upper() == "AM" and hours == 12:
        hours = 0

    final_datetime = date + timedelta(hours=hours, minutes=minutes)
    return final_datetime.isoformat()

def appendShort(item, yourList, date, time=None, end_time=None):
    if time:
        start_time_iso = convertDateTime(date, time)
        if end_time:
            end_time_iso = convertDateTime(date, end_time)
        else:
            end_time_iso = start_time_iso  # If no end time, use start time as end
        yourList.append({
            "summary": course_code + " " + item,
            "start": {
                "dateTime": start_time_iso,
                "timeZone": str(timeZone),
            },
            "end": {
                "dateTime": end_time_iso,
                "timeZone": str(timeZone),
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 24 * 60},  # Reminder 1 day before
                    {"method": "email", "minutes": 48 * 60},  # Email reminder 2 days before
                ],
            },
        })
    else:
        yourList.append({
            "summary": course_code + " " + item,
            "start": {
                "date": date,
                "timeZone": str(timeZone),
            },
            "end": {
                "date": date,
                "timeZone": str(timeZone),
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 24 * 60},
                    {"method": "email", "minutes": 48 * 60},
                ],
            },
        })

def process_event(event_type, line, due_dates):
    date_match = re.search(date_pattern, line)
    if date_match:
        date = convertDate(date_match.group(0))
        time_match = re.search(time_pattern, line)
        if time_match:
            start_time = time_match.group(1)
            end_time = time_match.group(2) if time_match.group(2) else None
            appendShort(event_type, due_dates, date, start_time, end_time)
        else:
            appendShort(event_type, due_dates, date)

lines = text.splitlines()
date_lines = [course_code + " " + line for line in lines if re.search(date_pattern, line)]

due_dates = []

for line in date_lines:
    if "assignment" in line.lower():
        process_event("Assignment Due", line, due_dates)
    if "final" in line.lower():
        process_event("FINAL EXAM", line, due_dates)
    if "mid term" in line.lower() or "midterm" in line.lower():
        process_event("MID TERM", line, due_dates)
    if "test" in line.lower():
        process_event("Test Due", line, due_dates)
    if "quiz" in line.lower():
        process_event("Quiz Due", line, due_dates)
    if "lab" in line.lower():
        process_event("Lab Due", line, due_dates)