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
    apiKey = doc.root.GoogleAPIKey.cdata.strip()
    host = doc.root.host.cdata.strip()
    addresses = doc.root.addresses.address
def printLatLong():
    """Prints the coordinates of the address supplied in the config.xml"""
    for address in addresses:
        a = address.cdata.strip() +" "+ address['CITY_STATE_ZIP']
        print(Fore.RESET+"The latitude and longiture for ",a," is:::"+Fore.CYAN)
        print(get_coordinates(a))

def get_coordinates(address):
    """Gets the coordinates of addresses supplied in the config.xml by invoking google api"""
    url = host + "?address=" + address+ "&key=" + apiKey
    response = requests.request('GET', url)
    geo = response.json()
    results = geo['results'][0]
    return [results['geometry']['location']['lat'],results['geometry']['location']['lng']]

try:
    init()
    printLatLong()
except Exception as e:
    print('Exception generated::: ',e)