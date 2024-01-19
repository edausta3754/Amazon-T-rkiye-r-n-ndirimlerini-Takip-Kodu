from bs4 import BeautifulSoup
from Produto import Produto
from browser import *
import sqlite3


def registra_produto_recente(products_list):
    conn = sqlite3.connect('producttracker.db')
    cursor = conn.cursor()
    produtos_recentes = cursor.execute('''SELECT name FROM produtos_recentes''').fetchall()

    for produto in products_list:
        ultima_verificacao = cursor.execute('''SELECT * FROM produtos_recentes WHERE name = ?''', (produto.nome,)).fetchone()
        
        if (produto.nome,) in produtos_recentes:
            cursor.execute('''UPDATE produtos_recentes SET price = ?, rating = ? WHERE name = ?''',
                           (produto.preco, produto.rating, produto.nome))
        else:
            cursor.execute('''INSERT INTO produtos_recentes VALUES (?,?,?)''',
                           (produto.nome, produto.preco, produto.rating))
    conn.commit()
    conn.close()


def amazonWebScrapper(link, page):
    page.goto(link)
    page.wait_for_load_state('load')
    page_soup = BeautifulSoup(page.content(), 'html.parser')

    main_results = page_soup.find('div', attrs='s-main-slot')
    if main_results is None:
        print("Hata: 'main_results' bulunamadı.")
        return []
    products_list = main_results.find_all('div', attrs='sg-col-4-of-24')
    items_list = []
    for product in products_list:
        if product.find('a', class_='puis-label-popover puis-sponsored-label-text') is None:  # Evitando Patrocinios
            nome = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            preco = product.find('span', class_='a-offscreen')
            rating = product.find('i', class_='a-icon')
            img_src = product.find('img', class_='s-image')  # ['src']
            prod_link = product.find('a',
                                     class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')

            item = Produto(
                len(items_list),  # Id
                nome.text if nome is not None else None,  # Nome
                preco.text[3:].replace('.', '').replace(',', '.') if preco is not None else None,  # Preco
                rating.text if rating is not None else None,  # Rating
                img_src['src'] if img_src is not None else None,  # Img Source
                'https://www.amazon.com.tr//' + prod_link['href'] if prod_link is not None else None  # Product Link
            )
            items_list.append(item)
    next_page = goto_nextpage(page_soup)
    if next_page:
        # print("\nNext Page\n")
        amazonWebScrapper(next_page, page)
        return items_list
    else:
        # print("Thats all Folks")
        return items_list


def registra_produto_rastreado(lista_de_produtos):
    conn = sqlite3.connect('producttracker.db')
    cursor = conn.cursor()

    for produto in lista_de_produtos:
        print(f"Inserindo {produto.nome}, {produto.preco}, {produto.rating}")
        cursor.execute('''INSERT INTO produtos_rastreados VALUES (?,?,?,?)''',
                       (produto.nome, produto.preco, produto.rating, produto.date))
    conn.commit()
    conn.close()
