"""Librerias."""
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from CE.scraping_arguments import ArgumentsLogin


class CookiesManager:
    """verificamos cookies."""
    @staticmethod
    def save_cookies(driver, _rfc):
        """funcion que se encarga de salvar las cookies"""
        folder_path = os.path.join("AppData", _rfc)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        cookies = driver.get_cookies()
        
        file_path = os.path.join(folder_path, 'cookies-'+_rfc+'.json')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(cookies, file)
        print("Nuevas cookies guardadas correctamente \n")

    @staticmethod
    def remove_cookies(driver, _rfc):
        """Elimina los registros de cookies del archivo 'cookies.json'."""
        folder_path = os.path.join("AppData", _rfc)
        path_cookies = folder_path+'\\cookies-'+_rfc+'.json'
        if os.path.exists(folder_path):
            os.remove(path_cookies)
            driver.delete_all_cookies()
            print("Registros de cookies eliminados correctamente \n")
            
    @staticmethod
    def replace_cookies(driver):
        """Elimina los registros de cookies del archivo 'cookies.json'."""
        if 'cookies.json' in os.listdir():
            with open('cookies.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps([]))
            driver.delete_all_cookies()
            print("Registros de cookies eliminados correctamente \n")
            return True
        else:
            print('No se encontró el archivo cookies remove \n')
            return False
        
    @staticmethod
    def load_cookies(driver, _rfc):
        """carga las cookies previamente guardadas."""
        #link_sat = SatLinks()
        #link_acessmanager = link_sat.acess_manager
        #driver.get(link_acessmanager)
        folder_path = os.path.join("AppData", _rfc)
        path_cookies = folder_path+'\\cookies-'+_rfc+'.json'
        if os.path.exists(path_cookies):
            with open(path_cookies, 'r', encoding='utf-8') as file:
                cookies = json.load(file)
                
            for cookie in cookies:
                driver.add_cookie(cookie)
            
            print("Cargando Cookies, espere...")
            return True
        else:
            print('No se encontró el archivo cookies-'+_rfc+'.json')
            return False
        
    @staticmethod
    def validate_expiration_cookies(driver):
        """Verifica la validez de todas las cookies en el archivo JSON."""        
        arguments_login = ArgumentsLogin()
        intentos = 0
        while intentos < 3:
            try:
                titulo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, arguments_login.div_acces_manager))).text
                if titulo == 'Access Manager':
                    intentos = 3
                    print("Se inicio sesion anteriormente, redirigiendo...")
                    return True
            except Exception:
                intentos += 1
                print(f"No cargo la pagina, intento # {intentos}")
                if intentos == 3:
                    print("Cookies vencidas, Redirigiendo...")
                    return False
                    