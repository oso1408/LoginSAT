"""Librerias."""
import requests
from bs4 import BeautifulSoup
from CE.load_cookies_soup import load_cookies_variable
from CE.links_sat import SatLinks
from CE.scraping_arguments import ArgumentsDownloadAcknowledgments


class DownloadacknowledgmentsCE:
    """Funcion para descargar xml de la contabilidad electronica."""
    def __init__(self, html_data, cookies_acuses, ruta_save_xml):
        self.link_sat = SatLinks()
        self.arguments = ArgumentsDownloadAcknowledgments()
        self.html_data = html_data
        self.cookies = cookies_acuses
        self.ruta_save_zip = ruta_save_xml
        
    def export_ce(self):
        """Exportacion de los documentos."""
        folio_list = []
        soup = BeautifulSoup(self.html_data, 'html.parser')

        pleca_error = soup.find(class_=self.arguments.class_plecaerror).find('span')
        total_registros = soup.find('div',id=self.arguments.id_divgridacuses).find(class_=self.arguments.class_fila).find('label')
        leyenda_table = soup.find('div',id=self.arguments.id_divgridacuses).find('td')
        dg_acuses = soup.find('div',id=self.arguments.id_divgridacuses).find('tr', class_=self.arguments.class_encabezado)

        if pleca_error:
            print(pleca_error.text.strip(),'\n')
            return True
        elif dg_acuses:
            msg_total_registros = dg_acuses.find('div', class_=self.arguments.class_fila)
            td_busqueda_xml = soup.find('div', id=self.arguments.id_dacuses).find(class_=self.arguments.class_tabla).find_all('tr')
            print(msg_total_registros.text.strip())

            for folios in td_busqueda_xml:
                celda_folio = folios.find('td', class_=self.arguments.class_acfolio)
                if celda_folio:
                    folio_list.append(celda_folio.get_text())
            print(folio_list)

            for valor in folio_list:
                print(valor)
                return folio_list
        else:
            print(total_registros.text.strip(),'\n',leyenda_table.text.strip())

    def import_ce(self):
        """Importacion de los documentos."""
        indice = -1
        folio_list = []
        name_file_list = []
        msg_download_successful = "Archivos descargados correctamente"
        link_download_xml = self.link_sat.partial_url
        read_cookies = load_cookies_variable(self.cookies)

        soup = BeautifulSoup(self.html_data, 'html.parser')
        pleca_error = soup.find(class_=self.arguments.class_plecaerror).find('span')
        total_registros = soup.find('div',id=self.arguments.id_divgridacuses).find(class_=self.arguments.class_fila).find('label')
        leyenda_table = soup.find('div',id=self.arguments.id_divgridacuses).find('td')
        dg_acuses = soup.find('div',id=self.arguments.id_divgridacuses).find('tr', class_=self.arguments.class_encabezado)

        if pleca_error:
            print(pleca_error.text.strip(),'\n')
            return pleca_error
        elif dg_acuses:
            msg_total_registros = soup.find('div', id=self.arguments.id_divgridacuses).find('div', class_=self.arguments.class_fila)
            td_busqueda_xml = soup.find('div', id=self.arguments.id_dacuses).find(class_=self.arguments.class_tabla).find_all('tr')
            print(msg_total_registros.text.strip())

            for folios in td_busqueda_xml:
                celda_folio = folios.find('td', class_=self.arguments.class_acfolio)
                celda_name_file = folios.find('td', class_=self.arguments.class_acnombrearchivo)
                if celda_folio:
                    folio_list.append(celda_folio.get_text())
                    name_file_list.append(celda_name_file.get_text())
                for folio in folio_list:
                    indice += 1
                    download_xml_zip = requests.get(link_download_xml+folio, cookies=read_cookies, timeout=30)
                    if download_xml_zip.status_code == 200:
                        with open(self.ruta_save_zip+name_file_list[indice], 'wb') as f:
                            f.write(download_xml_zip.content)
                            print("Archivo descargado exitosamente como:", name_file_list[indice])
                    else:
                        print("Error al descargar el archivo:", name_file_list[indice])
                return msg_download_successful
        else:
            print(total_registros.text.strip(),'\n',leyenda_table.text.strip())