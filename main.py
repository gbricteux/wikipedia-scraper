from src.api_client import CountryLeadersAPI
from src.html_scraper import WikipediaScraper

def main() -> None: 

    # Initialize the countryLeadersAPI module
    api = CountryLeadersAPI()

    # Retrieve countries
    countries = api.get_countries()

    # Retrieve leaders from countries
    leaders_per_country = {}

    for country in countries:
        print (f"We are looking for leaders in {country}")
        leaders = api.get_leaders(country)
        leaders_per_country[country] = leaders
        

    # Initialize the scraper engine
    scraper = WikipediaScraper()

    scraper.to_json_file("leaders.json", leaders_per_country)


if __name__ == "__main__":
    main()