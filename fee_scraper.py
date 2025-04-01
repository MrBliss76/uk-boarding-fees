import requests
from bs4 import BeautifulSoup

SCHOOL_FEES_PAGES = {
    "Eton College": "https://www.etoncollege.com/admissions/fees/",
    "Harrow School": "https://www.harrowschool.org.uk/admissions/fees/",
    "Winchester College": "https://www.winchestercollege.org/admissions/fees",
    "Cheltenham Ladies’ College": "https://www.cheltladiescollege.org/admissions/fees/",
    "Westminster School": "https://www.westminster.org.uk/admissions/fees/"
}

def fetch_school_fees(school_name):
    url = SCHOOL_FEES_PAGES.get(school_name)
    if not url:
        return {"error": "School not found"}

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        fee_lines = []
        for tag in soup.find_all(["p", "li"]):
            text = tag.get_text(separator=" ", strip=True)
            if any(word in text.lower() for word in ["fee", "term", "boarding", "day", "registration", "deposit", "tuition", "per term", "£"]):
                fee_lines.append(text)

        return {
            "school": school_name,
            "url": url,
            "fees": fee_lines if fee_lines else ["No fee info found on page."]
        }

    except Exception as e:
        return {"error": str(e)}
