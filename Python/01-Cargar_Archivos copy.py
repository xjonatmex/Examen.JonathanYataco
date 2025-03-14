import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyautogui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# 📌 Ruta del archivo Excel
ruta_excel = r"C:\GitHub\Examen.JonathanYataco\Python\Datos.xlsx"

# 📌 URL del formulario de Google
url_formulario = "https://docs.google.com/forms/d/e/1FAIpQLSf5ZsXYdLj0eLa_Nb5L4kYrYYjTH8e2r6wVXQ1y7Q_qHhdVRg/viewform"

# 📌 Configuración de Chrome
opciones = webdriver.ChromeOptions()
opciones.add_argument(r"--user-data-dir=C:\Users\jonathan\AppData\Local\Google\Chrome\User Data")
opciones.add_argument(r"--profile-directory=Default")
opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
opciones.add_experimental_option("useAutomationExtension", False)

# 📌 Inicializar WebDriver
driver = webdriver.Chrome(options=opciones)
driver.get(url_formulario)
time.sleep(3)  # Esperar carga del formulario

# 📌 Leer el archivo Excel
df = pd.read_excel(ruta_excel)

# 📌 Mapeo de campos del formulario con las columnas del Excel
mapeo_campos = {
    "CORREO": {
        "xpath": "//input[@aria-labelledby='i1 i4']",  # Campo de correo
        "tipo": "texto"
    },
    "FECHA DE GASTO": {
        "xpath": "//input[@type='date']",  # Campo de fecha
        "tipo": "fecha"
    }
}

# 📌 Mapeo de los valores de ENTIDAD con sus XPaths en el formulario
mapeo_entidad_xpath = {
    "Secured": "//div[@role='radio' and @data-value='Secured']",
    "Unsecured": "//div[@role='radio' and @data-value='Unsecured']",
    "Post Castigo Secured": "//div[@role='radio' and @data-value='Post Castigo Secured']",
    "Post Castigo Unsecured": "//div[@role='radio' and @data-value='Post Castigo Unsecured']",
    "Extrajudicial": "//div[@role='radio' and @data-value='Extrajudicial']",
    "Venta de cartera": "//div[@role='radio' and @data-value='Venta de cartera']",
    "IRBSA": "//div[@role='radio' and @data-value='IRBSA']"
}

# 📌 Mapeo de los valores de TIPO con sus XPaths en el formulario
mapeo_tipo_xpath = {
    "Banco": "//div[@role='radio' and @data-value='Banco']",
    "IRBSA": "//div[@role='radio' and @data-value='IRBSA']"
}

# 📌 Mapeo de los valores de PORTAFOLIO con sus XPaths en el formulario
mapeo_portafolio_xpath = {
    "Minorista": "//div[@role='radio' and @data-value='Minorista']",
    "Mayorista": "//div[@role='radio' and @data-value='Mayorista']",
    "IRBSA": "//div[@role='radio' and @data-value='IRBSA']"
}


