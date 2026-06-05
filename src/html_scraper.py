import requests
from requests import Session
from bs4 import BeautifulSoup
import json
import re

class WikipediaScraper:
    """
    Class that can download and parse HTML documents
    """
    def __init__(self, session : Session = Session()) -> None:
        """
        Constructor that creates a wikipedia scraper with a session.

        :param session: Requests session to query the wikipedia page.
        """
        self.session = session

    def fetch_html(self, url : str) -> str:
        """
        Method that requests raw HTML text.

        :param url: A string with the url of the html to request.
        :return: A string with the html text.
        """
        try:
            # header is used to tell the website that the script is not from automated bot
            headers = {"User-Agent":"Mozilla/5.0"}
            response = self.session.get(url, headers = headers)
            return response.text
        except (requests.exceptions.HTTPError, requests.exceptions.ReadTimeout) as err:
            print(err.args[0])
            return ""
    
    def clean_text(self, text: str) -> str:
        """
        Method that cleans a text by stripping out unwanted characters, whitespace, or Wikipedia citation brackets.
        
        :param text: A string with the text to clean.
        :return: A string with the cleaned text.
        """
        text = text.strip() # remove end of line at the end of the text
        text = re.sub(r'\[.*\]',"",text) # remove references between brackets
        text = re.sub(r'\s+',' ',text) # replace no-break spaces
        text = re.sub(r'ⓘ','',text) # removes info icon
        return text

    def get_first_paragraph(self, html: str) -> str:
        """
        Method that parses raw HTML with BeautifulSoup, finds the first true biographical narrative paragraph, and returns it.
        
        :param html: A string with the html
        """
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")
        for par in paragraphs:
            # assume first paragraph begins with bold tag and has more than 30 characters
            if re.match(r'^<p(?: id="[a-zA-Z]{4}")?><b(?: id="[a-zA-Z]{4}")?>', str(par)) and len(par.text) > 30:
                return self.clean_text(par.text)
        for par in paragraphs:
            # if not found, take the first paragraph with at least 120 characters
            if len(par.text) > 120:
                return self.clean_text(par.text)
        print("Could not find first paragraph of :")
        print(paragraphs[0].text)
        return ""
    
    @staticmethod
    def to_json_file(filepath: str, dictionary : dict) -> None :
        """
        Method that stores the data structure into a JSON file.

        :param filepath: A string with the file path where the json is stored.
        :param dictionary: A dictionary that is stored in the json file.
        """
        with open(filepath,"w") as file:
            json.dump(dictionary, file, ensure_ascii=False)
