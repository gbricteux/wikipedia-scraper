import requests
from src.html_scraper import WikipediaScraper

class CountryLeadersAPI:
    '''
    a class that responsible for communicating with country leaders API.
    
    This class handels API requests, session management, and endpoint configuration
    for retrieving information about countries and leaders.
    '''
    def __init__(self):
        '''
        Initialize a countryLeadersAPI object.
        
        This constructor sets the API base URL, defines the available endpoints,
        and creates a persistent requests sessions for handling HTTP requests.
        '''

        self.base_url = "https://country-leaders.onrender.com/"
        self.country_endpoint = "countries"
        self.cookies_endpoint = "cookie"
        self.leaders_endpoint = "leaders"
        self.session = requests.Session()

        self.cookies = requests.get(self.base_url + self.cookies_endpoint).cookies

    def close(self):
        """
        Close the HTTP session to release network resources.

        This method should be called manually when the API client 
        is no longer needed.
        """
        self.session.close()


    def refresh_cookie(self) -> None:

        '''
        Check wether current session cookie is still valid  and refreshe it when needed.
        '''
        # we use /leaders as 
        response = self.session.get(
            self.base_url + self.country_endpoint,
            cookies=self.cookies)
        
        # Check if old cookie is still valid 
        if response.status_code != 200:
            self.cookies = requests.get(self.base_url + self.cookies_endpoint).cookies 

    def get_countries(self) -> dict:
        '''
        Fetch the list of supported country codes from the API.

        This method sends a GET request to the /country endpoint and returns 
        the parsed JSON response.

        :returns: A dictionary of country codes.
        '''
        
        self.refresh_cookie()
        response = self.session.get(
        self.base_url + self.country_endpoint,
        cookies=self.cookies)

        countries = response.json()

        return countries
    
    def get_leaders(self, country: str) -> list:
        '''
        Fetch leaders for a given country and erich with the wikipedia summary.

        This method:
        - Ensures the session cookie is valid
        - Queries the API for leaders of tthe specified countriy
        - Scrapes wikipedia pages for each leader (if available)
        - Adds a "bio" field containing the first paragraph of wikipedia pages

        :param country: Country code (e.g., "fr", "us").
        :return: A list of leader dictionaries enriched with a "bio" field.
        '''

        # Ensure we are using a valid authentication cookie before making API calls
        self.refresh_cookie()

        response = self.session.get(
            self.base_url + self.leaders_endpoint,
            params={"country": country},
            cookies=self.cookies)

        leaders = response.json()

        enriched_leaders = []

        # Wikipedia scraper is reused to avoid recreating it for every leader
        wikipedia_scraper = WikipediaScraper(self.session)

        for leader in leaders:
            url = leader.get("wikipedia_url")
            if url:
                try:
                    html = wikipedia_scraper.fetch_html(url)
                    # extract only the first paragraph as a short biography
                    first_paragraph = wikipedia_scraper.get_first_paragraph(html)
                                   
                    leader["bio"] = first_paragraph
                except Exception:
                    # No wikipedia page available
                    leader["bio"] = None
            enriched_leaders.append(leader)
        return enriched_leaders
