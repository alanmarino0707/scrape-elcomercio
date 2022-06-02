import requests
import lxml.html as html
import os
import datetime
import csv

# XPATH ROUTES AND URL OF THE NEWSPAPER TO SCRAPE

HOME_URL = "https://www.elcomercio.com/"

XPATH_ARTICLE_LINK = '//h3[@class="list-item__title"]/a/@href'
XPATH_ARTICLE_TIME = '//time/text()'
XPATH_ARTICLE_AUTHOR = '//div[@class="entry__author"]/text()'
XPATH_ARTICLE_TITLE = '//h1[@class="entry__title"]/text()'
XPATH_ARTICLE_BODY = '//div[contains(@class, "entry__content")]/p/descendant-or-self::node()/text()'
XPATH_CATEGORIES = '//ul[@class="site-topics__topics"]//a/text()'

CSV_HEADER = ["Título de la publicación","Hora de publicación","Autor","Cuerpo de la publicación","Link del artículo"]

# .csv ->1
# .txt ->2
# .json ->3

# Function that gets the data of the articles the parse_home passes to it.
def parse_news(link, timedate, choices, ctr):
    try:
        # Getting link from the parse_home function
        article = requests.get(link)
        if article.status_code == 200:
            news = article.content.decode("utf-8")
            parsed = html.fromstring(news)
            try:
                # Getting all the data from the article via its XPATH
                title = parsed.xpath(XPATH_ARTICLE_TITLE)[0]
                title = title.replace('"', "")
                title = title.replace("¿", "")
                title = title.replace("?", "")
                published = parsed.xpath(XPATH_ARTICLE_TIME)[0][0]
                author = parsed.xpath(XPATH_ARTICLE_AUTHOR)
                author = str(author).replace('\n',"")
                body = parsed.xpath(XPATH_ARTICLE_BODY)
                joined_body = "".join(body)
            except IndexError:
                return
            # choices[1] saves the user's file type. 
            if choices[1]== "1":
                # establishing creation of the csv file on its first iteration. Also, adding the header and wrting the rows of the first article
                with open(f"{timedate[0]}/{timedate[1]}.csv","w", newline="", encoding = "utf-8") as f:
                    writer = csv.writer(f)
                    if ctr == 0:
                        writer.writerow(CSV_HEADER)
                    rows =[title,published,author,joined_body,link]
                    writer.writerow(rows)
            elif choices[1] == "2":
                # establishing creation of the txt files and writing all the data in them
                with open(f"{timedate[0]}/{title}.txt","w", newline="", encoding = "utf-8") as f:
                    f.write(title)
                    f.write('\n\n')
                    f.write("Publicado a las: " + published + "Fecha: " + timedate[0])
                    f.write('\n\n')
                    f.write("Autor: " + author)
                    f.write('\n\n')
                    f.write(joined_body)
                    f.write('\n\n')
                    f.write("Link al artículo" + link)

            elif choices[1] == "3":
                # establishing creation of the json file on its first iteration.
                # Also, creating dictionaries which contain the data and saving them into a list
                if ctr == 0:
                    list_d_data = []
                    with open(f"{timedate[0]}/{timedate[1]}.json","w", newline="", encoding = "utf-8") as f:
                        dict_data = {"Título":title, "Hora de publicación":published, "Autor de la publicación":author,"Cuerpo de la publicación":joined_body,"Link del artículo":link}
                        list_d_data += dict_data
                    f.close()
                elif ctr in range(11,17):
                    f = open(f"{timedate[0]}/{timedate[1]}.json","w", newline="", encoding = "utf-8")
                    dict_data = {"Título":title, "Hora de publicación":published, "Autor de la publicación":author,"Cuerpo de la publicación":joined_body,"Link del artículo":link}
                    list_d_data += dict_data
                    dict_json = str(list_d_data)
                    dict_json = dict_json.replace('[','{')
                    dict_json = dict_json.replace(']','}')
                    json_file = open(f"{timedate[0]}/{timedate[1]}.json","w")
                    json_file.write(dict_json)
                    json_file.close()
                    f.close()
                else:
                    f = open(f"{timedate[0]}/{timedate[1]}.json","w", newline="", encoding = "utf-8")
                    dict_data = {"Título":title, "Hora de publicación":published, "Autor de la publicación":author,"Cuerpo de la publicación":joined_body,"Link del artículo":link}
                    list_d_data += dict_data
                    f.close()
            else:
                return
        else:
            raise ValueError(f'Error: {article.status_code!r}')
    except ValueError as ve:
        print(ve)

