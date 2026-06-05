from src import api_client, html_scraper

def main() -> None: 

    # Initialize the countryLeadersAPI module
    api= api_client.CountryLeadersAPI()

    # Retrieve countries
    countries = api.get_countries()

    # Retrieve leaders from countries
    leaders_per_country = {}

    for country in countries:
        print (f"We are looking for leaders in {country}")
        leaders = api.get_leaders(country)
        leaders_per_country[country] = leaders
        

    # Initialize the scraper engine
    scraper = html_scraper.WikipediaScraper()

    scraper.to_json_file("leaders.json", leaders_per_country)

if __name__ == "__main__":
    main()