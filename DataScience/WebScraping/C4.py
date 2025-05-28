import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def get_total_pages(base_url):
    response = requests.get(base_url)
    response.encoding = "utf-8"
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pager = soup.find("ul", class_="pager")
        if pager:
            last_page = pager.find("li", class_="current").text.strip().split()[-1]
            return int(last_page)
    return 1

def scrape_books(base_url):
    total_pages = get_total_pages(base_url)
    all_books = []

    for page in range(1, total_pages + 1):
        url = f"{base_url}/catalogue/page-{page}.html"
        response = requests.get(url)
        response.encoding = "utf-8"
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a.attrs["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p.attrs["class"][1]

            # Link para a página do livro
            book_url = urljoin(url, book.h3.a["href"])
            # Acessa a página do livro para pegar a categoria
            book_resp = requests.get(book_url)
            book_resp.encoding = "utf-8"
            book_soup = BeautifulSoup(book_resp.text, "html.parser")

            # A categoria está no caminho de navegação (breadcrumb)
            category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

            all_books.append([title, price, rating, category])

    return all_books

# Executar o scraper
base_url = "https://books.toscrape.com"
books_data = scrape_books(base_url)

# Criar o DataFrame
df = pd.DataFrame(books_data, columns=["Título", "Preço", "Classificação", "Categoria"])

# Salvar em CSV
df.to_csv("books_detalhado.csv", index=False, encoding="utf-8")
print("Todos os dados foram extraídos e salvos com sucesso!")