# Defining the function that will obtain the article links for each page
def parse_home(choices,categories):
    pages = choices[0]
    try:
        # Accessing the main URL as long as the status code == 200
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            try:
                if pages >0 and pages<=6:
                    # creating a directory / folder whose name is today's date
                    today = datetime.date.today().strftime("%d-%m-%Y")
                    curr_time = datetime.datetime.now().strftime("%H-%M-%S")
                    timedate = [today,curr_time]
                    if not os.path.isdir(today):
                        os.mkdir(today)
                    # Calling the function that will get the data of the articles in each page, as many times as pages the user chose.
                    for itr in range(pages):
                        # If the length of choices is 2, it is because the user chose to scrape the latest news
                        # Accessing the link for the latest news
                        if len(choices) == 2:
                            response_pages = requests.get(f"{HOME_URL}ultima-hora/page/{itr+1}")
                        # If the length of choices is 3, it is because the user chose to scrape the trending news
                        # Accessing the link for the trending news
                        elif len(choices) == 3:
                            response_pages = requests.get(f"{HOME_URL}tag/{categories[int(choices[2])-1]}/page/{itr+1}")
                        if response_pages.status_code == 200:
                        # getting main URL, and transformig its HTML structure in order to get categories through its XPATH
                            home_g = response_pages.content.decode("utf-8")
                            parsed_g = html.fromstring(home_g)
                            news_links =parsed_g.xpath(XPATH_ARTICLE_LINK)
                            # This function gets data for every article. This will happen 10 times for each page.
                            ctr = itr
                            for link in news_links:
                                parse_news(link,timedate,choices,ctr)
                                ctr+=1
                else:
                    raise TypeError(f"Error: Fuera de rango, o valor incorrecto.")
            except TypeError as ve:
                print(ve)
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
                print("Presiona " + str(count+1) + " para leer noticias sobre: " + category)
            t_choice = int(input("Escoge una opción: "))
            control = True
            while control:
                # Directing parse_home_trends(choices) into parse_home(choices)
                # Regardless of the type of news the user chooses, parse_home will always be run
                if t_choice in range(1,len(categories)+1):
                    t_choice = str(t_choice)
                    choices += t_choice
                    parse_home(choices,categories)
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
    print("Hola. Obtendré las noticias más importantes y las guardaré para ti en un archivo .csv, en uno .json, en uno ,txt o en varios archivos .txt \n")
    # Inserting how many pages and what file type the user wants.
    pages = int(input(f"¿Cuántas páginas de las noticias deseas obtener? Cada página tiene 10 noticias. Escribe un número del 1 al 6: \n"))
    file_type = str(input("¿Qué tipo de archivo quieres? \n\n 1 para .csv \n\n 2 para .txt \n\n 3 para .json \n"))
    # Saving what the user chose into the list choices
    choices = []
    choices.append(pages)
    choices.append(file_type)
    categories = []
    control = True
    # Asking the user whether they want trending news or the last news.
    # This directs them to  parse_home(choices) or to parse_home_trends(choices)
    while control:
        u_choice = str(input("Para escoger las noticias del último momento presiona 1. \n\n Si deseas noticias de los temas en tendencia, presiona 2. \n"))
        if u_choice == "1":
            parse_home(choices, categories)
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