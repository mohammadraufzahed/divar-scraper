from classes.getPosterLink import GetPosterLink

if __name__ == "__main__":
    # Create instance of GetPosterLink
    get_poster_links = GetPosterLink(timeout=5)
    # Scrap the links
    get_poster_links.scrapData()
    # Save the scraped links
    get_poster_links.saveLinks()
