# OpenClassRooms
Projects for my OpenClassRooms formation

## About / Synopsis

* This is a project to learn to scrap informations on items on a website
* Project status: test for my studies

## Installation

* Download Files:
download the files contact_site.py and requirements.tx there : https://github.com/micLand76/OpenClassRooms.git
* From the command line (like Git Bash): 
python -m venv env
pip install -r requirements.txt
source env/scripts/activate
python contact_site.py

## Usage

With the script contact_site.py you will create as many csv file as there's categories in the website https://books.toscrape.com/index.html.
It will create as many repositories as there's categories to download the book's pictures into.

### Features

The script is written in Python 3.7.3
I used the internal librairies os and urllib.request.
Os is used to create a new repository for each categorie of books.
Urllib.request is used to download the picture of each book.
I had imported the librairies BeautifulSoup and Requests
BeautifulSoup is used to parse the pages of the website.
Requests is used to recover the website pages.

### Content

First, the script request to the website and parse it.
We search the tag to find the name of each categorie, except the first categorie wich is 'Books': the entire catalogue.
We call the recup_book_url fonction, for each categorie, to parse the page(s) of it and recover the url of each book.
The recup_book_url fonction call the next_page_exist fonction to know if there's many pages for the categorie to parse it.
For each book's url, we use recup_book_info fonction to recover all the informations we need on a book and write them in the categorie's csv file and to download the book's picture.
During the processing, the script print on the screen the name of the categorie it's working on.

