from flask import Flask, render_template, url_for, redirect, request , g
from flask_wtf import CSRFProtect
from Amazon import *
import csv
import sqlite3

########## CONFIG ###########
app = Flask(__name__)

app.config.from_pyfile('config.py')
csrf = CSRFProtect(app)
@app.before_request
def before_request():
    g.db = sqlite3.connect('producttracker.db')

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def rastreia_produto(search_term):  # Receber outra url dps
    url = create_amazon_url(search_term)
    page = browser_setup()
    products_list = amazonWebScrapper(url, page)  # WebScraping Amazon
    page.close()

    conn = sqlite3.connect('producttracker.db')
    c = conn.cursor()

    for produto in products_list:
        ultima_verificacao = c.execute('''SELECT * FROM produtos_recentes WHERE name = ?''', (produto.nome,)).fetchone()
        historico = c.execute('''SELECT * FROM produtos_rastreados WHERE name = ?''', (produto.nome,)).fetchall()

        if ultima_verificacao is not None and ultima_verificacao != 0:
            # Kontrol ekleniyor
            if produto.preco is not None and ultima_verificacao[1] is not None:
                produto.last_price_change = ((produto.preco - ultima_verificacao[1]) / ultima_verificacao[1]) * 100
            else:
              produto.last_price_change = None  # Veya başka bir değer
        if historico is not None:
            produto.registrado = True
            for registro in historico:
              if produto.preco is not None and registro[1] is not None:
                 produto.last_price_change = ((produto.preco - registro[1]) / registro[1]) * 100
                 produto.price_history.append((registro[1]))
                 produto.price_history_dates.append(registro[-1])

    conn.close()

    registra_produto_recente(products_list)

    return products_list


def tracked_terms():
    lista_de_termos = []
    with open('/Users/edausta/Desktop/PYTHON.PY/AmazonPriceTracker-main/MainProject/tracked_terms.csv', 'r', newline='') as termos:
        csv_reader = csv.reader(termos)
        for termo in csv_reader:
            lista_de_termos.append(termo[0])
        termos.close()

    return lista_de_termos


@app.route('/')
def index():
    termos_rastreados = tracked_terms()
    return render_template('index.html', lista_de_termos=termos_rastreados)


@app.route('/register_search_term', methods=['GET', ])
def register_search_term():
    tracked_term = request.args.get('tracked-term')
    already_tracked_terms = tracked_terms()
    if tracked_term not in already_tracked_terms:
        with open('/Users/edausta/Desktop/PYTHON.PY/AmazonPriceTracker-main/MainProject/tracked_terms.csv', 'a', newline='') as termos:
            csv_writer = csv.writer(termos)
            csv_writer.writerow([tracked_term])
            termos.close()
        produtos = rastreia_produto(tracked_term)
        registra_produto_rastreado(produtos)

    return redirect(url_for('index'))


@app.route('/remove_search_term', methods=['GET', ])
def remove_search_term():
    lista_de_termos = tracked_terms()
    item_id = int(request.args.get('id'))  # Obtém o ID do item a partir do formulário

    # Lógica para remover o item da lista (lista_de_termos) aqui
    if 1 <= item_id <= len(lista_de_termos):
        termo_removido = lista_de_termos.pop(item_id - 1)
        with open('/Users/edausta/Desktop/PYTHON.PY/AmazonPriceTracker-main/MainProject/tracked_terms.csv', 'w', newline='') as termos:
            csv_writer = csv.writer(termos)
            for termo in lista_de_termos:
                csv_writer.writerow([termo])
            termos.close()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/produtos-rastreados', methods=['GET', ])
def produtos_rastreados():
    termos_rastreados = tracked_terms()
    search_term = request.args.get('search_term')
    if search_term.strip() == '':
        return redirect(url_for('index'))
    else:
        products_list = rastreia_produto(search_term)
        return render_template('rastreamento.html', products_list=products_list, lista_de_termos=termos_rastreados)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
