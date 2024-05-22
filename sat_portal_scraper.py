"""Librerias."""
import argparse
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from CE.config_webdriver import DriverConfig
from CE.fiel_session_manager import SatWebBase
from CE.verify_cookies import CookiesManager
from CE.make_an_enquery import PeticionCESelenium
from CE.links_sat import SatLinks
from CE.scraping_arguments import ArgumentsLogin
from download_acknowledgments import DownloadacknowledgmentsCE


class SATPortalScraper:
    """Clase scraper portal SAT."""
    def __init__(self):
        self.intentos = 0
        self.driver = webdriver.Chrome(options=DriverConfig().config_headless())
        #self.driver = webdriver.Chrome()
        self.credentials = "config.json"
        self.cookies_manager = CookiesManager()
        self.link_sat = SatLinks()
        self.arguments_id_login = ArgumentsLogin()
        self.download_acuse_cf = None

        parser = argparse.ArgumentParser(description='Manual Para Usar Este Script')
        parser.add_argument('-c', '--credentials_path', type=str, default=None, help='Ruta de la carpeta donde se encuentran las credenciales')
        parser.add_argument('-r', '--rfc', type=str, default=None, help='RFC de la empresa')
        parser.add_argument('-y', '--year', type=int, default=None, help='Año - ingrese año entre el 2015 al año actual')
        parser.add_argument('-i', '--initial_month', type=str, default=None, help='Mes inicial (01 - Enero --- 12 - Diciembre, 13 - Ajuste al cierre)')
        parser.add_argument('-e', '--end_month', type=str, default=None, help='Mes final (01 - Enero --- 12 - Diciembre, 13 - Ajuste al cierre)')
        parser.add_argument('-m', '--reason', type=str, default=None, help='Motivo por el envio de la contabilidad electronica')
        parser.add_argument('-ta', '--type_of_file', type=str, default=None, help='Tipo de archivo (CT, B, PL, XF, XC)')
        parser.add_argument('-es', '--status', type=str, default=None, help='Estatus del archivo (Recibido, Aceptado, Rechazado, Todos)')
        parser.add_argument('-te', '--type_of_send', type=str, default=None, help='tipo de envio (N, C)')
        parser.add_argument('-o', '--output_path', type=str, default=None, help='Ruta donde se guardara los archivos descargados')
        parser.add_argument('-f', '--folio', type=str, default=None, help='Folio del acuse (opcional)')
        args = parser.parse_args()

        self.credentials_path = str(args.credentials_path)
        self.rfc = str(args.rfc)
        self.query_folio = None
        self.anio_ce = str(args.year)
        self.mes_inicial_ce = str(args.initial_month)
        self.mes_fin_ce = str(args.end_month)
        self.motivo_ce = str(args.reason)
        self.tipo_de_archivo_ce = str(args.type_of_file)
        self.estatus_ce = str(args.status)
        self.tipo_envio_ce = str(args.type_of_send)
        self.output_path=str(args.output_path)
        self.sat_web_base = SatWebBase(self.driver, self.credentials_path)
        self.peticion_selenium = PeticionCESelenium(self.driver, self.query_folio, self.anio_ce, self.mes_inicial_ce, self.mes_fin_ce, self.motivo_ce, self.tipo_de_archivo_ce, self.estatus_ce, self.tipo_envio_ce)

    def login(self):
        """Funcion login Access Manager """
        inicio = time.time()
        self.intentos = 0
        self.driver.get(self.link_sat.acess_manager)
        if self.cookies_manager.load_cookies(self.driver, self.rfc):
            if self.cookies_manager.validate_expiration_cookies(self.driver):
                self._proceed_with_query()
            else:
                self._refresh_cookies_and_proceed()
        else:
            self.driver.delete_all_cookies()
            self._login_and_proceed()
        fin = time.time()
        print(f"\n tiempo de ejecucion main --- {fin-inicio}")
        time.sleep(10)

    def _proceed_with_query(self):
        print("Espere un momento, Redirigiendo... \n")
        self.driver.get(self.link_sat.contabilidad_electronica)
        try:
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH,self.arguments_id_login.div_c_acuses)))
            html_data = self.query_by()
            cookies_page = self.driver.get_cookies()
            self.download_acuse_cf = DownloadacknowledgmentsCE(html_data, cookies_page, self.output_path)
            print(self.download_acuse_cf.import_ce())
        except Exception as msg_error:
            raise ValueError("Ocurrio un error: ", msg_error)

    def _refresh_cookies_and_proceed(self):
        while self.intentos < 3:
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_id_login.btn_fiel))).click()
                msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.arguments_id_login.div_a_efirma))).text
                if msg:
                    self.intentos = 3
                    CookiesManager().remove_cookies(self.driver, self.rfc)
                    login_fiel = self.sat_web_base.efirma_login()
                    try:
                        if login_fiel !='':
                            CookiesManager().save_cookies(self.driver, login_fiel)
                            print("Cookies actualizadas")
                            self._proceed_with_query()
                        else:
                            print("Ocurrio un error: No se actualizaron las cookies reintente de nuevo.")
                    except Exception as exc:
                        raise ValueError("Ocurrio un error: ", exc)
            except Exception:
                self.driver.delete_all_cookies()
                print(f"Aun no carga la pagina intento # {self.intentos + 1}")
                self.intentos += 1
                if self.intentos == 3:
                    print("Intentos agotados, el portal del sat no se cargo correctamente \n")

    def _login_and_proceed(self):
        try:
            self.driver.get(self.link_sat.acess_manager)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID,self.arguments_id_login.btn_fiel))).click()
            print("Espere un momento, Redirigiendo al formulario\n")
            login_fiel = self.sat_web_base.efirma_login()
            if login_fiel !='':
                CookiesManager().save_cookies(self.driver, login_fiel)
                print("se actualizaron las cookies")
                self._proceed_with_query()
            else:
                print("ocurrio un error")
        except ValueError as ex:
            print("Ocurio un Error: ", ex)

    def query_by(self):
        try:
            if self.query_folio is None:
                html_data = self.peticion_selenium.send_query_date()
                return html_data
            else:
                html_data = self.peticion_selenium.send_query_uuids()
                return html_data
        except Exception as exq:
            raise ValueError("Ocurrio un error: ", exq)

# Uso de la clase
scraper = SATPortalScraper()
scraper.login()