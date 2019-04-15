from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(executable_path=r'./driver/geckodriver')

count = 0

lst = []
while (count != 500):

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

# print ("Please check the src folder for 'Possibilities.csv'.")
# new_lst = pandas.DataFrame(lst)
# new_lst.to_csv("Possibles.csv")
