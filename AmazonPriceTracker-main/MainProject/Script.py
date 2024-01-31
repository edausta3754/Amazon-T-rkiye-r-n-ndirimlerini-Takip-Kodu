from browser import *
from Amazon import amazonWebScrapper
import sqlite3
import csv

tracked_terms = []
with open('tracked_terms.csv', 'r', newline='') as termos:
    csv_reader = csv.reader(termos)
    page = browser_setup()
    conn = sqlite3.connect('producttracker.db')
    cursor = conn.cursor()

    for termo in csv_reader:
        url = create_amazon_url(termo)
        products_list = amazonWebScrapper(url, page)  # WebScraping Amazon
        for produto in products_list:
            print(f"Inserindo {produto.nome}, {produto.preco}, {produto.rating}")
            cursor.execute('''INSERT INTO produtos_rastreados VALUES (?,?,?,?)''',
                           (produto.nome, produto.preco, produto.rating, produto.date))

    conn.commit()
    conn.close()
    page.close()
    termos.close()
