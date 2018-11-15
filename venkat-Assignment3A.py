import csv
from statistics import mean

# ------------------CONSTANTS
length = "length"
ProdCost = "ProdCost"
AlbumSales = "AlbumSales"
bandCol = 2
prod_cost_col = 3
album_sales_col = 4
# fileName = 'C:\\Users\\venkat\\Desktop\\ufa\\coursework\\week12\\Albums.csv'

# ------------------global variables
d = {}


def splitByBand(reader):
    """populates the global dictionary d as it reads each row in the reader variable"""
    try:
        total_prod_cost = 0
        total_album_sales = 0
        len = 0

        for row in reader:
            theDict = d[row[bandCol]]  # step1: gets the dictionary for the band

            al_sale = theDict[AlbumSales]  # step2 gets the list of album sales for the band
            al_sale.append(float(row[album_sales_col]))  #step3 appends current row value to the list
            theDict[AlbumSales] = al_sale #step4 updates the value to 'AlbumSales' key

            pc = theDict[ProdCost]  #step5 gets the list of production cost for the band
            pc.append(float(row[prod_cost_col]))  #step6 appends the current row value to the list
            theDict[ProdCost] = pc #step7 updates the value to 'ProdCost'
            d[row[bandCol]] = theDict  #step8 updates value for d with updated theDict
    except Exception as e:
        print('Exception in splitByBand')
        raise e

def initDictionary(bands):
    """initializes dictionary d.
    d has band-name as the key and dictionary as the value.
    value for each key is a dictionary and has two elements
    (ProdCost initialised to []--this will store prod cost for this band,
    AlbumSales initialised to []--this will store album sales for this band
    """
    for x in bands:
        d["{}".format(x)] = {ProdCost: [], AlbumSales: []}


def initBands(reader):
    """Gets unique set of band names from reader and
        initialises d to empty values."""
    bandsSet = []
    try:
        for row in reader:
            bandsSet.append(row[bandCol])
        bandsSet = set(bandsSet)
        initDictionary(bandsSet)
    except Exception as e:
        print('Exception in initBands')
        raise e

def init(fileName):
    """Read the csv file, initialises the d variable and calls splitByBand function"""
    global grand_prod_cost, grand_album_sales
    infile = ''
    try:
        with open(fileName, mode='r') as infile:
            reader = csv.reader(infile)
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(infile.read(2048))
            infile.seek(0)
            if (has_header):
               next(reader)  # move curser to next row so the header is not included
            initBands(reader)
            # Reset the curser to start based on presence of header
            if(has_header):
               infile.seek(0)
            # avoid header
               next(reader)
            else:
               infile.seek(0)
            splitByBand(reader)
    except Exception as e:
        print('Exception in init')
        raise e

def printValues():
    """Prints the required values to console both by band and overall"""
    grand_prod_cost = []
    grand_album_sales = []
    for x in d:
        print("----------------------------------------------")
        print("Statistics for Band '" + x + "'")
        thisDict = d[x]
        print("1)What is the total production cost of the album?  :", round(sum(thisDict[ProdCost]), 2))
        print("2)What is the total sales of the album?            :", round(sum(thisDict[AlbumSales]), 2))
        print("3)What is the average production cost of the album?:", round(mean(thisDict[ProdCost]), 2))
        print("4)What is the average of the album sale?           :", round(mean(thisDict[AlbumSales]), 2))
        print("5)Net Profit/Loss                                  :", round(sum(thisDict[AlbumSales]) - sum(thisDict[ProdCost]), 2))

        grand_prod_cost +=thisDict[ProdCost]
        grand_album_sales +=(thisDict[AlbumSales])

    print('**********************************************************************************')
    print('Statistics of all albums')
    print('1)What is the total production cost of all albums?  :', round(sum(grand_prod_cost), 2))
    print('2)What is the total sales of all albums?            :', round(sum(grand_album_sales), 2))
    print('3)What is the average production cost of all albums?:', round(mean(grand_prod_cost),2))
    print('4)What is the average of all album sales?           :', round(mean((grand_album_sales)),2))
    print('5)Net Profit/Loss                                   :', round((sum(grand_album_sales) - sum(grand_prod_cost)),2))
    print('**********************************************************************************')

#entry point for the program
while True:
    try:
        fileName = input("Enter the full path and name of the csv file:")
        if(fileName == ""):
            raise Exception("Enter File Name")
        init(fileName)
        printValues()
        break
    except Exception as e:
        print(e)
    else:
        print("Program successfully executed")
