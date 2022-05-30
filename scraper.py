import requests
import lxml.html as html
import os
import datetime
import csv

# XPATH ROUTES AND URL OF THE NEWSPAPER TO SCRAPE

HOME_URL = "https://www.elcomercio.com/"

XPATH_ARTICLE_LINK = '//h3[@class="list-item__title"]/a/@href'
XPATH_ARTICLE_TIME = '//div[@class="entry__date text-nowrap text-muted"]/time/text()'
XPATH_ARTICLE_AUTHOR = '//div[@class="entry__author"]/text()'
XPATH_ARTICLE_TITLE = '//h1[@class="entry__title"]/text()'
XPATH_ARTICLE_BODY = '//div[@class="entry__content tbl-forkorts-article"]/p/descendant-or-self::node()/text()'
XPATH_CATEGORIES = '//ul[@class="site-topics__topics"]//a/text()'

# .csv ->1
# .txt ->2
# .json ->3


# Function that gets the data of the articles the parse_home passes to it.
def parse_news(link,today):
    try:
        article = requests.get(link)
        if article.status_code == 200:
            news = article.content.decode("utf-8")
            parsed = html.fromstring(news)

            try:
                title = parsed.xpath(XPATH_ARTICLE_TITLE)[0]
                title = title.replace('"', "")
                title = title.replace("¿", "")
                title = title.replace("?", "")
                published = parsed.xpath(XPATH_ARTICLE_TIME)[0]
                author = parsed.xpath(XPATH_ARTICLE_AUTHOR)
                body = parsed.xpath(XPATH_ARTICLE_BODY)
            except IndexError:
                return



    except ValueError as ve:
        print(ve)

# Defining the function that will obtain the article links for each page
def parse_home(choices):
    pages = choices[0]
    try:
        # Accessing the main URL as long as the status code == 200
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            if pages >0 and pages<=6:
                # creating a directory / folder whose name is today's date
                today = datetime.date.today().strftime("%d-%m-%Y")
                if not os.path.isdir(today):
                    os.mkdir(today)
                # Calling the function that will get the data of the articles in each page, as many times as pages the user chose.
                for i in range(pages):
                    # If the length of choices is 2, it is because the user chose to scrape the latest news
                    # Accessing the link for the latest news
                    if len(choices) == 2:
                        response_pages = f"{response!r}ultima-hora/page/{i+1}"
                    # If the length of choices is 3, it is because the user chose to scrape the trending news
                    # Accesing the link for the trending news
                    elif len(choices) == 3:
                        response_pages = f"{response!r}tag/{choices[3]}/page/{i+1}"
                    if response_pages.status_code == 200:
                    # getting main URL, and transformig its HTML structure in order to get categories through its XPATH
                        home = response_pages.content.decode("utf-8")
                        parsed = html.fromstring(home)
                        news_links =parsed.xpath(XPATH_ARTICLE_LINK)
                        # This function gets data for every article. This will happen 10 times for each page.
                        for link in news_links:
                            parse_news(link,today)
            else:
                pass
        else:
            raise ValueError(f"Error: {response.status_code}")
    except ValueError as ve:
        print(ve)

# Defining the function that gets the trending news
def parse_home_trends(choices):
    try:
        # getting main URL, and transformig its HTML structure in order to get categories through its XPATH
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode("utf-8")
            parsed = html.fromstring(home)
            categories = parsed.xpath(XPATH_CATEGORIES)
            # Printing out all categories and asking the user to choose one of them.
            # Then saving their choice into the list choices.
            for count, category in enumerate(categories):
                print("Presiona " + count + " para leer noticias sobre: " + category)
            t_choice = int(input("Escoge una opción: "))
            control = True
            while control:
                # Directing parse_home_trends(choices) into parse_home(choices)
                # Regardless of the type of news the user chooses, parse_home will always be run
                if t_choice in range(1,len(categories)):
                    choices += t_choice
                    parse_home(choices)
                control = False
                break
            else:
                exit = input("Has ingresado un valor incorrecto, ingresa cualquier valor y presiona Enter para volver a ingresar . \n\n O solo presiona Enter para salir del programa.")
                if exit == "":
                    control = False
                else:
                    control = True
    except ValueError as ve:
        print(ve)


# Defining main function. It will direct the user to either parse_home(choices) or to parse_home_trends(choices) 
# The function will direct to either sub-function depending on whether they choose to scrape the latest news or the most trending news.
# If the user chooses to get the trending news, they will be directed to parse_home_trends and then to parse_home
# choices is a list in which all choices made by the user will be saved at some point.
def scraper():
    print("Hola. Obtendré las noticias más importantes y las guardaré para ti en un archivo .csv, en uno .json, en uno ,txt o en varios archivos .txt")
    # Inserting how many pages and what file type the user wants.
    pages = [int(input(f"¿Cuántas páginas de las noticias deseas obtener? Cada página tiene 10 noticias. Escribe un número del 1 al 6"))]
    file_type = [str(input("¿Qué tipo de archivo quieres? \n\n 1 para .csv \n\n 2 para .txt \n\n 3 para .json"))]
    # Saving what the user chose into the list choices
    choices = pages + file_type
    control = True
    # Asking the user whether they want trending news or the last news.
    # This directs them to  parse_home(choices) or to parse_home_trends(choices)
    while control:
        u_choice = str(input("Para escoger las noticias del último momento presiona 1. \n\n Si deseas noticias de los temas en tendencia, presiona 2."))
        if u_choice == "1":
            parse_home(choices)
            break
        elif u_choice == "2":
            parse_home_trends(choices)
            break
        else:
            exit = input("Has ingresado un valor incorrecto, ingresa cualquier valor y presiona Enter para volver a empezar. \n\n O solo presiona Enter para salir del programa.")
            if exit == "":
                control = False
            else:
                control = True





def run():
    scraper()

if __name__ == "__main__":
    run()