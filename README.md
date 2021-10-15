# phonenumber.validator

Phone Number Validator
**********************
 
This program validates international phone numbers by using a Python port of
Google's libphonenumber library:
https://github.com/daviddrysdale/python-phonenumbers
https://github.com/google/libphonenumber

Functions:

• parse - parses input phone number into country code and national number
• isPossibleNumber - quickly guesses whether a number is a possible phone number
  by using only the length information, much faster than a full validation.
• isValidNumber - full validation of a phone number for a region using length
  and prefix information.
• carrier.name_for_number - displays the original carrier of the phone number (if possible)
• geocoder.country_name_for_number - displays the origin country of the phone number (if possible)

Requirements:

• Input file needs to have the following attributes/columns (see sample file):
  "cn","mail","mobile","userPrincipalName","sAMAccountName"
• Encoding of Input file needs to be set to UTF-8
• Phone numbers have to be provided in E.164 format
