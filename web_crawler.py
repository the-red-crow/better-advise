import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from typing import List

class WebCrawler():
    def __init__(self, catalog_url = "https://catalog.columbusstate.edu/course-descriptions/cpsc/"):
        self.catalog_url = catalog_url
        self._data = self.get_course_data()

    def get_course_data(self):
        """Scrapes CSU CPSC catalog and extracts course details with prerequisites."""

        # Step 1: Fetch HTML
        print("Connecting to catalog...")
        page = requests.get(self.catalog_url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")

        extracted = []

        # Step 2: Iterate through all course blocks
        for block in soup.select("div.courseblock"):
            header = block.select_one("div.cols.noindent")
            if not header:
                continue

            code = header.select_one("span.detail-code strong").get_text(strip=True)
            title = header.select_one("span.detail-title strong").get_text(strip=True)
            prereq_list = []

            # Step 3: Search for prerequisite text in the course description
            for desc in block.select("div.courseblockextra"):
                text = desc.get_text(" ", strip=True)
                if "Prerequisite" in text:
                    text = (text
                        .replace("\xa0", " ")   # non-breaking space
                        .replace("Â", " ")      # stray symbol
                        .replace("¬†", " ")     # alternate non-breaking space
                        .encode("utf-8", "ignore")
                        .decode("utf-8"))
                    # Clean text and extract all course codes like CPSC 1301K, MATH 1113, etc.
                    cleaned = re.sub(r"[^A-Za-z0-9\s]", " ", text)
                    matches = re.findall(r"[A-Z]{4}\s?\d{4}[A-Z]?", cleaned)
                    prereq_list.extend(matches)

            prereq_list = list(dict.fromkeys(prereq_list))  # remove duplicates

            extracted.append({
                "Course_Code": code,
                "Course_Title": title,
                "Prerequisites": ", ".join(prereq_list) if prereq_list else ""
            })

        return extracted

    def save_to_csv(self, data, output_file="cpsc_prerequisites.csv"):
        """Stores the parsed data into a CSV file."""
        df = pd.DataFrame(data, columns=["Course_Code", "Course_Title", "Prerequisites"])
        if os.path.exists(output_file):
            os.remove(output_file)
        df.to_csv(output_file, index=False, encoding="utf-8")
        print(f" File saved: {output_file} ({len(df)} courses)")

    def quick_test(self):
        results = self.get_course_data()
        self.save_to_csv(results)

    def crawl_course_prerequisites(self, course_code: str) -> List[str]:
        course = [x for x in self._data if x.get("Course_Code") == course_code]
        return course[0].get("Prerequisites").split(", ")
