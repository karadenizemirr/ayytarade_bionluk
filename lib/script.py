import requests
from multiprocessing import Lock
from rich.console import Console
from bs4 import BeautifulSoup
from lib import custom_request
from urllib.parse import urlparse

class Scraper:
    def __init__(self,url:str, counter:int) -> None:
        self.session = requests.Session()
        self.url = url
        self.counter = counter
        self.console = Console()
        self.data = []
        self.lock = Lock()
        # Test Connection
        test_response = self.session.get(self.url).status_code

        if test_response == 200:
            self.console.print(f"\n[bold green]Connection to [bold blue]{self.url}[/bold blue] established[/bold green]\n")
        else:
            self.console.print(f"\n[red]Connection to {self.url} failed[/red]\n")

    def __product_links(self, category_url:str):
        try:
            res = self.session.get(category_url)
            soup = BeautifulSoup(res.text, "html.parser")

            product_li = soup.find_all('li', {'class': 'product'})
            links = [link.find('a', {'data-event-type': 'product-click'})['href'] for link in product_li]

            self.console.print(f"[bold green]Found [bold blue]{len(links)}[/bold blue] products[/bold green]\n")
            return links
        except Exception as e:
            print(e)
    
    def __product_detail(self, product_link:str):
        try:
            html_res = custom_request.GET(product_link)

            # CategoryName
            parsed_url = urlparse(self.url)
            category = parsed_url.path.split('/')[1]
            

            soup = BeautifulSoup(html_res, "html.parser")
            product_name = soup.select('body > div.body > div.container > div.productView-scope > div.productView.productView--full > div.productView-detailsWrapper > div > section:nth-child(1) > div > h1')[0].text
            product_upc = soup.select('body > div.body > div.container > div.productView-scope > div.productView.productView--full > div.productView-detailsWrapper > div > section:nth-child(1) > div > dl > dd.productView-info-value.productView-info-value--upc')[0].text
            product_price = soup.select('body > div.body > div.container > div.productView-scope > div.productView.productView--full > div.productView-detailsWrapper > div > section:nth-child(3) > div.productView-options.productView-options--1col > div > div:nth-child(2) > span.price.price--withoutTax.price--main')[0].text
            product_stock = soup.select('body > div.body > div.container > div.productView-scope > div.productView.productView--full > div.productView-detailsWrapper > div > section:nth-child(3) > div.productView-options.productView-options--1col > form.form.form--addToCart > div.form-field.form-field--stock > label > span')[0].text
            product_image = soup.find('li', {'class': 'productView-imageCarousel-main-item'}).find('img')['src']

            detail = {
                "product_name": product_name,
                "product_category": category,
                "product_upc": product_upc,
                "product_price": product_price,
                "product_stock": product_stock,
                "product_image": product_image,
                "product_link": product_link
            }
            
            self.console.print(f"[bold green]Product [bold blue]{product_name}[/bold blue] scraped[/bold green]\n")
            return detail
        except Exception as e:
            print(e)
            return None

    def run(self):
        for _ in range(self.counter):
            links = self.__product_links(f"{self.url}?page={_ + 1}")

            for link in links:
                product_detail = self.__product_detail(link)
                self.data.append(product_detail)
        
        return self.data

