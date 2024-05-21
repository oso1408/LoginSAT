"""Librerias"""
#from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from CE.scraping_arguments import ArgumentsMakeAnEnquery


class PeticionCESelenium:
    """Clase consulta Contabilidad Electronica"""
    def __init__(self, driver, query_uuids, anio_ce, mes_inicial_ce, mes_fin_ce, motivo_ce, tipo_de_archivo_ce, estatus_ce, tipo_envio_ce):
        self.arguments_make_query = ArgumentsMakeAnEnquery()
        self.driver = driver
        self.query_uuids = query_uuids
        self.anio_ce = anio_ce
        self.mes_inicial_ce = mes_inicial_ce
        self.mes_fin_ce = mes_fin_ce
        self.motivo_ce = motivo_ce
        self.tipo_de_archivo_ce = tipo_de_archivo_ce
        self.estatus_ce = estatus_ce
        self.tipo_envio_ce = tipo_envio_ce

    def send_query_uuids(self):
        """Consulta de acuses por Uuids."""
        try:
            txtNoFolio = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, self.arguments_make_query.input_folio)))
            txtNoFolio.send_keys(self.query_uuids)#"123456789")

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, self.arguments_make_query.btn_search))).click()
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.div_table)))
            consulta_content = self.driver.page_source
            return consulta_content
        except Exception as exce:
            raise ValueError("Error: ", exce)

    def send_query_date(self):
        """Consulta de acuses por fecha."""
        try:
            rdoCriterios = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.rbtn_period)))
            rdoCriterios.click()

            ddlAnio = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.input_anio)))
            ddlAnio.send_keys(self.anio_ce)#2015)

            ddlMesInicio = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.input_initial_month)))
            ddlMesInicio.send_keys(self.mes_inicial_ce)#'01 - Enero')

            ddlMesFin = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.input_end_month)))
            ddlMesFin.send_keys(self.mes_fin_ce)#'03 - Marzo')

            ddlMotivo = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.input_reason)))
            ddlMotivo.send_keys(self.motivo_ce)

            ddlTipoArchivo = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.input_type_file)))
            ddlTipoArchivo.send_keys(self.tipo_de_archivo_ce)#'B - Balanzas de Comprobación')

            ddlEstatus = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.input_status)))
            ddlEstatus.send_keys(self.estatus_ce)#'Recibido')

            ddlTipoEnvio = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.input_type_send)))

            if ddlTipoEnvio.get_attribute("disabled"):
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.btn_search))).click()
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.div_table)))
                consulta_content = self.driver.page_source
                return consulta_content
            else:
                ddlTipoEnvio.send_keys(self.tipo_envio_ce)#'Todos')
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.btn_search))).click()
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID,self.arguments_make_query.div_table)))
                consulta_content = self.driver.page_source
                return consulta_content
        except Exception as en:
            ValueError("Error: ", en)