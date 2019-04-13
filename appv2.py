from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(executable_path=r'./driver/geckodriver')
driver.get("http://www.google.com/")

urls = []
for count in range(0, 500, 100):
    print(count)
    urls.append('https://www.autotrader.ca/cars/?rcp=100&rcs={}'.format(count))


lst = []
def parse(url, count):

    driver.execute_script("window.open('{}',);".format(url))

    driver.switch_to.window(driver.window_handles[count])

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'wrapper')))

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
    # print(len(lst))
    driver.quit()

# print ("Please check the src folder for 'Possibilities.csv'.")
# new_lst = pandas.DataFrame(lst)
# new_lst.to_csv("Possibles.csv")