# 📌 Iterar sobre cada fila del archivo
for index, fila in df.iterrows():


    # 📌 Rellenar el campo de "CORREO"
    campo_correo = driver.find_element(By.XPATH, mapeo_campos["CORREO"]["xpath"])
    campo_correo.clear()  # Limpiar la caja antes de ingresar el dato
    correo = fila[0]  # Tomando el correo desde la columna 0
    campo_correo.send_keys(correo)
    time.sleep(1)

    # 📌 Rellenar el campo de "FECHA DE GASTO"
    campo_fecha = driver.find_element(By.XPATH, mapeo_campos["FECHA DE GASTO"]["xpath"])
    if pd.notna(fila["FECHA DE GASTO"]):  # Evitar valores nulos
        fecha_formateada = fila[1].strftime("%d-%m-%Y")
        campo_fecha.send_keys(fecha_formateada)
        campo_fecha.send_keys(Keys.ENTER)
        # 📌 Simular presionar TAB en el teclado
        actions = ActionChains(driver)
        time.sleep(1)
        actions.send_keys(Keys.TAB)
        time.sleep(1)
        actions.send_keys(Keys.TAB)  # Pasa al siguiente control
        actions.send_keys(Keys.ARROW_DOWN)  # Baja una opción en el combo
        time.sleep(2)
        actions.send_keys(Keys.ARROW_DOWN)  # Baja segunda opción
        time.sleep(2)
        actions.send_keys(Keys.ARROW_DOWN)  # Baja tercera opción
        time.sleep(2)
        actions.send_keys(Keys.ARROW_DOWN)  # Baja una opción en el combo
        time.sleep(2)
        actions.send_keys(Keys.ENTER)  # Selecciona la opción
        actions.perform()  # Ejecutar la secuencia de teclas
    else:
        print("⚠️ Advertencia: Fecha inválida en el Excel, saltando fila.")

    time.sleep(2)

   







    # 📌 Seleccionar el radio button de "ENTIDAD"
    entidad = fila[2].strip()  # Asegurarse de que no haya espacios extra

    if entidad in mapeo_entidad_xpath:
        try:
            # 📌 Esperar que el radio button sea interactuable
            campo_entidad = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, mapeo_entidad_xpath[entidad]))
            )

            # 📌 Desplazar la vista hasta el elemento si es necesario
            driver.execute_script("arguments[0].scrollIntoView(true);", campo_entidad)
            time.sleep(1)

            # 📌 Hacer clic en la opción correcta
            campo_entidad.click()
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ No se pudo seleccionar la opción '{entidad}' en la fila {index}. Error: {e}")


    # 📌 Seleccionar el radio button de "TIPO"
    tipo = fila[3].strip()  # Asegurarse de que no haya espacios extra
    if tipo in mapeo_tipo_xpath:
        try:
            # 📌 Esperar que el radio button sea interactuable
            campo_tipo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, mapeo_tipo_xpath[tipo]))
            )

            # 📌 Desplazar la vista hasta el elemento si es necesario
            driver.execute_script("arguments[0].scrollIntoView(true);", campo_tipo)
            time.sleep(1)

            # 📌 Hacer clic en la opción correcta
            campo_tipo.click()
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ No se pudo seleccionar la opción '{tipo}' en la fila {index}. Error: {e}")


    # 📌 Seleccionar el radio button de "PORTAFOLIO"
    portafolio = fila[4].strip()  # Asegurarse de que no haya espacios extra

    if portafolio in mapeo_portafolio_xpath:
        try:
            # 📌 Esperar que el radio button sea interactuable
            campo_portafolio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, mapeo_portafolio_xpath[portafolio]))
            )

            # 📌 Desplazar la vista hasta el elemento si es necesario
            driver.execute_script("arguments[0].scrollIntoView(true);", campo_portafolio)
            time.sleep(1)

            # 📌 Hacer clic en la opción correcta
            campo_portafolio.click()
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ No se pudo seleccionar la opción '{portafolio}' en la fila {index}. Error: {e}")

    # 📌 Localizar el campo de "IMPORTE ITF" (fila 22 del Excel)
    campo_importeitf = driver.find_element(By.XPATH, "//input[@type='text' and @aria-labelledby='i68 i71']")
    campo_importeitf.clear()
    campo_importeitf.send_keys(fila[22])
    time.sleep(1)

    # 📌 Localizar el campo de "CARTA" (fila 6 del Excel)
    campo_carta = driver.find_element(By.XPATH, "//input[@type='text' and @aria-labelledby='i73 i76']")
    campo_carta.clear()
    campo_carta.send_keys(fila[6])
    time.sleep(1)



    # 📌 Localizar el campo de "CÓDIGO UGA" (fila 7 del Excel)
    campo_codigo_uga = driver.find_element(By.XPATH, "//input[@type='text' and @aria-labelledby='i78 i81']")
    campo_codigo_uga.clear()
    campo_codigo_uga.send_keys(fila[7])
    time.sleep(1)


    # 📌 Localizar el campo de "CÓDIGO CENTRAL" (columna 8 del Excel)
    campo_codigo_central = driver.find_element(By.XPATH, "//input[@type='text' and @aria-labelledby='i83 i86']")
    campo_codigo_central.clear()
    campo_codigo_central.send_keys(fila[8])
    time.sleep(1)


    # 📌 Localizar el campo de "NÚMERO DE CONTRATO" (columna 10 del Excel)
    campo_numero_contrato = driver.find_element(By.XPATH, "//input[@type='text' and @aria-labelledby='i88 i91']")
    campo_numero_contrato.clear()
    campo_numero_contrato.send_keys(fila[9])
    time.sleep(1)

    # 📌 Rellenar el campo de "RAZÓN SOCIAL"
    campo_razon_social = driver.find_element(By.XPATH, "//input[@aria-labelledby='i93 i96']")
    campo_razon_social.clear()  # Limpiar la caja antes de ingresar el dato
    campo_razon_social.send_keys(fila[10])  # Tomando el valor de la columna 11 del Excel
    time.sleep(1)



    # 📌 Rellenar el campo de "TIPO GASTO"
    mapeo_tipo_gasto_xpath = {
        "Gasto Notarial - Carta Notarial": "//div[@role='radio' and @data-value='Gasto Notarial - Carta Notarial']",
        "Gasto Notarial - Testimonio de Constitución de hipoteca": "//div[@role='radio' and @data-value='Gasto Notarial - Testimonio de Constitución de hipoteca']",
        "Gasto Notarial - Testimonio de modificación y ampliación": "//div[@role='radio' and @data-value='Gasto Notarial - Testimonio de modificación y ampliación']",
        "Gasto Notarial - Legalización de documentos": "//div[@role='radio' and @data-value='Gasto Notarial - Legalización de documentos']",
        "Gasto Registral - Boleta Informativa Vehicular": "//div[@role='radio' and @data-value='Gasto Registral - Boleta Informativa Vehicular']",
        "Gasto Registral - Certificado de gravamen vehicular": "//div[@role='radio' and @data-value='Gasto Registral - Certificado de gravamen vehicular']",
        "Gasto Registral - Título archivado": "//div[@role='radio' and @data-value='Gasto Registral - Título archivado']",
        "Gasto Registral - Búsqueda de registro de propiedad inmueble": "//div[@role='radio' and @data-value='Gasto Registral - Búsqueda de registro de propiedad inmueble']",
        "Gasto Registral - Búsqueda de registro de propiedad vehicular": "//div[@role='radio' and @data-value='Gasto Registral - Búsqueda de registro de propiedad vehicular']",
        "Gasto Registral - Copia literal de inmueble": "//div[@role='radio' and @data-value='Gasto Registral - Copia literal de inmueble']",
        "Gasto Registral - Certificado de gravamen inmueble": "//div[@role='radio' and @data-value='Gasto Registral - Certificado de gravamen inmueble']",
        "Gasto Judicial - Arancel por solicitud de incautación": "//div[@role='radio' and @data-value='Gasto Judicial - Arancel por solicitud de incautación']",
        "Gasto Judicial - Cédulas de notificación": "//div[@role='radio' and @data-value='Gasto Judicial - Cédulas de notificación']",
        "Gasto Judicial - Servicio de ubicación y captura (Capturador)": "//div[@role='radio' and @data-value='Gasto Judicial - Servicio de ubicación y captura (Capturador)']",
        # Agregar más opciones según el formulario...
    }

    tipo_gasto = str(fila[18]).strip()  # Obtener el valor de la columna 18 (índice 18)

    # 📌 Verificar que el tipo de gasto esté en el mapeo
    if tipo_gasto in mapeo_tipo_gasto_xpath:
            try:
                # 📌 Esperar que el radio button sea interactuable
                campo_tipo_gasto = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, mapeo_tipo_gasto_xpath[tipo_gasto]))
                )

                # 📌 Desplazar la vista hasta el elemento si es necesario
                driver.execute_script("arguments[0].scrollIntoView(true);", campo_tipo_gasto)
                time.sleep(1)

                # 📌 Hacer clic en la opción correcta
                campo_tipo_gasto.click()
                print(f"✅ Seleccionado: {tipo_gasto}")

                time.sleep(1)  # Pequeña pausa antes de continuar
            except Exception as e:
                print(f"⚠️ No se pudo seleccionar el tipo de gasto '{tipo_gasto}': {e}")
    else:
            print(f"❌ Tipo de gasto '{tipo_gasto}' no encontrado en el mapeo.")







    # 📌 Rellenar el campo de "NÚMERO COMPROBANTE"
    campo_numero_comprobante = driver.find_element(By.XPATH, "//input[@aria-labelledby='i256 i259']")
    campo_numero_comprobante.clear()  # Limpiar la caja antes de ingresar el dato
    campo_numero_comprobante.send_keys(fila[12])  # Tomando el valor de la columna 12 del Excel
    time.sleep(1)

    # 📌 Rellenar el campo de "NÚMERO TICKET" solo si tiene valor
    if pd.notna(fila[19]) and str(fila[19]).strip():  # Verifica que no sea NaN ni una cadena vacía
        campo_numero_ticket = driver.find_element(By.XPATH, "//input[@aria-labelledby='i261 i264']")
        campo_numero_ticket.clear()  # Limpiar la caja antes de ingresar el dato
        campo_numero_ticket.send_keys(str(fila[19]))  # Convertir a string para evitar errores
        time.sleep(1)


    # 📌 Rellenar el campo de "BASE IMPONIBLE" solo si tiene un valor válido
    if pd.notna(fila[13]):  # Verifica que no sea NaN
        base_imponible = str(fila[13])  # Convertir directamente a string sin modificar el formato
        campo_base_imponible = driver.find_element(By.XPATH, "//input[@aria-labelledby='i266 i269']")
        campo_base_imponible.clear()  # Limpiar la caja antes de ingresar el dato
        campo_base_imponible.send_keys(base_imponible)  # Ingresar el valor sin alterar
        time.sleep(1)


    # 📌 Rellenar el campo de "IGV" solo si tiene un valor válido
    if pd.notna(fila[21]):  # Verifica que no sea NaN
        igv = str(fila[21])  # Convertir directamente a string sin modificar el formato
        campo_igv = driver.find_element(By.XPATH, "//input[@aria-labelledby='i271 i274']")
        campo_igv.clear()  # Limpiar la caja antes de ingresar el dato
        campo_igv.send_keys(igv)  # Ingresar el valor sin alterar
        time.sleep(1)

    # 📌 Rellenar el campo de "Importe en Soles" solo si tiene un valor válido
    if pd.notna(fila[14]):  # Verifica que no sea NaN
        importe_soles = str(fila[14])  # Convertir a string sin modificar el formato
        campo_importe_soles = driver.find_element(By.XPATH, "//input[@aria-labelledby='i276 i279']")
        campo_importe_soles.clear()  # Limpiar la caja antes de ingresar el dato
        campo_importe_soles.send_keys(importe_soles)  # Ingresar el valor tal cual
        time.sleep(1)

    # 📌 Rellenar el campo de "Nombre de Oficina"
    if pd.notna(fila[15]):  # Verifica que no sea NaN
        nombre_oficina = str(fila[15]).strip()  # Convertir a string y limpiar espacios
        campo_nombre_oficina = driver.find_element(By.XPATH, "//input[@aria-labelledby='i281 i284']")
        campo_nombre_oficina.clear()  # Limpiar la caja antes de ingresar el dato
        campo_nombre_oficina.send_keys(nombre_oficina)  # Ingresar el valor
        time.sleep(1)

    # 📌 Mapeo de valores de "Territorio" con sus XPaths en el formulario
    mapeo_territorio_xpath = {
        "Centro Oriente": "//div[@role='radio' and @data-value='Centro Oriente']",
        "Norte": "//div[@role='radio' and @data-value='Norte']",
        "Lima Centro": "//div[@role='radio' and @data-value='Lima Centro']",
        "Lima Este": "//div[@role='radio' and @data-value='Lima Este']",
        "Lima Norte": "//div[@role='radio' and @data-value='Lima Norte']",
        "Lima Sur": "//div[@role='radio' and @data-value='Lima Sur']",
        "Lima Oeste": "//div[@role='radio' and @data-value='Lima Oeste']",
        "Miraflores": "//div[@role='radio' and @data-value='Miraflores']",
        "Sur": "//div[@role='radio' and @data-value='Sur']",
        "Labour Relation Ships & Compensation": "//div[@role='radio' and @data-value='Labour Relation Ships & Compensation']",
        "Banca Patrimonial y Privada": "//div[@role='radio' and @data-value='Banca Patrimonial y Privada']",
        "BEC Central": "//div[@role='radio' and @data-value='BEC Central']",
        "BEC Regional 1": "//div[@role='radio' and @data-value='BEC Regional 1']",
        "BEC Regional 2": "//div[@role='radio' and @data-value='BEC Regional 2']",
        "BEC Regional 3": "//div[@role='radio' and @data-value='BEC Regional 3']",
        "Operations": "//div[@role='radio' and @data-value='Operations']",
        "Oficina Prime Las Begonias": "//div[@role='radio' and @data-value='Oficina Prime Las Begonias']"
    }

    # 📌 Obtener el valor de "Territorio" desde el archivo Excel
    territorio = str(fila[16]).strip()  # Convertir a string y limpiar espacios extra

    # 📌 Verificar que el territorio esté en el mapeo
    if territorio in mapeo_territorio_xpath:
        try:
            # 📌 Esperar que el radio button sea interactuable
            campo_territorio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, mapeo_territorio_xpath[territorio]))
            )

            # 📌 Desplazar la vista hasta el elemento si es necesario
            driver.execute_script("arguments[0].scrollIntoView(true);", campo_territorio)
            time.sleep(1)

            # 📌 Hacer clic en la opción correcta
            campo_territorio.click()
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ No se pudo seleccionar el territorio '{territorio}': {e}")


    # 📌 Mapeo de valores de "Gestor" con sus XPaths en el formulario
    mapeo_gestor_xpath = {
        "Aracely Requejo": "//div[@role='radio' and @data-value='Aracely Requejo']",
        "Carlos Rodriguez": "//div[@role='radio' and @data-value='Carlos Rodriguez']",
        "Chabeli Rojas": "//div[@role='radio' and @data-value='Chabeli Rojas']",
        "Cynthia Rosales": "//div[@role='radio' and @data-value='Cynthia Rosales']",
        "Martin Cubas": "//div[@role='radio' and @data-value='Martin Cubas']",
        "Eddu Yanavilca": "//div[@role='radio' and @data-value='Eddu Yanavilca']",
        "Alejandra Recavarren": "//div[@role='radio' and @data-value='Alejandra Recavarren']",
        "Mónica Ardián": "//div[@role='radio' and @data-value='Mónica Ardián']",
        "Javier Mejía": "//div[@role='radio' and @data-value='Javier Mejía']",
        "Javier Quinteros": "//div[@role='radio' and @data-value='Javier Quinteros']",
        "Karina Alcántara": "//div[@role='radio' and @data-value='Karina Alcántara']",
        "Rita Cusato": "//div[@role='radio' and @data-value='Rita Cusato']",
        "Abigail Jara": "//div[@role='radio' and @data-value='Abigail Jara']",
        "Mayra Montes": "//div[@role='radio' and @data-value='Mayra Montes']",
        "Maria Lorena Ormeño": "//div[@role='radio' and @data-value='Maria Lorena Ormeño']",
        "Denis Rios": "//div[@role='radio' and @data-value='Denis Rios']",
        "Sioma Torres": "//div[@role='radio' and @data-value='Sioma Torres']",
        "Diego Aranibar": "//div[@role='radio' and @data-value='Diego Aranibar']",
        "Yasmin Gomez": "//div[@role='radio' and @data-value='Yasmin Gomez']"
    }

    # 📌 Obtener el valor de "Gestor" desde el archivo Excel
    gestor = str(fila[17]).strip()  # Convertir a string y limpiar espacios extra

    # 📌 Verificar que el gestor esté en el mapeo
    if gestor in mapeo_gestor_xpath:
        try:
            # 📌 Esperar que el radio button sea interactuable
            campo_gestor = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, mapeo_gestor_xpath[gestor]))
            )

            # 📌 Desplazar la vista hasta el elemento si es necesario
            driver.execute_script("arguments[0].scrollIntoView(true);", campo_gestor)
            time.sleep(1)

            # 📌 Hacer clic en la opción correcta
            campo_gestor.click()
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ No se pudo seleccionar el gestor '{gestor}': {e}")



    # 📌 Esperar y hacer clic en el botón "Siguiente"
    try:
        boton_siguiente = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//span[text()='Siguiente']]"))
        )

        # 📌 Desplazar la vista hasta el botón si es necesario
        driver.execute_script("arguments[0].scrollIntoView(true);", boton_siguiente)
        time.sleep(1)

        # 📌 Hacer clic en el botón
        boton_siguiente.click()
        print("✅ Se hizo clic en 'Siguiente'")
        time.sleep(2)  # Espera antes de continuar
    except Exception as e:
        print(f"⚠️ No se pudo hacer clic en 'Siguiente': {e}")



   # 📌 Obtener el nombre del archivo PDF desde la columna 23
    nombre_pdf = df.iloc[0, 23]  # 22 porque en Python los índices empiezan en 0
    ruta_pdf = f"C:\\PDFBBVA\\{nombre_pdf}.pdf"  # Ruta completa del PDF

   # 📌 Buscar y hacer clic en "Agregar archivo"
    boton_agregar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Agregar archivo')]"))
    )
    boton_agregar.click()
    time.sleep(5)

    
    # 📌 Esperar a que aparezca el iframe y cambiar a él
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'docs.google.com/picker')]"))
    )
    driver.switch_to.frame(iframe)

    # 📌 Esperar y hacer clic en el botón "Explorar" (puede ser un botón tipo input[type=file])
    input_archivo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

    # 📌 Enviar la ruta del archivo PDF
    input_archivo.send_keys(ruta_pdf)

    # 📌 Volver al contexto principal
    driver.switch_to.default_content()
    time.sleep(5)
    # 📌 Esperar y hacer clic en el botón "Enviar"
    boton_enviar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Enviar')]"))
    )
    #boton_enviar.click()

    # 📌 Esperar unos segundos para que el formulario se envíe
    time.sleep(5)

    # 📌 Esperar y cerrar el navegador
    time.sleep(5)


    # 📌 Opcional: Esperar un momento antes de cerrar el navegador
    time.sleep(5)

# driver.quit()  # Cierra el navegador
# Cerrar el navegador al finalizar
# driver.quit()
