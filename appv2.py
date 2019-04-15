import pandas
from selenium import webdriver
from threading import Thread, Lock
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


lock = Lock()
# precondition: firefox needs to be installed and a path to its binary should be specified.

# get the binary for firsfox browser.
driver = webdriver.Firefox(executable_path=r'./driver/geckodriver')
# open any page
driver.get("http://www.google.com/")

# get all the urls that you want to scrape and add them in an array.
urls = []
for count in range(0, 500, 100):
    urls.append('https://www.autotrader.ca/cars/?rcp=100&rcs={}&pRng=5000%2C8000&oRng=%2C150000&prx=-1&loc=L6V2S1&trans=Manual&hprc=True&wcp=True'.format(count))



lst = []
def parse(url, count):
    """
    Open a new tab for a url, switch over to the newly created tab; wait for the page to load
    then scrape the info you need.
    """
    driver.execute_script("window.open('{}',);".format(url))

    # print("current_url: {}, url: {}, => {}, {}".format(driver.current_url, url, driver.window_handles[count], count))
    lock.acquire()
    driver.switch_to.window(driver.window_handles[count])

    html = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'SearchListings')))
    
    # print(html.get_attribute("outerHTML"))

    # print("\n\n current_url: {}, \n url: {} \n\n".format(driver.current_url, url))
    html = driver.find_element_by_id("SearchListings").get_attribute("outerHTML")
    # cars = driver.find_elements(By.CLASS_NAME, "result-item-inner")
    # print("{} {}".format(len(cars), count))
    lock.release()

    # for car in cars:
    #     info = {}
    #     info["Car"] = car.find_elements(By.CLASS_NAME, "result-title")[0].text
	
    #     # if (info["Car"] != None):
    #         # info["year"] = str(car.find_elements(By.CLASS_NAME, "result-title")[0].text)[:4]
    #     if (car.find_elements(By.CLASS_NAME, "kms") != []):
    #         if (str(car.find_elements(By.CLASS_NAME, "kms")[0].text) != ""):
    #             info["Mileage"] = str(car.find_elements(By.CLASS_NAME, "kms")[0].text)[len("Mileage "):-3]
    #     if (car.find_elements(By.CLASS_NAME, "price-amount") != []):
    #         if (str(car.find_elements(By.CLASS_NAME, "price-amount")[0].text) != ""):
    #             info["price"] = str(car.find_elements(By.CLASS_NAME, "price-amount")[0].text)

    #     info["link"] = str(car.find_elements(By.CLASS_NAME, "result-title, click")[0].get_attribute("href"))

    #     lst.append(info)
    # driver.quit()

# create a thread for each url you want to scrape.
threadlist = []
if __name__ == '__main__':
    count = 0
    for url in urls:
        count += 1
        thread_ = Thread(target=parse, args=(url, count,))
        thread_.start()
        threadlist.append(thread_)

    for thread_ in threadlist:
        thread_.join()

    # print(len(urls))
    print(len(lst))
    driver.quit()

# print ("Please check the src folder for 'Possibilities.csv'.")
# new_lst = pandas.DataFrame(lst)
# new_lst.to_csv("Possibles.csv")
