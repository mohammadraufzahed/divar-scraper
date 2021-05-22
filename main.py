from classes.getPosterLink import GetPosterLink
from classes.extractData import ExtractData

if __name__ == "__main__":
    # Create instance of GetPosterLink
    get_poster_links = GetPosterLink(timeout=5)
    # Scrap the links
    get_poster_links.scrap_data()
    # Create instance of GetNumbers
    get_numbers = ExtractData()
    # Start the phone number scraper
    get_numbers.extract_data()
