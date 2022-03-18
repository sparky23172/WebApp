#!/usr/bin/python3

# Native
import subprocess
import argparse
import requests
import logging
import time
import re

#Non-Native
from selenium.common.exceptions import TimeoutException
from selenium import webdriver 
from zapv2 import ZAPv2

DEBUG = False


def get_args():
    parser = argparse.ArgumentParser(description='Bearer Token Fetcher')
    parser.add_argument('-u', '--url', dest='url', help='URL to go to')
    parser.add_argument('-p', '--password', dest='password', help='Password to login with')
    parser.add_argument('-U', '--user', dest='user', help='Username to login with')
    parser.add_argument("-d","--debug",dest="debug",action="store_true",help="Turn on debugging",default=False)
    parser.add_argument("-t","--timing",dest="timing",help="Time to wait for ZAP Proxy to load",default=20, type=int, choices=range(0,120))
    args=parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        global DEBUG
        DEBUG = True
    else:
        logging.basicConfig(level=logging.INFO)

    return args


def zap(url, email, password, timing):
    """ Takes a URL with protocol

    """
    logging.info("Starting ZAP intercept")

    logging.info("Sleeping to get ZAP up")
    output = subprocess.Popen(["zaproxy"])
    time.sleep(timing)
    print(output)
    print("Onwards")

    # Key needed to access ZAP
    apiKey = 'changeme'

    # "Project" name
    sessionName = "1SpookyCats"
    
    # Context (Scope)
    contextName = "spooky_little_cats"

    # By default ZAP API client will connect to port 8080
    zap = ZAPv2(apikey=apiKey)
    core = zap.core

    # Creating "Project"
    logging.debug('Create ZAP session: ' + sessionName + ' -> ' + core.new_session(name=sessionName, overwrite=True))
    context = zap.context

    "Creating Scope"
    logging.debug('Create ZAP context: ' + contextName + ' -> ' + context.new_context(contextname=contextName))

    try:
        PROXY = "127.0.0.1:8080"

        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
        }

        driver = webdriver.Firefox()
        options = webdriver.FirefoxOptions()
        options.set_preference("javascript.enabled", True)

        driver.get(url)
        
        time.sleep(5)
        
        redirect = driver.current_url

        # Default notes set to None so that in case nothing is found, it won't be a sad panda

        logging.debug("Base URL: {} vs Final URL: {}".format(url,redirect))

        if "Login" in redirect:
            # I am on a login page.
            logging.info("Login detected")

            # Typing in email address after finding it
            search_box = driver.find_element_by_name("username")
            search_box.send_keys(email)
            driver.find_element_by_id("submitButton").click()

            logging.debug("URL: {}".format(url))
            
            # Typing in password after finding it
            search_box = driver.find_element_by_name("password")
            search_box.send_keys(password)

            # Waiting 2 seconds so that it will let me click        
            logging.debug("Waiting 2 seconds")
            time.sleep(2)

            logging.debug("Going down a rabbit hole")
            
            # Clicking login button
            try:
                driver.find_element_by_id("submitButton").click()
            except TimeoutException:
                logging.debug("Ded af")
                
            logging.debug("Out of the rabbit hole")

        # ZAP portion to access findings
        headers = {
        'Accept': 'application/json',
        'X-ZAP-API-Key': apiKey
        }

        r = requests.get('http://127.0.0.1:8080/JSON/search/view/messagesByResponseRegex/', params={
        'regex': 'access_token.+?id_token',
        }, headers = headers)
        
        # Close browser
        driver.close()

        # Variable to hold json 
        token_json = ""

        for x in r.json()["messagesByResponseRegex"]:
            if "access_token" in str(x["responseBody"]):

                # Check to make sure I didn't catch js creating json string
                tp = re.findall(r'({\"access_token.+?id_token.+?}$)', str(x["responseBody"]))
                
                if tp:
                    logging.debug("Access Token Found")
                    logging.debug("JSON: {}".format(x["responseBody"]))
                    token_json = tp[0]
    
        if token_json:
            print(token_json)
        else:
            print("No token found")
    
        # Shutting down ZAP
        print('Shutdown ZAP -> ' + core.shutdown())
        
    except KeyError as e:
        logging.error("KeyError: {}".format(e))
        driver.quit()


def main():
    options = get_args()
    zap(options.url, options.user, options.password)


if __name__ == "__main__":
    main()
