import pandas
from bs4 import BeautifulSoup
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
driver.get("https://wwwa.autotrader.ca/cars/on/brampton/?rcp=100&rcs=0&srt=3&pRng=%2C5000&oRng=%2C150000&prx=250&prv=Ontario&loc=L6V%202S1&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch")

# get all the urls that you want to scrape and add them in an array.
urls = []


last_page = int(str(driver.find_elements(By.CLASS_NAME, "last-page, page-item")[0].get_attribute("data-page"))) * 100
for count in range(0, last_page, 100):
    urls.append('https://wwwa.autotrader.ca/cars/on/brampton/?rcp=100&rcs={}&srt=3&pRng=%2C5000&oRng=%2C150000&prx=250&prv=Ontario&loc=L6V%202S1&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch'.format(count))


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

    soup = BeautifulSoup(html, "html.parser")
    cars = soup.find_all("div", {"class": "result-item-inner"})

    for car in cars:
        info = {}
        inner_ = BeautifulSoup(str(car), "html.parser")

        try:
            title = (inner_.find("h2").text).encode('ascii', 'ignore').decode('ascii')
        except Exception as e:
            title = "N/A"
            print("DEBUG \n{}\n title error: {}".format(e, url))

        try:
            price = str(inner_.find("span", {"class": "price-amount"}).text)[1:].replace(",", "")
        except Exception as e:
            price = "N/A"
            print("DEBUG \n{}\n price error: {}".format(e, url))

        try:
            mileage = str(inner_.find("div", {"class": "kms"}).text).split(" ")[1].replace(",", "")
        except Exception as e:
            mileage = "N/A"
            print("DEBUG \n{}\n mileage error: {}".format(e, url))

        try:
            link_ = str(inner_.find("a", {"class": ["result-title", "click"]}, href=True)['href'])
        except Exception as e:
            link_ = "N/A"
            print("DEBUG \n{}\n link_ error: {}".format(e, url))


        info["Car"] = title
	
        # if (info["Car"] != None):
        #     info["year"] = title[:4]

        info["Mileage"] = mileage
        
        info["price"] = price

        if (link_ != "N/A"):
            info["link"] = "https://wwwa.autotrader.ca" + link_
        else:
            info["link"] = link_

        lst.append(info)


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

    # print(urls)
    # print(len(urls))
    print(len(lst))
    driver.quit()

print ("Please check the src folder for 'Possibilities.csv'.")
new_lst = pandas.DataFrame(lst)
new_lst.to_csv("Possibles.csv")
