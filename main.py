import requests
from bs4 import BeautifulSoup
import json
import html
from pathlib import Path
from selenium import webdriver
from selenium_stealth import stealth
import nodriver
import asyncio
import time
import random
import ikea_api

# Per Retailer
ScrapeAmount = "99999"

http_proxies = [
    'http://109.236.83.153:8888', 
    'http://64.227.46.7:8080', 
    'http://45.92.177.60:8080'
]

def SaveSofa(Retailer, RetailerURL, Name, Currency, Price, Attributes, Variant, Images, URL):
    JsonFile = Path("SofaDatav2.json")
    # Create an Empty JSON file
    if not JsonFile.is_file():
        f = open(str(Path(__file__).parent.resolve()) + "/SofaDatav2.json", "a")
        f.write("{\n}")
        f.close()
    
    JsonppData = open(str(Path(__file__).parent.resolve()) + "/SofaDatav2.json", "r")
    JsonData = json.loads(JsonppData.read())
    JsonppData.close()

    if not "Retailers" in JsonData:
        JsonData["Retailers"] = {}
    
    if not Retailer in JsonData["Retailers"]:
        JsonData["Retailers"][Retailer] = {}
        JsonData["Retailers"][Retailer]["RetailerURL"] = RetailerURL
    
    if not "Items" in JsonData["Retailers"][Retailer]:
        JsonData["Retailers"][Retailer]["Items"] = {}
    
    JsonData["Retailers"][Retailer]["Items"][Name] = {}
    JsonData["Retailers"][Retailer]["Items"][Name]["Currency"] = Currency
    JsonData["Retailers"][Retailer]["Items"][Name]["Price"] = Price
    JsonData["Retailers"][Retailer]["Items"][Name]["Attributes"] = Attributes
    JsonData["Retailers"][Retailer]["Items"][Name]["Variant"] = Variant
    JsonData["Retailers"][Retailer]["Items"][Name]["URL"] = URL
    JsonData["Retailers"][Retailer]["Items"][Name]["ImageUrls"] = Images
    
    with open(str(Path(__file__).parent.resolve()) + "/SofaDatav2.json", 'w') as f:
        json.dump(JsonData, f)

def ScrapeAmart():
    Retailer = "Amart Furniture"
    RetailerUrl = "https://www.amartfurniture.com.au/"
    URL = "https://www.amartfurniture.com.au/on/demandware.store/Sites-au-amart-Site/en_AU/Search-UpdateGrid?cgid=sale-loungesandsofas&start=0&sz=" + ScrapeAmount
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    # Find the main Sofa Element which contains the Sofas info
    SofaElements = soup.find_all("div", class_="col-6 col-lg-4")

    # Loop through All of the Found elements
    for i in range(len(SofaElements)):
        SofaElement = SofaElements[i]
        SofaTile = SofaElement.find("div", class_="product plp-product").find("div", class_="card product-tile-card")
        # Find the Sofa Info in json and unescape the values (it still doesn't give us the image and url)
        BootStrapInfo = html.unescape(SofaTile['data-bootstrap'])
        # Json Data Parsed into jsonData
        jsonData = json.loads(BootStrapInfo)

        SofaName = jsonData["gtmSaveData"]["data"]["name"]
        SofaCurrency = jsonData["gtmSaveData"]["data"]["currency"]
        SofaPrice = jsonData["gtmSaveData"]["data"]["price"]
        SofaAttributes = jsonData["gtmSaveData"]["data"]["attributes"]
        SofaVariant = jsonData["gtmSaveData"]["data"]["variant"]

        SofaImageCard = SofaTile.find("div", class_="figure card-img product-overlay-wrapper").find("a", class_="plp-image-link")
        SofaLink = RetailerUrl + SofaImageCard["href"]
        SofaPage = requests.get(SofaLink)
        SofaSoup = BeautifulSoup(SofaPage.content, "html.parser")
        SofaImages = SofaSoup.select("div.product-image-primary")
        SofaImageUrls = []
        for i in range(len(SofaImages)):
            SofaImageUrls.append(SofaImages[i].select("img")[0]["src"])

        SaveSofa(Retailer, RetailerUrl, SofaName, SofaCurrency, SofaPrice, SofaAttributes, SofaVariant, SofaImageUrls, SofaLink)

