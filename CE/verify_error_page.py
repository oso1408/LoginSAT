"""Librerias."""
from bs4 import BeautifulSoup

def verify_login_susseful(html_content):
    """Funcion verificacion contenedor de mensaje de error."""
    soup = BeautifulSoup(html_content, 'html.parser')
    div_row = soup.find('div', class_='row')
    if div_row:
        div_error = div_row.find('div', id='divError')
        msg_div = div_error.text.strip()
        return msg_div
    else:
        return False