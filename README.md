# scrape-elcomercio

_Este programa hace scraping de https://elcomercio.com ; una versión online de un famoso diario de Ecuador._
_This program scrapes through https://elcomercio.com ; a web version of a famous ecuadorian newspaper._

## Starting 🚀

El scraping es una técnica ampliamente utilizada que extrae información de un sitio web automáticamente.
Scraping is a widely used technique that extracts information from a website automatically.

### Prerrequisitos / Requirements 🖥

-   Python 3.5+ 👉 https://www.python.org/downloads/
-   Package Installer pip 👉 https://pypi.org/project/pip/

### Cómo usarlo / How to use it 📜

-El programa se ejecuta en la consola. Después de la ejecución, solicita la cantidad de páginas requeridas, el tipo de archivo deseado y si el usuario desea las últimas noticias o las noticias de moda.
-Si el usuario elige .txt, el programa creará múltiples archivos .txt con todas las noticias. Si el usuario elige .csv, el programa creará un archivo csv con las noticias y detalles en cada fila.
-Si se elige las noticias en tendencia, el programa preguntará de entre varios temas actuales, de cuál se desean las noticias.

-The program runs on console. After run, it asks for number of pages required, type of file wanted, and whether the user wants the latest news or the trending news.
-If the user chooses .txt, the program will create multiple .txt files with all the news. If the user chooses .csv, the program will create a csv file with the news and details in each row.
-If trending news is chosen, it will ask which topic is wanted.

### Cómo se creo / How it was created 🛠

Programado en python. Utiliza las librerías "lxml" y "requests" para obtener los datos de la página https://elcomercio.com.

Programmed in python. It uses the "lxml" and "requests" libraries to obtain the data from the https://elcomercio.com website.

[requests] = https://requests.readthedocs.io/en/latest/ --- Obtiene contenido de una URL con una petición GET // Obtains content with a GET request
[lxml] = https://lxml.de/ --- Procesa XML y HTML // Processes XML and HTML

-_-_-\_
Creado por Rothman Alan 😸
