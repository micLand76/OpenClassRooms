# OpenClassRooms
Projects for my OpenClassRooms formation

## About / Synopsis

* This is a project to learn to scrap informations on items on a website
* Project status: test for my studies

## Installation

* First, download Python on your PC: https://www.python.org/downloads/ and choose the installation for your OS
* Download Files:<br>
download the files contact_site.py and requirements.tx there : https://github.com/micLand76/OpenClassRooms.git
* From the command line (like Git Bash): <br>
  ```
  python -m venv env
  source env/scripts/activate
  pip install -r requirements.txt
  python contact_site.py
  ```

## Usage

With the script contact_site.py you will create as many csv file as there's categories in the website https://books.toscrape.com/index.html.<br>
It will create as many repositories as there's categories to download the book's pictures into.

### Features

The script is written in Python 3.7.3<br>
I used the internal librairies os and urllib.request.<br>
Os is used to create a new repository for each categorie of books.<br>
Urllib.request is used to download the picture of each book.<br>
I had imported the librairies BeautifulSoup and Requests<br>
BeautifulSoup is used to parse the pages of the website.<br>
Requests is used to recover the website pages.

### Content

First, the script request to the website and parse it.<br>
We search the tag to find the name of each categorie, except the first categorie wich is 'Books': the entire catalogue.<br>
We call the recup_book_url fonction, for each categorie, to parse the page(s) of it and recover the url of each book.<br>
The recup_book_url fonction call the next_page_exist fonction to know if there's many pages for the categorie to parse it.<br>
For each book's url, we use recup_book_info fonction to recover all the informations we need on a book and write them in the categorie's csv file and to download the book's picture.<br>
The differents informations on a book are separated by the '%' character (because the comma is used into the differents labels and descriptions) so to see the informations on Excel, it's necessary to convert the datas and separate them by the '%' character.<br>
During the processing, the script print on the screen the name of the categorie it's working on.

