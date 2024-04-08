import pandas as pd
import os
import matplotlib.pyplot as plt

#Merge files in Sales_Data
def concatenateAllSalesData():
    files = [file for file in os.listdir("/Users/knune/IdeaProjects/Pandas-Data-Science-Tasks/SalesAnalysis/Sales_Data")]
    allMonthsData = pd.DataFrame()

    for file in files:
        #print(file)
        monthData = pd.read_csv("/Users/knune/IdeaProjects/Pandas-Data-Science-Tasks/SalesAnalysis/Sales_Data/" + file)
        allMonthsData = pd.concat([allMonthsData, monthData])

    allMonthsData = allMonthsData.drop(allMonthsData[allMonthsData['Order ID'] == 'Order ID'].index)
    allMonthsData.to_csv("/Users/knune/IdeaProjects/Pandas-Data-Science-Tasks/SalesAnalysis/Output/Kaanjaree/allMonth.csv", index=False)

    return allMonthsData

def writeToCSV(df, path):
    df.to_csv(path)

def concatenateTwoFiles():
    df1 = pd.read_csv("/Users/knune/IdeaProjects/Pandas-Data-Science-Tasks/SalesAnalysis/Sales_Data/Sales_April_2019.csv")
    df2 = pd.read_csv("/Users/knune/IdeaProjects/Pandas-Data-Science-Tasks/SalesAnalysis/Sales_Data/Sales_August_2019.csv")
    twoMonths = pd.concat([df1, df2], ignore_index=True)
    writeToCSV(twoMonths, "/Users/knune/IdeaProjects/Pandas-Data-Science-Tasks/SalesAnalysis/Output/Kaanjaree/twoMonth.csv")

def readAllMonthData():
    df = pd.read_csv("/Users/knune/IdeaProjects/Pandas-Data-Science-Tasks/SalesAnalysis/Output/Kaanjaree/allMonth.csv")
    print(df.head())
    return df

def findBestSalesMonth():
    allMonthData = readAllMonthData()

    #Dropping NaN rows
    allMonthData = allMonthData.dropna(how='any')

    #Add month column
    allMonthData['Month'] = allMonthData['Order Date'].str[0:2]
    allMonthData['Month'] = allMonthData['Month'].astype('int32')

    #Add Sales Column and populate values to it
    allMonthData['Total Sales'] = allMonthData['Quantity Ordered'] * allMonthData['Price Each']

    #Find total sales value per month
    total_sales = allMonthData['Total Sales'].groupby(allMonthData['Month'])
    sorted_series = total_sales.sum().sort_values(ascending = False)
    dict = sorted_series.iloc[:1].to_dict()


    #Show visualization
    results = total_sales.sum()
    months = range(1, 13)
    plt.plot(months, results)
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.show()

    return dict


def getCity(address):
    city = address.split(",")[1]
    return city

def getState(address):
    state = address.split(",")[2].split(" ")[1]
    return state

def findBestSalesCity():
    allMonthsData = readAllMonthData()

    allMonthsData = allMonthsData.dropna(how='any')

    #Find city based on address and create City column
    allMonthsData["Count"] = allMonthsData['Purchase Address'].apply(lambda x: str(x).count(",") == 0)



    print(allMonthsData['Count'].value_counts())
    allMonthsData['City'] = allMonthsData['Purchase Address'].apply(lambda x: getCity(str(x)) + " (" + getState(str(x)) + ")" if str(x).count(",") == 2 else x)
    print(allMonthsData.head(10))

    #Create Total Sales column
    allMonthsData['Total Sales'] = allMonthsData['Quantity Ordered'] * allMonthsData['Price Each']

    #Figure out total sales for each city
    total_sales = allMonthsData['Total Sales'].groupby(allMonthsData['City'])
    results = total_sales.sum()
    sorted_series = results.sort_values(ascending = False)
    highestSalesCity = sorted_series.iloc[:1].to_dict()
    cities = [city for city, df in allMonthsData.groupby('City')]
    print(highestSalesCity)
    print(cities)
    plt.bar(cities, results)
    plt.xticks(cities,rotation="vertical", size=8)
    plt.xlabel("City")
    plt.ylabel("Total Sales ($)")
    plt.show()

def findBestTime():
    allMonthData = readAllMonthData()
    #create Hour and Minute column and get hour and minute from Order Date
    allMonthData['Order Date'] = pd.to_datetime(allMonthData['Order Date'])
    allMonthData['Hour'] = allMonthData['Order Date'].dt.time
    allMonthData['Hour'] = allMonthData['Hour'].apply(lambda x: str(x).split(":")[0])
    print(allMonthData.head())

    #Create Total Sales column
    allMonthData['Total Sales'] =  allMonthData['Quantity Ordered'] * allMonthData['Price Each']


    #Find hour where most purchases were made and return that hour
    totalSalesHour = allMonthData['Total Sales'].groupby(allMonthData['Hour'])
    sortedSeriesHour = totalSalesHour.sum().sort_values(ascending = False)
    bestHour = sortedSeriesHour.iloc[:1].to_dict()
    hours = range(0, 25)
    plt.plot(hours, totalSalesHour.sum())
    plt.xlabel("Hour")
    plt.ylabel("Total Sales ($)")
    plt.show()
    print(bestHour)

def findProductSoldMost():
    allData = readAllMonthData()
    #group all products together by quantity ordered
    products = allData.groupby('Product')['Quantity Ordered']
    productsSum = products.sum()
    #find product with highest quantity
    sortedProducts = products.sum().sort_values(ascending = False)
    bestProduct = sortedProducts.iloc[:1].to_dict()
    print(bestProduct)

    productsList = [product for product, df in allData.groupby('Product')]
    print(productsList)
    plt.bar(productsList, productsSum)
    plt.xticks(productsList,rotation="vertical", size=8)
    plt.xlabel("Product")
    plt.ylabel("Quantity Sold")
    plt.show()

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    #concatenateTwoFiles()
    concatenateAllSalesData()
    readAllMonthData()
    findProductSoldMost()
    #findBestTime()
    #findBestSalesCity()
    #findBestSalesMonth()
    #showTotalSalesVisual()