def test_proxy(proxy):
    """Test if the proxy is working by making a simple request."""
    try:
        # Test the proxy by sending a simple request to httpbin.org/ip
        response = requests.get('http://httpbin.org/ip', proxies={"http": proxy, "https": proxy}, timeout=5)
        # Check if status is OK
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def filter_working_proxies(proxy_list):
    """Test all proxies and filter only the ones that are functional."""
    working_proxies = []
    for proxy in proxy_list:
        if test_proxy(proxy):
            working_proxies.append(proxy)
    
    if not working_proxies:
        print("No working proxies were found.")
    else:
        print(f"Working proxies: {working_proxies}")
    return working_proxies

# First, test all proxies and filter the working ones
#valid_proxies = filter_working_proxies(http_proxies)

ala = True
cookies = None

async def getas(URL, ss): 
    """Scrape Webpage Data Undetected and return webpage content."""
    browser = None
    browser = await nodriver.start(browser_args=[
            "--disable-gpu",
            "--disable-hardware-acceleration",
            "--disable-extensions",
            "--enable-logging",
            "--v=1",
            "--user-data-dir=C:/Users/ronit/Desktop/SofaScraper/User Data/Profile",
        ])

    page = await browser.get(URL)
    if ala == True:
        ala == False
        if ss:
            await page.select("div.ProductCardPriceDevice_sf-price-device__ZcZaZ", 20)
        await asyncio.sleep(10)
    else:
        if ss:
            await page.select("div.ProductCardPriceDevice_sf-price-device__ZcZaZ", 20)
        await asyncio.sleep(10)
    
    content = await page.get_content()
    await page.close()
    return content

def ScrapeHarveyNorman():
    Retailer = "Harvey Norman"
    RetailerUrl = "https://www.harveynorman.com.au/"
    for i in range(int(ScrapeAmount)):
        URL = "https://www.harveynorman.com.au/furniture-outdoor-bbqs/living-room/lounges/sofas/1065?srsltid=AfmBOoqnrywO4WR7xOPX-AHX-XDRp0F59zCbvKqqV9LZ97gu3rUqCMpL&p=" + str(i+1)

        pgcont = nodriver.loop().run_until_complete(getas(URL, True))

        # close the driver

        soup = BeautifulSoup(pgcont, "html.parser")

        print(soup)

        # Find the main Sofa Element which contains the Sofas info
        if soup.find("div", class_="sf-product-card-container__grid sf-product-card-container__grid--2col") == None:
            break
        
        SofaElements = soup.find("div", class_="sf-product-card-container__grid sf-product-card-container__grid--2col").find_all("div", class_="ProductCard_sf-product-card__HIi_S")
        
        for i in range(len(SofaElements)):
            SofaElement = SofaElements[i]
            SofaBody = SofaElement.find("div", class_="ProductCard_sf-product-card__body__W_z7r")

            SofaName = SofaBody.find("div", class_="ProductCardName_sf-product-card__name__fYJRz").find("a").get_text()
            SofaCurrency = "AUD" # Assuming it is from .au
            SofaPrice = None
            if SofaBody.find("div", class_="ProductCardPriceDevice_sf-price-device__ZcZaZ") == None:
                SofaPrice = "Contact Harvey Norman for Price."
            elif SofaBody.find("div", class_="ProductCardPriceDevice_sf-price-device__ZcZaZ").find("div", class_="ProductCardPrice_sf-product-card-price__IGnOp") == None:
                SofaPrice = "Contact Harvey Norman for Price."
            elif SofaBody.find("div", class_="ProductCardPriceDevice_sf-price-device__ZcZaZ").find("div", class_="ProductCardPrice_sf-product-card-price__IGnOp").find("span", class_="ProductCardPrice_sf-product-card-price__amount__JcmtP") == None:
                SofaPrice = "Contact Harvey Norman for Price."
            else:
                SofaPrice = SofaBody.find("div", class_="ProductCardPriceDevice_sf-price-device__ZcZaZ").find("div", class_="ProductCardPrice_sf-product-card-price__IGnOp").find("span", class_="ProductCardPrice_sf-product-card-price__amount__JcmtP").get_text()
            
            SofaAttributes = ""
            try:
                SofaAttributes = "" + SofaElement.find("span", {'data-testid': "offer-flag"}).get_text() + ", In Stock" # Assuming it is in stock
            except AttributeError:
                SofaAttributes = "In Stock"
            SofaUrl = RetailerUrl + SofaBody.find("div", class_="ProductCardName_sf-product-card__name__fYJRz").find("a")["href"]
            
            page = nodriver.loop().run_until_complete(getas(SofaUrl, False))
            SofaSoup = BeautifulSoup(page, "html.parser")

            ImageLi = None
            if SofaSoup.find("ul", class_="Slider_glide__slides__JAy0g") == None:
                ImageLi = []
            else:
                ImageLi = SofaSoup.find("ul", class_="Slider_glide__slides__JAy0g").find_all("li", class_="Slider_glide__slide__INv_h")
            SofaImages = []
            SofaVariants = []
            for i in range(len(ImageLi)):
                SofaImages.append(ImageLi[i].find("img")["src"])
            
            VarLi = []
            if len(SofaSoup.select("div.ConfigurableOptions_select-container__Ep_HE")) > 0:
                VarLi = SofaSoup.select("div.ConfigurableOptions_select-container__Ep_HE")[0].find("select").find_all("option")
            print("s")
            print(VarLi)
            for i in range(len(VarLi)):
                if VarLi[i].get_text() != "":
                    print(VarLi[i].get_text())
                    SofaVariants.append(VarLi[i].get_text())
            
            if len(SofaVariants) > 1:
                for i in range(len(SofaVariants)):
                    SaveSofa(Retailer, RetailerUrl, SofaName, SofaCurrency, SofaPrice, SofaAttributes, SofaVariants[i], SofaImages, SofaUrl)
            else:
                SaveSofa(Retailer, RetailerUrl, SofaName, SofaCurrency, SofaPrice, SofaAttributes, "No Variants Yet", SofaImages, SofaUrl)

