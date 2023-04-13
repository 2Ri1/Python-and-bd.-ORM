import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

if __name__ == '__main__':
	
	DSN = "postgresql://postgres:parol@localhost:5432/hw"
	engine = sqlalchemy.create_engine(DSN)
	create_tables(engine)
	
	Session = sessionmaker(bind=engine)
	session = Session()
		
	with open('fixtures/tests_data.json', 'r') as fd:
		data = json.load(fd)
		
	for record in data:
		model = {
			        'publisher': Publisher,
			            'shop': Shop,
				        'book': Book,
				        'stock': Stock,
				        'sale': Sale,    
		}[record.get('model')]
		session.add(model(id=record.get('pk'), **record.get('fields')))
	session.commit()
	session.close()

	your_request = int(input('Введите 1, если хотите задать поиск по имени автора\n Введите 0, еслт хотите задать поиск по идентификатору издателя:'))
	
	if your_request == 1:
		your_request_1 = Publisher.name == input('Введите имя автора:')
		q = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).\
			        join(Publisher).join(Stock).join(Sale).join(Shop).\
								filter(your_request_1).order_by(Sale.date_sale)
		print(q)
		for book, shop, price, count, date in q:
			print("\t"f'{book:<40} | {shop:<10} | {price*count:<8} | {date}')
	
	else:
		your_request_2 = Publisher.id == input('Введите id автора:')
		q = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).\
			        join(Publisher).join(Stock).join(Sale).join(Shop).\
								filter(your_request_2).order_by(Sale.date_sale)
		print(q)
		for book, shop, price, count, date in q:
			print("\t"f'{book:<40} | {shop:<10} | {price*count:<8} | {date}')
			
	session.commit()