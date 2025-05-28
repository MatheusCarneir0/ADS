import os
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
    print(f"Total de páginas: {total_pages}")
    all_books = []

    for page in range(1, total_pages + 1):
        url = f"{base_url}/catalogue/page-{page}.html"
        print(f"Buscando página {page}: {url}")
        response = requests.get(url)
        response.encoding = "utf-8"
        if response.status_code != 200:
            print(f"Falha ao acessar a página {page}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a.attrs["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p.attrs["class"][1]

            # Link para a página do livro
            book_url = urljoin(url, book.h3.a["href"])
            book_resp = requests.get(book_url)
            book_resp.encoding = "utf-8"
            if book_resp.status_code != 200:
                category = "N/A"
            else:
                book_soup = BeautifulSoup(book_resp.text, "html.parser")
                breadcrumb = book_soup.find("ul", class_="breadcrumb")
                if breadcrumb:
                    category = breadcrumb.find_all("li")[2].text.strip()
                else:
                    category = "N/A"

            all_books.append([title, price, rating, category])

    return all_books

if __name__ == "__main__":
    base_url = "https://books.toscrape.com"
    books_data = scrape_books(base_url)

    df = pd.DataFrame(books_data, columns=["Título", "Preço", "Classificação", "Categoria"])
    print(f"Total de livros coletados: {len(df)}")

    # Caminho completo para salvar o CSV no diretório atual
    file_path = os.path.join(os.getcwd(), "books_detalhado.csv")
    df.to_csv(file_path, index=False, encoding="utf-8")

    print(f"Arquivo salvo em: {file_path}")
    print("Todos os dados foram extraídos e salvos com sucesso!")
