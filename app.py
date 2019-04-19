import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(executable_path=r'./driver/geckodriver')
driver.get("https://wwwa.autotrader.ca/cars/on/brampton/?rcp=100&rcs=0&srt=3&pRng=%2C5000&oRng=%2C150000&prx=250&prv=Ontario&loc=L6V%202S1&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch")

urls = []
last_page = int(str(driver.find_elements(By.CLASS_NAME, "last-page, page-item")[0].get_attribute("data-page"))) * 100
for count in range(0, last_page, 100):
    urls.append('https://wwwa.autotrader.ca/cars/on/brampton/?rcp=100&rcs={}&srt=3&pRng=%2C5000&oRng=%2C150000&prx=250&prv=Ontario&loc=L6V%202S1&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch'.format(count))


lst = []
def parse(url):
	info = {}
	driver.get(url) # update rcs by 100 each time
	cars = driver.find_elements(By.CLASS_NAME, "result-item-inner")

	for car in cars:

        try:
            title = (car.find_elements(By.CLASS_NAME, "result-title")[0].text).encode('ascii', 'ignore').decode('ascii')
        except Exception as e:
            title = "N/A"
            print("DEBUG \n{}\n title error: {}".format(e, url))

        try:
            price = str(car.find_elements(By.CLASS_NAME, "price-amount")[0].text)[1:].replace(",", "")
        except Exception as e:
            price = "N/A"
            print("DEBUG \n{}\n price error: {}".format(e, url))

        try:
            mileage = str(car.find_elements(By.CLASS_NAME, "kms")[0].text)[len("Mileage "):-3]
        except Exception as e:
            mileage = "N/A"
            print("DEBUG \n{}\n mileage error: {}".format(e, url))
	    
	    info = {}
	    info["Title"] = title
		info["Mileage"] = mileage
		info["Price"] = price
	    
	    lst.append(info)

if __name__ == '__main__':
	
	for url in urls:
		parse(url)

	print ("Please check the src folder for 'Possibilities.csv'.")
	new_lst = pandas.DataFrame(lst)
	new_lst.to_csv("Possibles.csv")
