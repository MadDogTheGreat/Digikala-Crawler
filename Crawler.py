from lxml import etree
from bs4 import BeautifulSoup

# You can config this method to get the data you want
# if digikala changed it's structure, you can change it here
# it returns a json object with pdp data
def Crawler(index: int, soup: BeautifulSoup, productUrl: str):

    myJson = {
        "Id": "",
        "Name": "",
        "ProductUrl": "",
        "MetaKeyWords": "",
        "MetaDescription": "",
        "Price": "",
        "OldPrice": "",
        "Gallery": [],
        "FullDescription": "",
        "ShortDescription": "",
        "Categories": [],
        "Manufacturer": {},
        "SpecificationAttributes": [],
        "ProductAttributes": [],
        "ProductTags": []
    }

    dom = etree.HTML(str(soup))

    myJson["Id"] = index

    myJson["ProductUrl"] = productUrl

    try:
        productName = soup.find('meta', {"name": "twitter:title"})["content"]
    except:
        productName = soup.find("h1", {"class": "text-h4 color-900 mb-2"})

    myJson["Name"] = productName

    try:
        price = soup.find(
            'span', {"class": "text-h4 ml-1 color-800"}).text.replace("تومان", "").replace("\n", "").replace(",", "").strip()
        myJson["Price"] = price
    except:
        pass

    images = soup.find_all(
        'img', {"alt": productName})
    imageList = []
    for image in images:
        try:
            imageList.append(image["src"])
        except:
            continue
    finalImageList = list(set(imageList))
    cnt = 1
    for images in finalImageList:
        myJson["Gallery"].append({
            "PictureSrc": images,
            "DisplayOrder": cnt
        })
        cnt += 1

    try:
        specificationAttribute = soup.find(
            'section', {"id": "specification"}).find_all('div', {"class": "w-full d-flex last PdpSpecification_PdpSpecification__valuesBox__smZXG"})

        resList = []
        for spec in specificationAttribute:
            specTitle = spec.find(
                'p', {"class": "ml-4 text-body-1 color-500 py-2 py-3-lg p-2-lg shrink-0 PdpSpecification_PdpSpecification__value__l6oUa"}).text.replace("\u200c", " ")
            specValueList = spec.find('div').find_all('p')
            finalSpecValues = []
            for spec in specValueList:
                finalSpecValues.append(spec.text)
                resList.append({
                    "Title": specTitle,
                    "Value": spec.text
                })

        myJson["SpecificationAttributes"].append({
            "ClassName": "مشخصات",
            "SpecificationList": resList
        })

    except:
        pass

    try:
        variantTitle = soup.find("div", {"class": "break-words py-3"}).find(
            "p", {"class": "grow-1 text-h5 color-900"}).text.split(':')[0]
        variants = soup.find_all("li", {
            "class": "pos-absolute z-1 w-100 overflow-hidden overflow-y-auto hide-scrollbar radius mt-1 bg-000 border-200 user-select-none DropDown_DropDown__list__VFq8Z"})
        for variant in variants:
            myJson["ProductAttributes"].append({
                "Title": variantTitle,
                "Value": variant.text,
            })
    except:
        pass

    try:
        variantTitle = soup.find("div", {"class": "break-words py-3"}).find(
            "p", {"class": "grow-1 text-h5 color-900"}).text.split(':')[0]
        variants = soup.find_all(
            'span', {"class": "d-none-lg mr-2 text-body-2 text-no-wrap"})
        for variant in variants:
            myJson["ProductAttributes"].append({
                "Title": variantTitle,
                "Value": variant.text,
            })
    except:
        pass

    categories = soup.find(
        'nav', {'class': 'py-2 px-5 px-0-lg grow-1 w-min-0'}).find_all('a')
    for category in categories[1:]:
        myJson["Categories"].append({
            "Name": category.text.replace("/", ""),
            "Url": category['href'],
            "MetaDescription": "",
            "MetaKeyWords": ""
        })

    try:
        shortDescription = soup.find(
            'div', {'id': 'shortReviewSection'}).text
        myJson["ShortDescription"] = shortDescription
    except:
        pass

    try:
        brand = soup.find("div", {
            "class": "d-flex flex-column flex-row-lg ProductContent_PdpProductContent__infoSection__vO1Gl"}).find("div", {"class": "grow-1 w-min-0"}).find("a")

        myJson["Manufacturer"] = {
            "Name": brand.text,
            "Url": brand['href'],
            "ImageUrl": "",
            "MetaDescription": "",
            "MetaKeyWords": ""
        }
    except:
        pass

    try:
        fullDescription = soup.find('article', {'id': 'PdpShortReview'})
        myJson["FullDescription"] = str(fullDescription)
    except:
        pass

    return myJson
