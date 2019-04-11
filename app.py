from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(executable_path=r'./driver/geckodriver')

count = 0

lst = []
while (count != 200):

	driver.get('https://www.autotrader.ca/cars/?rcp=100&rcs={}'.format(count)) # update rcs by 100 each time
	cars = driver.find_elements(By.CLASS_NAME, "result-item-inner")

	for car in cars:
	    info = {}
	    info["Car"] = car.find_elements(By.CLASS_NAME, "result-title")[0].text
	    # info["year"] = str(car.find_elements(By.CLASS_NAME, "result-title")[0].text)[:4]
	    if (car.find_elements(By.CLASS_NAME, "kms") != []):
		if (str(car.find_elements(By.CLASS_NAME, "kms")[0].text) != ""):
		    info["Mileage"] = str(car.find_elements(By.CLASS_NAME, "kms")[0].text)[len("Mileage "):-3]
	    if (car.find_elements(By.CLASS_NAME, "price-amount") != []):
		if (str(car.find_elements(By.CLASS_NAME, "price-amount")[0].text) != ""):
		    info["price"] = str(car.find_elements(By.CLASS_NAME, "price-amount")[0].text)
	    lst.append(info)

	count += 100

print(len(lst))


    



# from bs4 import BeautifulSoup
# import requests, pandas, os


# print ("Welcome to smartRealtor!")
# # budget = str(input("Please provide max price."+os.linesep))
# # maxBedRooms = str(input("Please specify the minimum number of Bedrooms."+os.linesep))
# # minBathRooms = str(input("Please specify the minimum number of Bathrooms."+os.linesep))
# # city = str(input("Please provide a city."+os.linesep))

# driver = webdriver.Firefox(executable_path=r'./driver/geckodriver')
# driver.get('https://www.autotrader.ca')
# content = req.content
# print(content)

# soup = BeautifulSoup(content, "html.parser")
# listings = soup.find_all("div", {"class": ["result-item-inner"]}) #all the listings

# print(len(listings))

# print ("Gathering Data! Please wait.")
# if soup.find("ol", {"class": "pagination"}):
# 	if soup.find("ol", {"class": "pagination"}).findChildren() != None:
# 	    pages = soup.find("ol", {"class": "pagination"}).findChildren()

# 	for i in range(2, int(pages[-3].text) + 1):
# 	    req = requests.get("https://www.century21.ca/search/PropType-RES/0-700000/Beds-3/Baths-2/Q-brampton/page" + str(i))    
# 	    content = req.content
# 	    soup = BeautifulSoup(content, "html.parser")
# 	    listings += soup.find_all("span", {"class": ["mls-id", "property-id"]})

# print ("Please check the src folder for 'Possibilities.csv'.")
# new_lst = pandas.DataFrame(lst)
# new_lst.to_csv("Possibles.csv")
