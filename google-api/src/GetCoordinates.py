The below program does the following in sequence:
#1)invokes init and user is made to select the config.xml file, reads the file, prints the contents.
    #(makes use of untangle python xml package to read the config .xml)
#2)invokes printLatLong, passes the addresses it has got from step 1 and gets coordinates. Prints coordinates
    #(invokes google maps api to get coordinates)
#3)invokes printFormattedAddress, passes coordinates it has got from step2 and gets address. Prints address
    #(invokes google maps api to get address)

import googlemaps
import requests
import json
from colorama import init, Fore, Back
import untangle
from tkinter import *
from tkinter.filedialog import askopenfilename

apiKey = ''
host = ''
addresses = {}
coordinates = []


def init():
    """Opens a windowless gui for user to select a config.xml file"""
    global apiKey, host, addresses
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    doc = untangle.parse(filename)
    apiKey = doc.root.GoogleAPIKey.cdata.strip()
    print("----------------------------------------------------------------------------------------------")
    print("1)Printing the contents of the xml")
    print("----------------------------------------------------------------------------------------------")
    print("apiKey is :"+apiKey)
    host = doc.root.host.cdata.strip()
    print("host is :"+host)
    addresses = doc.root.addresses.address
    print("addresses are :")
    for address in addresses:
        print(address['name']+" "+address['CITY_STATE_ZIP']+" "+address.cdata.strip())


def printLatLong():
    """Prints the coordinates of the address supplied in the config.xml"""
    global coordinates
    print("\n\n**********************************************************************************************")
    print("2)Printing the coordinates by passing the address to googles geocode api")
    print("**********************************************************************************************")
    for address in addresses:
        a = address.cdata.strip() + " " + address['CITY_STATE_ZIP']
        print(Fore.RESET + "The latitude and longiture for ", a, " is:::" + Fore.CYAN)
        c = get_coordinates(a)
        print(c)
        coordinates.append(c)


def get_coordinates(address):
    """Gets the coordinates of addresses supplied in the config.xml by invoking google api"""
    url = host + "?address=" + address + "&key=" + apiKey
    response = requests.request('GET', url)
    geo = response.json()
    results = geo['results'][0]
    return [results['geometry']['location']['lat'], results['geometry']['location']['lng']]


def printFormattedAddress():
    """ Invokes google api, gets address from coordinates and Prints formatted address"""
    print(Fore.RESET)
    print("----------------------------------------------------------------------------------------------")
    print("3)Printing the address by passing the coordinates to googles geocode api")
    print("----------------------------------------------------------------------------------------------")
    for c in coordinates:
        print(Fore.RESET+"Address for coordinates:")
        print(c)
        print("is"+Fore.YELLOW)
        print(reverseGeoCode(c))

def reverseGeoCode(coordinates):
    """Gets the formatted address by using lat and long. Invokes Googles geocode api"""
    c0 = repr(coordinates[0])
    c1 = repr(coordinates[1])
    url = host + "?latlng=" + c0+","+c1+"&key=" + apiKey
    response = requests.request('GET', url)
    geo = response.json()

    answer = geo['results'][0]
    return answer.get('formatted_address')


try:
    init()
    printLatLong()
    printFormattedAddress()
except Exception as e:
    print('Exception generated::: ', e)
