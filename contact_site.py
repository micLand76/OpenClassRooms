# encoding=utf8

"""Script to scrapp the test website books.toscrape.com
first: find all the books categories
after: get all the book's url of all pages of a categorie
end: get the infos of a book and write them into a csv file
	(the csv file is for each categorie)
	and download picture of the book, for each book
"""

import os
import urllib.request

import requests
from bs4 import BeautifulSoup


def recup_books_url(categorie_url):
	"""Recup the url of the books

	for each categorie we get the url of the differents books
	all the url are added to product_page_url_list

	Parameters
	----------
	categorie_url: tag
		give the url of the categorie to parse the page(s) of the categorie

	Returns
	-------
	list
		list of the url of the products of the category
	"""

	response_cat = requests.get(SITE_URL + categorie_url.a['href'])
	source_cat = BeautifulSoup(response_cat.content, 'html.parser')
	prod_list = source_cat.find_all('h3')

	first_page = SITE_URL + categorie_url.a['href'].replace('index.html','')


	while next_page_exist(source_cat) is True:
		response_cat = requests.get(first_page + \
						str(source_cat.find("li",{"class": 'next'}).a['href']))
		source_cat = BeautifulSoup(response_cat.content, 'html.parser')
		prod_list += source_cat.find_all('h3')

	return prod_list


def next_page_exist(soup_cat):
	"""verify if there's a next page

	to know if there's more than one page of books for the categorie
	if the string 'next' appears in the page, that means there's another
	page so we continue to add the books of the next page until there's no 'next'

	Parameters
	----------
	soup_cat: document parsed
		give the categorie's page parsed to find a tag with 'next'

	Returns
	-------
	boolean
		if there's the 'next' class into the document, returns True
	"""

	if soup_cat.find("li",{"class": 'next'}) is not None:
		return True


def recup_book_info(contenu):
	"""Recup a book's infos

	for a book we recup all the infos asked
	some of them are into a table in the page
	some else are into tags (like title)
	the infos are writen into the csv file of the categorie
	the picture of the book if downloaded into a repository
	of the categorie

	Parameters
	----------
	contenu: tag
		the content of the book's page

	Returns
	-------

	"""

	soup = BeautifulSoup(contenu, 'html.parser')

	#name of the book without modifications
	title = soup.find("div",{"class": 'col-sm-6 product_main'}).\
				find('h1').text.strip().replace('%','')
	#name of the book with modification to give a name to the file jpg
	image_name = title.replace("'","").replace("\\","").replace(",","")\
			.replace("-","_").replace(".","").replace("!","")\
			.replace(":","").replace("?","").replace(")","")\
			.replace("(","").replace("*","").replace("#","")\
			.replace(" ","_").replace("&","").replace("/","_")\
			.replace("\"","_")

	image_url_tag = soup.find("div",{"class": 'item active'}).find('img')
	image_url = image_url_tag['src'].replace('../..','http://books.toscrape.com')

	#the informations about the book are in a table
	upc_liste = soup.find("table",{"class": 'table-striped'}).find_all('td')

	product_description = soup.find_all('p')[3].text.replace('...more','').replace('%','')

	book = []
	for upc in upc_liste:
		book.append(upc.text.strip().replace('%',''))

	#to extract the nb of stock available and not the entire sentence
	nb_available = book[5][book[5].find('(')+1:].replace(' available)','')
	if nb_available.isdigit is False:
		nb_available = 0

	#we create a new repository for each categorie
	try:
		os.makedirs(CATEGORY_NAME, exist_ok=True)
	except:
		print("There's a problem")

	#we use % to make the diff between columns because there's
	#often commas into the product description
	csv_file.write(product_url + '%' + book[0] + '%' + title + '%' + book[3] +\
					'%' + book[2] + '%' + nb_available + '%' +\
					CATEGORY_NAME + '%' + book[6] +\
					'%' + image_url + '%' + CATEGORY_NAME + '\\' + image_name + ".jpg" +\
					'%' + product_description + '\n')

	#after we had create the csv file, we download each book's image
	urllib.request.urlretrieve(image_url, CATEGORY_NAME + "/" + image_name + ".jpg")


SITE_URL = 'http://books.toscrape.com/'

#we begin by getting the url of all the categories of books
response_books= requests.get(SITE_URL + 'index.html')
source_page = BeautifulSoup(response_books.content, 'html.parser')
categorie = source_page.find("ul",{"class": 'nav nav-list'}).find_all('li')


for cat_url in categorie:
	#the first categorie is ignored because it's the whole catalogue
	if cat_url.a['href'] == "catalogue/category/books_1/index.html":
		continue

	#we create a file for each categorie
	#we open the csv file with option to don't have any problem of
	#caracters conversion we make this here to not erase the csv file
	#of the categorie when it make another loop to find the name of the
	#categorie, we need to use the get_text fct and to erase the spaces
	CATEGORY_NAME = str(cat_url.get_text()).strip()
	print('SCRAPPING OF THE CATEGORIE ' + CATEGORY_NAME,flush=True)
	with open('./'+CATEGORY_NAME+'.csv', 'w', encoding='utf-8-sig') as csv_file:

		#we create the title of the columns
		#we use % to make the diff between columns because there's
		#often commas into the product description
		csv_file.write("product_page_url" + '%' + "universal_ product_code (upc)"\
						+ '%' + "title" + '%'	+ "price_including_tax" + '%'\
						+ "price_excluding_tax" + '%' + "number_available" + '%'\
						+ "category" + '%'\
						+ "review_rating" + '%' + "image_url" + '%'\
						+ "image_file_name" + '%' + "product_description" + '\n')

		#we recupere all the books' url into product_page_url_list
		product_page_url_list = recup_books_url(cat_url)

		product_page_url = []

		#for each categorie, we loop on the books of it
		for product_url in product_page_url_list:
			product_url = 'http://books.toscrape.com/catalogue' +\
							product_url.a['href'].replace('../../..','')
			response = requests.get(product_url)

			if response.status_code == 200 :
				recup_book_info(response.content)
