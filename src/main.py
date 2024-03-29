import argparse

from classes.extractData import ExtractData
from classes.getPosterLink import GetPosterLink
from classes.savePhoneNumbers import savePhoneNumbers
from init import init

if __name__ == "__main__":
    # Initial the arguments
    arg_pars = argparse.ArgumentParser(description='Scrap the data from divar')
    arg_pars.add_argument("--init", type=bool,
                          default=False, help='Initial the required files and database')
    arg_pars.add_argument("--start", type=bool,
                          default=False, help='start the scraper')
    arg_pars.add_argument("--saveNumbers", type=bool, default=False,
                          help="Save the unique and valid phone numbers from database")
    argpars = arg_pars.parse_args()
    if argpars.init:
        init()
    elif argpars.start:
        # Create instance of GetPosterLink
        get_poster_links = GetPosterLink(timeout=5)
        # Scrap the links
        get_poster_links.scrap_data()
        # Create instance of GetNumbers
        get_numbers = ExtractData()
        # Start the phone number scraper
        get_numbers.extract_data()
    elif argpars.saveNumbers:
        savePhoneNumbers()
    else:
        arg_pars.print_help()
