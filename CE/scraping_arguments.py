"""Clase argumentos portal SAT."""

class ArgumentsLogin:
    """Argumentos login AcessManeger selenium."""
    input_cer = "fileCertificate"
    input_key = "filePrivateKey"
    input_pasword = "privateKeyPassword"
    btn_fiel = "buttonFiel"
    btn_enviar = "submit"
    div_a_efirma = "//h3[contains(.,'Acceso con e.firma')]"
    div_rfc = "//div[@class='GJIDORCJO']"
    div_msg_alert = "//div[contains(@class,'alert alert-danger')]"
    div_acces_manager = "//span[contains(.,'Access Manager')]"
    div_c_acuses = "//div[@class='titulo']"

class ArgumentsMakeAnEnquery:
    """Argumentos scraping busqueda acuses selenium."""
    rbtn_period = "rdoCriterios"
    input_folio = "txtNoFolio"
    input_anio = "ddlAnio"
    input_initial_month = "ddlMesInicio"
    input_end_month = "ddlMesFin"
    input_reason = "ddlMotivo"
    input_type_file = "ddlTipoArchivo"
    input_status = "ddlEstatus"
    input_type_send = "ddlTipoEnvio"
    div_table = "dAcuses"
    btn_search = "btnBuscar"

class ArgumentsDownloadAcknowledgments():
    """Argumentos scraping Beatifulsoup."""
    label = "label"
    div = "div"
    td = "td"
    tr = "tr"
    span = "span"
    id_divgridacuses = "divGridAcuses"
    id_dacuses = "dAcuses"
    class_plecaerror = "plecaError"
    class_fila = "fila"
    class_encabezado = "encabezado"
    class_tabla = "tabla"
    class_acfolio = "acFolio"
    class_acnombrearchivo = "acNombreArchivo"
