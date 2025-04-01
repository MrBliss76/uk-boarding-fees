import requests
from bs4 import BeautifulSoup

SCHOOL_FEES_PAGES = {
    "Eton College": "https://www.etoncollege.com/admissions/fees/",
    "Harrow School": "https://www.harrowschool.org.uk/admissions/fees/",
    "Winchester College": "https://www.winchestercollege.org/admissions/fees",
    "Cheltenham Ladies’ College": "https://www.cheltladiescollege.org/admissions/fees/",
    "Westminster School": "https://www.westminster.org.uk/admissions/fees/"
}

KEYWORDS = ["fee", "fees", "term", "boarding", "day", "registration", "deposit", "tuition", "per term", "£"]

def fetch_school_fees(school_name):
    url = SCHOOL_FEES_PAGES.get(school_name)
    if not url:
        return {"error": "School not found"}

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        fee_lines = []
        for tag in soup.find_all(["p", "li", "div", "span", "h2", "h3"]):
            text = tag.get_text(separator=" ", strip=True)
            if any(keyword in text.lower() for keyword in KEYWORDS) and "cookie" not in text.lower():
                fee_lines.append(text)

        return {
            "school": school_name,
            "url": url,
            "fees": list(dict.fromkeys(fee_lines)) or ["No fee info found on page."]
        }

    except Exception as e:
        return {"error": str(e)}
