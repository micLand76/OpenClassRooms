# encoding=utf8

import requests
import csv
from bs4 import BeautifulSoup


"""we open the csv file with option to don't have any problem of caracters conversion
we make this here to not erase the csv file when it make another loop"""
with open('./zitate.csv', 'w', encoding = 'utf-8-sig') as csv_file:

	url = 'http://books.toscrape.com/'

	"""we begin by getting the url of all the categories of books"""
	response_books= requests.get(url + 'index.html')
	source_page = BeautifulSoup(response_books.content, 'html.parser')
	categorie = source_page.find("ul",{"class":'nav nav-list'}).find_all('li')
	

	for cat_url in categorie:
		"""the first categorie is ignored because it's the whole catalogue"""
		#print(cat_url.a['href'])
		if cat_url.a['href'] == "catalogue/category/books_1/index.html":
			continue
		
		"""for each categorie we get the url of the differents books"""
		response_cat = requests.get(url + cat_url.a['href'])
		source_cat = BeautifulSoup(response_cat.content, 'html.parser')
		product_page_url_list = source_cat.find_all('h3')

		page_suiv = source_cat.find("ul",{"class":'pager'})
		page_prem = url + cat_url.a['href'].replace('index.html','')
		
		def page_suiv_existe(soup_cat):
			
			if soup_cat.find("li",{"class":'next'}) != None:
				return True
		

		while page_suiv_existe(source_cat) is True:
			response_cat = requests.get(page_prem + str(source_cat.find("li",{"class":'next'}).a['href']))
			#print(page_prem + str(source_cat.find("ul",{"class":'pager'}).a['href']))
			source_cat = BeautifulSoup(response_cat.content, 'html.parser')
			product_page_url_list += source_cat.find_all('h3')
			

		product_page_url = []

		"""for each categorie, we loop on the books of it"""
		for product_url in product_page_url_list:
			#print(product_url.a['href'].replace('../../..',''))
			product_url = 'http://books.toscrape.com/catalogue' + product_url.a['href'].replace('../../..','')
			response = requests.get(product_url)

			if response.status_code == 200 :
				"""we get the informations of the book"""
				soup = BeautifulSoup(response.content, 'html.parser')
				livre = []
				titre = soup.find("div",{"class":'col-sm-6 product_main'}).find('h1').text.strip()
				livre.append(titre)
				image_url = soup.find("div",{"class":'item active'}).find('img')
				livre.append(image_url['src'].replace('../..','http://books.toscrape.com'))
				"""the informations about the book are in a table"""
				upc_liste = soup.find("table",{"class":'table-striped'}).find_all('td')

				for upc in upc_liste:
					livre.append(upc.text.strip())

				csv_file.write(product_url + ',' + livre[0] + ',' + livre[1] + ',' + livre[2] + ',' + livre[3] + ',' + livre[4] + ',' + livre[5] + ',' + livre[6] + ',' + livre[7] + '\n')
				

