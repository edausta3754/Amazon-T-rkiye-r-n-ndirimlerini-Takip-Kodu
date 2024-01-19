import sqlite3
from Produto import Produto
from datetime import datetime

if __name__ == '__main__':
    conn = sqlite3.connect('producttracker.db')
    c = conn.cursor()
    
   # produtos_recentes tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS produtos_recentes(name TEXT PRIMARY KEY, price FLOAT, rating TEXT)''')

    # produtos_rastreados tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS produtos_rastreados(name TEXT, price FLOAT, rating TEXT, data DATE)''')

    # Veritabanı işlemlerini commit et ve bağlantıyı kapat
    conn.commit()
    conn.close()
