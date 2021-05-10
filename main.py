from classes.getPosterLink import GetPosterLink
from classes.getNumbers import GetNumbers

if __name__ == "__main__":
    # Create instance of GetPosterLink
    get_poster_links = GetPosterLink(timeout=5)
    # Scrap the links
    get_poster_links.scrapData()
    # Save the scraped links
    get_poster_links.saveLinks()
    # Create instance of GetNumbers
    get_numbers = GetNumbers()
    # Start the phone number scraper
    get_numbers.extract_phone_numbers()