def ScrapeTFP():
    Retailer = "The Furniture People"
    RetailerURL = "https://thefurniturepeople.com.au/"
    URL = "https://thefurniturepeople.com.au/lounges/configuration/sofa-bed/mfp/c-configuration-0,111?limit=" + ScrapeAmount

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    
    SofaElements = soup.select("div.product-layout.product-grid.no-desc.col-xl-4.col-lg-4.col-md-4.col-sm-6.col-12")
    
    for i in range(len(SofaElements)):
        SofaElement = SofaElements[i]
        SofaTitle = SofaElement.select("a.text-ellipsis-2")[0].get_text()
        SofaUrl = SofaElement.select("a.text-ellipsis-2")[0]["href"]
        SofaCurrency = "AUD"
        SofaPrice = None
        if SofaElement.select("span.price-new.special") == None:
            SofaPrice = SofaElement.select("span.price-old")[0].get_text()
        else:
            SofaPrice = SofaElement.select("span.price-new.special")[0].get_text()
        
        SofaAttributes = ""
        if len(SofaElement.select("div.product-label.bottom_right div.square")) != 0:
            if SofaElement.select("div.product-label.bottom_right div.square")[0].get_text() == "In Stock":
                SofaAttributes += "In Stock"
            elif SofaElement.select("div.product-label.bottom_right div.square")[0].get_text() == "Best Sellers":
                SofaAttributes += "Best Sellers, In Stock"
        
        SofaPage = nodriver.loop().run_until_complete(getas(SofaUrl, False))

        SofaSoup = BeautifulSoup(SofaPage, "html.parser")
        SofaImages = []
        SofaVariants = []
        SofaImagesBody = SofaSoup.select("div.owl-stage")[0].select("div.owl-item")

        for i in range(len(SofaImagesBody)):
            if len(SofaImagesBody[i].select("a")) != 0:
                SofaImages.append(SofaImagesBody[i].select("a")[0]["href"])
        
        SofaVariantsBody = SofaSoup.select("div.form-group.col-lg-6.col-xl-12.required")
        for i in range(len(SofaVariantsBody)):
            if SofaVariantsBody[i].find("label").get_text() == "Colour":
                col = SofaVariantsBody[i].select("label.custom-control-label")
                for i in range(len(col)):
                    SofaVariants.append(' '.join(col[i].get_text().split()))
        
        if len(SofaVariants) > 1:
            for i in range(len(SofaVariants)):
                SaveSofa(Retailer, RetailerURL, SofaTitle, SofaCurrency, SofaPrice, SofaAttributes, SofaVariants[i], SofaImages, SofaUrl)
        elif len(SofaVariants) == 1:
            SaveSofa(Retailer, RetailerURL, SofaTitle, SofaCurrency, SofaPrice, SofaAttributes, SofaVariants[0], SofaImages, SofaUrl)
        else:
            SaveSofa(Retailer, RetailerURL, SofaTitle, SofaCurrency, SofaPrice, SofaAttributes, "No Variants", SofaImages, SofaUrl)

