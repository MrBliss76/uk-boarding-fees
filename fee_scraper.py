import requests
from bs4 import BeautifulSoup
import re

SCHOOL_FEES_PAGES = {
    "Eton College": "https://www.etoncollege.com/admissions/fees/",
    "Harrow School": "https://www.harrowschool.org.uk/admissions/fees/",
    "Winchester College": "https://www.winchestercollege.org/admissions/fees",
    "Cheltenham Ladies’ College": "https://www.cheltladiescollege.org/admissions/fees/",
    "Westminster School": "https://www.westminster.org.uk/admissions/fees/"
}

# Regex to extract clean fee lines
FEE_REGEX = re.compile(r"£[0-9,]+(?:\.[0-9]{2})?.*?(term|half|year|annum|per)", re.IGNORECASE)

def fetch_school_fees(school_name):
    url = SCHOOL_FEES_PAGES.get(school_name)
    if not url:
        return {"error": "School not found"}

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        matches = []
        for tag in soup.find_all(["p", "li", "div", "span"]):
            text = tag.get_text(separator=" ", strip=True)
            if "£" in text:
                found = FEE_REGEX.findall(text)
                if found:
                    matches.append(text)

        # Remove duplicates and sort by length (shorter = more concise)
        unique_fees = sorted(set(matches), key=len)

        return {
            "school": school_name,
            "url": url,
            "fees": unique_fees[:5] or ["No core fees found."]
        }

    except Exception as e:
        return {"error": str(e)}
