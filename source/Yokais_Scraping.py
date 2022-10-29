from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from json import JSONEncoder
import urllib.request
        
class Yokai:
    Number=0
    Name=""
    Tribe=""
    Range=""
    FavoriteFood=""
    Biography=""
    def __init__(self, Number, Name, Tribe, Range, FavoriteFood, Biography):
        self.Number = Number
        self.Name = Name
        self.Tribe = Tribe
        self.Range = Range
        self.FavoriteFood = FavoriteFood
        self.Biography = Biography

    def serialize(self):  
        return {           
            'Number': self.Number, 
            'Name': self.Name,
            'Tribe': self.Tribe,
            'Range': self.Range,
            'FavoriteFood': self.FavoriteFood,
            'DetailUrl': self.DetailUrl
        }

class YokaiEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Yokai):
                 return obj.__dict__
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)
        
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def downloadImage(source,destination):
    urllib.request.urlretrieve(source, destination)
    
def get_yokai_biograpy(url):
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        yokaiTable= html.find("table", class_="infobox roundy")  
        td=yokaiTable.find("td",class_="roundy")
        return td.text.strip()
    return None

def get_yokais():
    """
    Downloads the page where the list of mathematicians is found
    and returns a list of strings, one per mathematician
    """
    url = 'http://es.yo-kaiwatch.wikia.com/wiki/Lista_de_Yo-kai_de_Yo-kai_Watch'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        yokaiTable= html.find("table", class_="wikitable")
        yokaiTrs=yokaiTable.find_all("tr")[1:]
        yokais=[]
        for yokaiTr in yokaiTrs:
            numberTd=yokaiTr.td;
            number=int(numberTd.text)

            nameTd=numberTd.nextSibling
            name=nameTd.a.text
            detailUrl=nameTd.a["href"]

            tribeTd=nameTd.nextSibling
            tribe=tribeTd.text.rstrip("\n\r")

            rangeTd=tribeTd.nextSibling
            range=rangeTd.text.replace(u'\xa0', u' ').rstrip("-\n\r").strip()

            favoriteFoodTd=rangeTd.nextSibling
            favoriteFood=favoriteFoodTd.text.rstrip("\n\r")
            if favoriteFood == "No tiene":
                favoriteFood=""

            yokai=Yokai(number,name,tribe,range,favoriteFood,get_yokai_biograpy(detailUrl))
            yokais.append(yokai)
        return list(yokais)

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))

def get_yokai_images():
    
    url = 'http://es.yo-kaiwatch.wikia.com/wiki/Lista_de_Yo-kai_de_Yo-kai_Watch'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        yokaiTable= html.find("table", class_="wikitable")
        yokaiTrs=yokaiTable.find_all("tr")[1:]
        
        for yokaiTr in yokaiTrs:
            numberTd=yokaiTr.td

            nameTd=numberTd.nextSibling
            name=nameTd.a.text
            detailUrl=nameTd.a["href"]
            get_yokai_image(detailUrl,name)



def get_yokai_image(detailUrl,name):
    response = simple_get(detailUrl)
    html = BeautifulSoup(response, 'html.parser')
    image=html.find("img",alt=name)
    if image is None:
       image= html.find_all("a",class_="image image-thumbnail")[1].img

    imageSrc="";
    if image.has_attr('data-src'):
        imageSrc=image["data-src"]
    else:
        imageSrc=image["src"]
        
    fileName=image["data-image-key"]
    downloadImage(imageSrc,name+"."+fileName.split('.')[1])