def ScrapeIKEA():
    Retailer = "IKEA"
    RetailerUrl = "https://www.ikea.com/"
    for i in range(int(ScrapeAmount)):
        URL = "https://www.ikea.com/au/en/cat/sofas-fu003/?page=" + str(i)

        page = nodriver.loop().run_until_complete(getas(URL, False))

        soup = BeautifulSoup(page, "html.parser")

        with open("output.html", "w") as file:
            file.write(str(page))

        SofaElements = soup.select("div.plp-product-list__products div.plp-fragment-wrapper")

        if SofaElements == None:
            break

        for SofaElement in SofaElements:
            SofaName = SofaElement.select("h3.plp-price-module__name.notranslate span.plp-price-module__name-decorator span.notranslate.plp-price-module__product-name")[0].get_text()
            SofaCurrency = "AUD"
            SofaPrice = "Contact IKEA for Price"
            if len(SofaElement.select("span.plp-price.plp-price--leading.plp-price--leading.plp-price--medium.plp-price--currency-super-aligned.plp-price--decimal-super-aligned.plp-price-module__current-price.notranslate span.plp-price__integer")) != 0:
                SofaPrice = "$" + SofaElement.select("span.plp-price.plp-price--leading.plp-price--leading.plp-price--medium.plp-price--currency-super-aligned.plp-price--decimal-super-aligned.plp-price-module__current-price.notranslate span.plp-price__integer")[0].get_text()
            SofaAttributes = ""
            if len(SofaElement.select("p.plp-product-badge.plp-product-badge--top-seller")) != 0:
                if SofaElement.select("p.plp-product-badge.plp-product-badge--top-seller")[0].get_text() == "Best seller":
                    SofaAttributes = "Best Seller"
            
            #print(SofaElement.select("div.plp-commercial-message.plp-commercial-message--subtle.plp-commercial-message--subtle--nlp span"))
            for x in range(len(SofaElement.select("div.plp-commercial-message.plp-commercial-message--subtle.plp-commercial-message--subtle--nlp span"))):
                if "lower" in SofaElement.select("div.plp-commercial-message.plp-commercial-message--subtle.plp-commercial-message--subtle--nlp span")[x].get_text():
                    if SofaAttributes == "":
                        SofaAttributes += "Sale"
                    else:
                        SofaAttributes += ", Sale"
                elif "New" in SofaElement.select("span.plp-commercial-message__title")[x].get_text():
                    if SofaAttributes == "":
                        SofaAttributes += "New"
                    else:
                        SofaAttributes += ", New"

            for x in range(len(SofaElement.select("span.plp-status.plp-status--labelled.plp-status--leading span.plp-status__label"))):
                if "stock" in SofaElement.select("span.plp-status.plp-status--labelled.plp-status--leading span.plp-status__label")[x].get_text():
                    if SofaAttributes == "":
                        SofaAttributes += "In Stock"
                    else:
                        SofaAttributes += ", In Stock"
                elif "Running" in SofaElement.select("span.plp-status.plp-status--labelled.plp-status--leading span.plp-status__label")[x].get_text():
                    if SofaAttributes == "":
                        SofaAttributes += "Running Low"
                    else:
                        SofaAttributes += ", Running Low"
            
            SofaVariant = "Various Colours"
            SofaURL = SofaElement.select("div.plp-mastercard__item.plp-mastercard__price")[0].find("a")["href"]
            SofaImages = SofaElement.select("div.plp-mastercard__item.plp-mastercard__image")[0].select("img.plp-product__image")
            SofaImageUrls = []
            for Im in SofaImages:
                SofaImageUrls.append(Im["src"])
            
            SaveSofa(Retailer, RetailerUrl, SofaName, SofaCurrency, SofaPrice, SofaAttributes, SofaVariant, SofaImageUrls, SofaURL)

if __name__ == "__main__":
    ScrapeIKEA()
    #ScrapeTFP()
    #ScrapeHarveyNorman()
    #ScrapeAmart()
