"""Librerias"""
import time
#from datetime import datetime, timezone
from pathlib import Path
#from cryptography import x509
from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
#from cryptography.hazmat.backends import default_backend
from CE.search_and_read_credentials import ReadPathCredentials
from CE.scraping_arguments import ArgumentsLogin
from CE.verify_error_page import verify_login_susseful

#Checar porque falla la funcion de certificado_der x503
class SatWebBase:
    """inicializamos el driver."""
    def __init__(self, driver, credentials_path):
        self.driver = driver
        self._credentials_path = credentials_path
        self.read_path = ReadPathCredentials()
        self.arguments_id_login = ArgumentsLogin()

    def efirma_login(self):
        """valida credenciales."""
        inicio = time.time()
        path_ruta_certificado = Path(self.read_path.search_files_path(self._credentials_path, '.cer'))
        path_ruta_key = Path(self.read_path.search_files_path(self._credentials_path, '.key'))
        credential_cer = self.read_path.search_files_path(self._credentials_path, '.cer')
        credential_key = self.read_path.search_files_path(self._credentials_path, '.key')
        credential_private_key = self.read_path.read_password(self._credentials_path)
        #credential_rfc = self.load_credential.load_credetial_rfc()
        try:
            if not path_ruta_certificado.is_file():
                raise ValueError("No existe el certificado en la ruta: " + self._credentials_path+'\\'+credential_cer)
            if not path_ruta_key.is_file():
                raise ValueError("No existe el certificado en la ruta: "+ self._credentials_path,credential_key)
            if credential_private_key is None:
                raise ValueError("No se ha especificado la contraseña de clave privada")
            if path_ruta_certificado.suffix != ".cer":
                raise ValueError("El certificado no es válido, se requiere un archivo *.cer")
            if path_ruta_key.suffix != ".key":
                raise ValueError("El certificado no es válido, se requiere un archivo *.key")

            with open(credential_cer, 'rb') as archivo_certificado:
                contenido_certificado = archivo_certificado.read()

            #certificado_der = x509.load_der_x509_certificate(contenido_certificado, default_backend())

            if not 'fiel' in self.driver.current_url:
                raise ValueError("No se logró cargar la página del login por efirma.")

            self.driver.find_element(By.ID, self.arguments_id_login.input_cer).send_keys(credential_cer)
            self.driver.find_element(By.ID, self.arguments_id_login.input_key).send_keys(credential_key)
            self.driver.find_element(By.ID, self.arguments_id_login.input_pasword).send_keys(credential_private_key)

            #fecha_validez = certificado_der.not_valid_after_utc

            #if fecha_validez < datetime.now(timezone.utc):
            #    raise ValueError("No se puede iniciar sesión: E.FIRMA Vencida \n")

            self.driver.find_element(By.ID, self.arguments_id_login.btn_enviar).click()

            content_page = self.driver.page_source
            div_error = verify_login_susseful(content_page)

            if div_error:
                raise ValueError(div_error)
            else:
                pass

            fin = time.time()
            print(f"Sesión iniciada correctamente {fin - inicio}")
            return True

        except ValueError as e:
            #print("Error. Ocurrio un error en el proceso:", e)
            raise ValueError("Error. Ocurrio un error en el proceso: ", e)