import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from bs4 import BeautifulSoup
import re
import psycopg2
from django.conf import settings
import certifi

# TripAdvisor API Key
TRIPADVISOR_KEY = '4DA558B86CE54BF883B26708661637C8'

# Oxylabs Proxy Configuration
USERNAME, PASSWORD = 'liiffe_tester_MIrzJ', '23789Amds_1212'



proxies = {
    'http': f'http://{USERNAME}:{PASSWORD}@realtime.oxylabs.io:60000',
    'https': f'https://{USERNAME}:{PASSWORD}@realtime.oxylabs.io:60000'
}

# Headers para evitar bloqueos
headers = {
    'x-oxylabs-user-agent-type': 'desktop_chrome',
    'x-oxylabs-geo-location': 'US',
    'X-Oxylabs-Render': 'html',
}

def crearURL(ciudad, lugar, categoria, criterio):
    """Genera la URL de TripAdvisor con base en los criterios."""
    urlBase = "https://www.tripadvisor.com.mx/"
    limitacion = "&broadened=false"

    if lugar == 'RESTAURANTE':
        urlBase += f"FindRestaurants?geo={ciudad}&{categoria}={criterio}{limitacion}"
    elif lugar == 'HOTEL':
        urlBase += f"Hotels-{ciudad}&{categoria}={criterio}{limitacion}"

    return urlBase

def scrapingTripAdvisor(urlTripAdvisor):
    """Hace scraping a la URL y guarda el HTML en un archivo."""
    try:
        response = requests.get(urlTripAdvisor, headers=headers, proxies=proxies, verify=True)

        with open('tripadvisor_result.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        return "OK"
    except Exception as e:
        return f"ERROR: {str(e)}"

def extraerEnlaces():
    """Extrae los enlaces con los identificadores de lugares desde el HTML."""
    try:
        with open("tripadvisor_result.html", "r", encoding="utf-8") as file:
            contenido = file.read()

        soup = BeautifulSoup(contenido, "lxml")

        # Clases CSS donde se encuentran los enlaces
        clases = {"BMQDV", "_F", "Gv", "wSSLS", "SwZTJ", "FGwzt", "ukgoS"}
        enlaces_a = soup.find_all("a", class_=lambda c: c and any(cls in c.split() for cls in clases))

        # Extraer y filtrar los href que contengan "Restaurant_Review"
        enlaces_filtrados = {a["href"] for a in enlaces_a if a.has_attr("href") and "Restaurant_Review" in a["href"]}

        return enlaces_filtrados
    except Exception as e:
        return set()

def extraerIdentificadores(enlaces):
    """Obtiene los identificadores de los lugares desde las URLs extraídas."""
    patron = r"g\d+-d(\d+)"
    identificadores = {match.group(1) for url in enlaces if (match := re.search(patron, url))}
    return identificadores

def obtenerLugar(idPlace):
    """Consulta la API de TripAdvisor para obtener detalles de un lugar."""
    try:
        url = f"https://api.content.tripadvisor.com/api/v1/location/{idPlace}/details?key={TRIPADVISOR_KEY}&language=es&currency=USD"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers, verify=certifi.where())
        return response.json()
    except:
        return {"error": "Lugar no encontrado"}


def consultarLugares(category, tag, place):
    
    conexion = None
    cursor = None
    
    # Obtener configuración de la base de datos
    db_config = settings.DATABASES['default']
    
    try:
        # Conexión a la base de datos
        conexion = psycopg2.connect(            
            host=db_config['HOST'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            database=db_config['NAME'],
            port=db_config['PORT']
        )
        cursor = conexion.cursor()        
        consulta_sql = """
            SELECT id_element, category_url    
            FROM public.categoriestripadvisor  
            WHERE category = %s 
            AND tag = %s 
            AND place = %s;
        """
        cursor.execute(consulta_sql, (category, tag, place))  
        resultados = cursor.fetchall() 

        return resultados

    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None

    finally:
     
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()



@api_view(['GET'])
def obtener_lugares(request):
    """Endpoint para obtener detalles de lugares desde TripAdvisor."""

    # Obtener parámetros de la solicitud con valores por defecto
    categoria = request.GET.get('categoria', 'ESTABLECIMIENTO')
    tag = request.GET.get('tag', 'POSTRES')

    print("categoria ",categoria)
    print("tag ",tag)
    
    # Criterios por defecto
    lugar = "RESTAURANTE"    
    idCiudad = 187497 #BARCELONA

    idTag = ""
    categoriaUrl = ""

    
    resultados = consultarLugares(categoria, tag, lugar)
    if resultados:
        for fila in resultados:        
            idTag = fila[0]
            categoriaUrl = fila[1]


    # 1. Crear la URL de TripAdvisor
    urlTripAdvisor = crearURL(idCiudad, lugar, categoriaUrl, idTag)

    # 2. Hacer scraping de la URL con Oxylabs
    scraping_result = scrapingTripAdvisor(urlTripAdvisor)
    if scraping_result != "OK":
        return Response({'error': scraping_result}, status=500)

    # 3. Extraer enlaces con identificadores de lugares
    enlaces = extraerEnlaces()
    if not enlaces:
        return Response({'error': 'No se encontraron enlaces'}, status=404)

    # 4. Extraer IDs de los lugares
    ids_lugares = extraerIdentificadores(enlaces)
    if not ids_lugares:
        return Response({'error': 'No se encontraron identificadores válidos'}, status=404)

    # 5. Consultar la API de TripAdvisor para obtener detalles
    lugares_info = [obtenerLugar(idPlace) for idPlace in ids_lugares]

    return Response(lugares_info)
