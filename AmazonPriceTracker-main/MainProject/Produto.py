from datetime import datetime

class Produto:
    def __init__(self, identificador, nome, preco, rating, img_src, product_link, last_price=None):
        self.id = identificador
        self.nome = nome
        self.preco = self.convert_to_float(preco)
        self.rating = rating
        self.img_src = img_src
        self.product_link = product_link
        self.date = datetime.today().strftime('%d/%m/%Y')
        self.last_price_change = last_price
        self.price_history = []
        self.price_history_dates = []
        self.registrado = False
        self.old_price = None
    

    def convert_to_float(self, preco):
        if preco is not None:
            # 'TL' ifadesini temizle
            preco = preco.replace('TL', '')
            
            # Nokta ve virgül karakterlerini temizle, noktaya çevir
            preco = preco.replace(',', '').strip()
            
            # Eğer '.' karakteri varsa, sadece bir tane bırak
            if preco.count('.') > 1:
                preco = preco.rsplit('.', 1)[0] + '.' + preco.rsplit('.', 1)[1]
            
            return float(preco)
        return None

    def __str__(self):
        eski_fiyat_info = f"Eski Fiyat: {self.last_price_change}" if self.last_price_change is not None else ""
        
        return   f"Produto: {self.nome},\n" \
               f"Preço: {self.preco}\n" \
               f"Avaliacao: {self.rating}\n" \
               f"Link: {self.product_link}\n" \
               f"Dia do registro: {self.date}\n " \
               f"Eski Fiyat: {self.old_price} {self.preco}\n"
