import os
import json

def load_cookies_from_json(nombre_archivo):
    if os.path.isfile(nombre_archivo):
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            cookies_data = json.load(f)
            cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_data}
            return cookies_dict
    else:
        print("El archivo no existe.")
        return None
    
def load_cookies_variable(cookies_data):
    try:
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_data}
        return cookies_dict
    except Exception as e:
        print("Error al cargar las cookies:", e)
        return None