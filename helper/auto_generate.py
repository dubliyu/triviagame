import scraper as sc
import sqlite3

items = [
'clock',
'milk',
'lamp',
'spoon',
'credit card',
'bed',
'scotch tape',
'needle',
'sun glasses',
'shawl',
'truck',
'grid paper',
'glass',
'cookie jar',
'money',
'pants',
'air freshener',
'hair brush',
'book',
'box',
'coasters',
'tire swing',
'greeting card',
'bowl',
'sketch pad',
'teddies',
'carrots',
'headphones',
'canvas',
'shampoo',
'apple',
'spring',
'tv',
'puddle',
'thermometer',
'chair',
'twister',
'door',
'plate',
'balloon',
'helmet',
'pillow',
'car',
'bread',
'ice cube tray',
'sponge',
'lip gloss',
'leg warmers',
'paper',
'lotion',
'drill press',
'pen',
'toothbrush',
'shoe lace',
'phone',
'flag',
'clay pot',
'face wash',
'vase',
'fork',
'camera',
'cat',
'chocolate',
'twezzers',
'cup',
'shovel',
'socks',
'chalk',
'rug',
'sandal',
'conditioner',
'nail clippers',
'table',
'lamp shade',
'clamp',
'doll',
'house',
'soda can',
'keyboard',
'fridge',
'sticky note',
'seat belt',
'glow stick',
'cork',
'blanket',
'playing card',
'mirror',
'checkbook',
'ring',
'sailboat',
'rubber band',
'charger',
'soap',
'pencil',
'sidewalk',
'towel',
'packing peanuts',
'mouse pad',
'fake flowers',
'USB drive',
'candle',
'cell phone',
'plastic fork',
'rubber duck',
'chapter book',
'button',
'sand paper',
'floor',
'newspaper',
'desk',
'ipod',
'sofa',
'bookmark',
'soy sauce packet',
'bracelet',
'computer',
'stop sign',
'outlet',
'television',
'bottle',
'street lights',
'toe ring',
'candy wrapper',
'washing machine',
'keys',
'tissue box',
'bottle cap',
'beef',
'speakers',
'blouse',
'toilet',
'zipper',
'controller',
'flowers',
'hanger',
'key chain',
'pool stick',
'wagon',
'toothpaste',
'eye liner',
'window',
'sharpie',
'screw',
'shoes',
'tree',
'hair tie',
'paint brush',
'purse',
'mop',
'drawer',
'slipper',
'tooth picks',
'thread',
'model car',
'picture frame',
'tomato',
'knife'
]

LIMIT = len(items)
COUNT = 0
con = sqlite3.connect('app.db')
cur = con.cursor()
cur.execute("select max(qid) from questions;")
records = cur.fetchall()
max_qid = records[0][0]

def insert_into(a, b, c, d):
	sql = "insert into questions (qid, name, price, description, image) values (?, ?, ?, ?, ?)"
	global max_qid
	global con
	max_qid = max_qid + 1
	con.execute(sql, (max_qid, a, b, c, d,))
	con.commit()

def add_products(result):
	for product in result:
		url = product[2]
		soup = sc.open_url(url)
		title = sc.scrape_title(soup)
		price = sc.scrape_price(soup)
		desc = sc.scrape_desc(soup)
		if desc == "": desc = title
		img_urls = sc.scrape_Image_URLs(soup)
		if len(img_urls) == 0 : continue
		paths = sc.download_images(title, [img_urls[0]])
		print("Title: " + title + "\tPrice: " + str(price) + "\tImages: " + str(len(paths)))
		if len(paths) == 0 : continue
		insert_into(title, price, desc, str(paths[0]))

for item in items:
	COUNT = COUNT + 1
	if COUNT == LIMIT:
		COUNT = 0
		break
	res = sc.get_search_results(item)
	if res == None: continue
	add_products(list(res))



con.close()


#delete_Folder(_TEMP)
