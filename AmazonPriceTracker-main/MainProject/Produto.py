from datetime import datetime


class Produto:
    def __init__(self, identificador, nome, preco, rating, img_src, product_link, last_price=None):
        self.id = identificador
        self.nome = nome
        self.preco = float(preco.replace(',', '.')) if preco is not None else None
        self.rating = rating
        self.img_src = img_src
        self.product_link = product_link
        self.date = datetime.today().strftime('%d/%m/%Y')
        self.last_price_change = last_price
        self.price_history = []
        self.price_history_dates = []
        self.registrado = False

    def __str__(self):
        return f"Produto: {self.nome},\n" \
               f"Preço: R${self.preco}\n" \
               f"Avalicao: {self.rating}\n" \
               f"Link: {self.product_link}\n" \
               f"Dia do registro: {self.date}"
