import requests
from src.html_scraper import WikipediaScraper
from requests.cookies import RequestsCookieJar

class CountryLeadersAPI:
    '''
    a class that resposible for cmmunicating with country leaders API.
    
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

    def close(self):
        """
        Close the HTTP session to release network resources.

        This method should be called manually when the API client 
        is no longer needed.
        """
        self.session.close()


    def refresh_cookie(self, old_cookies) -> RequestsCookieJar:

        '''
        Check wether current session cookie is still valid  and refreshe it when needed.

        :param old_cookies: the current session cookies used for authentication.
        :return: A valid RequestsCookieJar object containing active session cookies.
        '''
        # we use /leaders as 
        response = self.session.get(
            self.base_url + "leaders",
            params={"country": "fr"},
            cookies=old_cookies)
        
        # Check if old cookie is still valid 
        if response.status_code == 200:
            return old_cookies
        else:    
            return requests.get(self.base_url + "cookie").cookies 


    def get_countries(self, cookies) -> dict:
        '''
        Fetch the list of supported country codes from the API.

        This method sends a GET request to the /country endpoint and returns 
        the parsed JSON response.

        :param cookies: authentikation cookies used for the API requests.
        :returns: A dictionary of country codes.

        '''
        response = self.session.get(
        self.base_url + "countries",
        cookies=cookies)

        countries = response.json()

        return countries
    
    def get_leaders(self, country, cookies) :
        '''
        Fetch leaders for a given country and erich with the wikipedia summary.

        This method:
        - Ensures the session cookie is valid
        - Queries the API for leaders of tthe specified countriy
        - Scrapes wikipedia pages for each leader (if available)
        - Adds a "bio" field containing the first paragraph of wikipedia pages

        :param country: Country code (e.g., "fr", "us").
        :param cookies: Authentication cookies used for API requests.
        :return: A list of leader dictionaries enriched with a "bio" field.
        '''

        # Ensure we are using a valid authentication cookie before making API calls
        cookies = self.refresh_cookie(cookies)

        response = self.session.get(
            self.base_url + "leaders",
            params={"country": country},
            cookies=cookies)

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
