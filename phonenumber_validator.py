#!/usr/bin/env python

"""
This program validates international phone numbers by using a Python port of
Google's libphonenumber library.

https://github.com/daviddrysdale/python-phonenumbers

Functions:

parse - parses input phone number into country code and national number
isPossibleNumber - quickly guesses whether a number is a possible phone number
    by using only the length information, much faster than a full validation.
isValidNumber - full validation of a phone number for a region using length
    and prefix information.
carrier.name_for_number - displays the original carrier of the phone number (if possible)
geocoder.country_name_for_number - displays the origin country of the phone number (if possible)

Requirements:

Input file needs to have the following attributes/columns (see sample file):
"cn","mail","mobile","userPrincipalName","sAMAccountName"

Encoding of Input file needs to be set to UTF-8

Phone numbers have to be provided in E.164 format
"""

__author__ = "buzz1n6m4xx"
__status__ = "Production"
__version__ = "0.1"

# =============================================================================
#  MODULES
# =============================================================================

import csv # https://docs.python.org/3/library/csv.html
from os import getcwd
import phonenumbers
from phonenumbers import carrier, geocoder

# =============================================================================
#  VARIABLES
# =============================================================================

numbers = []
directory = getcwd()

# CSV FILE SETTINGS
outputfile = "checkednumbers.csv"
fieldnames = ["cn", "sAMAccountName", "userPrincipalName", "mail", "mobile", \
           "country", "carrier", "validnumber", "possiblenumber", "checked"]

# TEXT OPTIONS
TXTCOLRST = "\x1b[0;0m"
TXTCOLGR = "\x1b[1;32m"
TXTCOLRD = "\x1b[1;31m"

# OPEN AND SAVE INPUT FILE
with open('phonenumbers.csv', 'r', encoding="utf8") as prepfile:\
    # UTF8 needed for special characters
    reader = csv.DictReader(prepfile, delimiter = ',')
    # DictReader to address columns by fieldnames (first row)
    for row in reader:
        numbers.append(row)

with open("checkednumbers.csv", "w", newline="") as csvfile:

    csvwriter = csv.DictWriter(csvfile, fieldnames, delimiter = ',')
    # DictWriter to write fieldnames and rows
    csvwriter.writeheader() # Write fieldnames

    print(TXTCOLGR + "\n... Validating numbers ..." + TXTCOLRST)

    for number in numbers:

        csvcn=number["cn"]
        cssam=number["sAMAccountName"]
        csvupn=number["userPrincipalName"]
        csvmail=number["mail"]
        csvnumber=number["mobile"]

        if csvnumber in [" ", ""]:
            print("\n" + TXTCOLRD + "Number   : " + "N/A")
            print("Error    : Phone number is missing." \
                  + TXTCOLRST)
            CHECKED="False"
            csvwriter.writerow({"cn": csvcn, "sAMAccountName": cssam, "userPrincipalName": \
                                csvupn, "mail": csvmail, "mobile": csvnumber, "country": \
                                    "N/A", "carrier": "N/A", "validnumber": "N/A", \
                                        "possiblenumber": "N/A", "checked": CHECKED})
        else:
            try:
                parsed_number = phonenumbers.parse(number["mobile"]) # Address "mobile" column
                possible = (phonenumbers.is_possible_number(parsed_number)) # Quick check
                valid = (phonenumbers.is_valid_number(parsed_number)) # Full check
                country = geocoder.country_name_for_number(parsed_number, "en")
                net = carrier.name_for_number(parsed_number, "en")
                print("\nNumber   : " + number["mobile"])
                print("Country  : " + country)
                print("Carrier  : " + net)
                print("Possible : " + str(possible))
                print("Valid    : " + str(valid))
                CHECKED="True"
                csvwriter.writerow({"cn": csvcn, "sAMAccountName": cssam, \
                                    "userPrincipalName": csvupn, "mail": csvmail, \
                                        "mobile": csvnumber, "country": country, \
                                            "carrier": net, "validnumber": valid, \
                                            "possiblenumber": possible, "checked": CHECKED})
            except:
                print("\n" + TXTCOLRD + "Number   : " + number["mobile"])
                print("Error    : Invalid phone number or format. Number could not be parsed." \
                      + TXTCOLRST)
                CHECKED="False"
                csvwriter.writerow({"cn": csvcn, "sAMAccountName": cssam, \
                                    "userPrincipalName": csvupn, "mail": csvmail, \
                                        "mobile": csvnumber, "country": country, \
                                            "carrier": net, "validnumber": valid, \
                                            "possiblenumber": possible, "checked": CHECKED})
                pass
print(TXTCOLGR + "\n... Validation finished ...\n")
print(outputfile + " has been saved to " + directory + TXTCOLRST)
