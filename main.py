from Crawler import Crawler
import json
from termcolor import colored
from bs4 import BeautifulSoup
from selenium import webdriver
import uuid
import pyfiglet


# Gets data from plpUrls.json with start and end page.
# It can be Category or certain brand or any other plp pages.
def PLP():
    driver = webdriver.Chrome("chromedriver.exe")
    f = open("plpUrls.json", 'r')
    urlObjects = json.loads(f.read())
    for url in urlObjects["Urls"]:
        plpUrl = url["Url"]
        startPage = url["StartPage"]
        endPage = url["EndPage"]
        productdigikalaUrl = 1
        plpSplitedUrls = plpUrl.split("/")
        plpSplitedUrls = [u for u in plpSplitedUrls if u != ""]
        plpCategoryNameToNameJsonFile = plpSplitedUrls[-1]
        for page in range(startPage, endPage):
            digikalaUrl = f'{plpUrl}?page={page}'
            resultJson = {
                "Products": []
            }
            driver.get(digikalaUrl)
            plpPageSource = driver.page_source
            plpSoup = BeautifulSoup(plpPageSource, 'html.parser')
            productsLinks = plpSoup.find_all(
                'a', {"class": "d-block pointer pos-relative bg-000 overflow-hidden grow-1 py-3 px-4 px-2-lg h-full-lg VerticalProductCard_VerticalProductCard--hover___3eXg"})
            productLinkList = []
            for link in productsLinks:
                productLinkList.append(
                    f'https://www.digikala.com{link["href"]}')
            productLinkList = [
                x for x in productLinkList if "click" not in x]
            for productLink in productLinkList:
                driver.get(productLink)
                productSoup = BeautifulSoup(driver.page_source, 'html.parser')
                resultJson["Products"].append(
                    Crawler(index=productdigikalaUrl, soup=productSoup, productUrl=productLink))
                if(productdigikalaUrl % 10 == 0):
                    print(
                        colored(f"{productdigikalaUrl} pages Where Extracted ...", 'red'))
                print(
                    colored(f"page {productLink} was succesfully extracted!", 'green'))
                productdigikalaUrl += 1
            with open(f'Data/{plpCategoryNameToNameJsonFile}{page}.json', 'w', encoding="utf-8") as f:
                json.dump(resultJson, f, ensure_ascii=False)
        driver.close()


# Gets data from urls in Urls.txt and it should contain pdp urls.
def PDP():
    f = open("urls.txt", "r")
    urllist = [line.rstrip() for line in f]
    resultJson = {
        "Products": []
    }
    driver = webdriver.Chrome("chromedriver.exe")
    for url in urllist:
        driver.get(url)
        productSoup = BeautifulSoup(driver.page_source, 'html.parser')
        resultJson["Products"].append(Crawler(url, productSoup, url))

    with open(f'Data/{uuid.uuid1()}.json', 'w', encoding="utf-8") as f:
        json.dump(resultJson, f, ensure_ascii=False)
        driver.close()


# UnComment wich you want to run and comment the other one.
PLP()
# PDP()

# Done!
print(pyfiglet.figlet_format("ALL DONE!", font="banner3-D"))
