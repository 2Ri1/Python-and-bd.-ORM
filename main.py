import json

import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

if __name__ == '__main__':
	
	DSN = "postgresql://postgres:parol@localhost:5432/hw"
	engine = sqlalchemy.create_engine(DSN)
	create_tables(engine)
	
	Session = sessionmaker(bind=engine)
	session = Session()
	
	# publisher = Publisher()
	# shop = Shop()
	# book = Book()
	# stock = Stock()
	# sale = Sale()
	
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
		
	your_request = int(input('Введите 1, если хотите задать поиск по имени автора\n Введите 0, еслт хотите задать поиск по идентификатору издателя:'))
	
	if your_request == 1:
		your_request_1 = input('Введите имя автора:')
		q = session.query(publisher).join(book.course).filter(publisher.name == your_request_1)
		q = q.stock()
		q = q.shop()
		q = q.sale()
		print(q)
		for s in q.all():
			print("\t"f"{book.title} | {shop.name} | {sale.price} | {sale.date_sale}")
	else:
		your_request_2 = input('Введите id автора:')
		q = session.query(publisher).join(book.course).filter(publisher.id == your_request_2)
		q = q.stock()
		q = q.shop()
		q = q.sale()
		print(q)
		for s in q.all():
			print("\t"f"{book.title} | {shop.name} | {sale.price} | {sale.date_sale}")
			
	session.commit()