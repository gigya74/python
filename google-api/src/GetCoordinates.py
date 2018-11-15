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
def init():
    """Opens a windowless gui for user to select a config.xml file"""
    global  apiKey , host , addresses
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    doc = untangle.parse(filename)
    apiKey = doc.root.myAPIKey.cdata.strip()
    host = doc.root.host.cdata.strip()
    addresses = doc.root.addresses.address
def printLatLong():
    """Prints the coordinates of the address supplied in the config.xml"""
    for address in addresses:
        a = address.cdata.strip() +" "+ address['CITY_STATE_ZIP']
        print(Fore.RESET+"The latitude and longiture for ",a," is:::"+Fore.CYAN)
        coordinates = get_coordinates(a)
        print(coordinates)
        print(Fore.RESET+" Printing the formatted address by passing the coordinates to googles geocode api"+Fore.YELLOW)
        print(reverseGeoCode(coordinates))

def get_coordinates(address):
    """Gets the coordinates of addresses supplied in the config.xml by invoking google api"""
    url = host + "?address=" + address+ "&key=" + apiKey
    response = requests.request('GET', url)
    geo = response.json()
    results = geo['results'][0]
    return [results['geometry']['location']['lat'],results['geometry']['location']['lng']]

def reverseGeoCode(coordinates):
    """Gets the formatted address by using lat and long. Invokes Googles geocode api"""
    c0 = repr(coordinates[0])
    c1 = repr(coordinates[1])
    url = host + "?latlng="+c0+','+c1+"&key=" + apiKey
    response = requests.request('GET', url)
    geo = response.json()

    answer = geo['results'][0]
    return answer.get('formatted_address')

try:
    init()
    printLatLong()
except Exception as e:
    print('Exception generated::: ',e)
