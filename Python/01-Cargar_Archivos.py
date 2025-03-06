from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 📌 Ruta del archivo Excel
ruta_excel = "C:\GitHub\Examen.JonathanYataco\Python\Datos.xlsx" # Ajusta si lo ejecutas localmente

# 📌 URL del formulario de Google
url_formulario = "https://docs.google.com/forms/d/e/1FAIpQLSf5ZsXYdLj0eLa_Nb5L4kYrYYjTH8e2r6wVXQ1y7Q_qHhdVRg/viewform"

# 📌 Configuración de Chrome para abrir en modo usuario
opciones = webdriver.ChromeOptions()
opciones.add_argument(r"--user-data-dir=C:\Users\jonat\AppData\Local\Google\Chrome\User Data")  # Ajusta tu perfil de Chrome
opciones.add_argument(r"--profile-directory=Default")
opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
opciones.add_experimental_option("useAutomationExtension", False)

# 📌 Inicializar WebDriver
driver = webdriver.Chrome(options=opciones)
driver.get(url_formulario)
time.sleep(3)  # Esperar carga del formulario

# 📌 Leer el archivo Excel y asegurarnos de que la fecha está en el formato correcto
df = pd.read_excel(ruta_excel, sheet_name="Hoja1")

# Convertir la columna "FECHA DE GASTO" a formato datetime
df["FECHA DE GASTO"] = pd.to_datetime(df["FECHA DE GASTO"], errors='coerce', dayfirst=True)

# 📌 Mapeo de campos del formulario con las columnas del Excel
mapeo_campos = {
    "CORREO": {
        "xpath": "//input[@aria-labelledby='i1 i4']",  # Campo de correo
        "tipo": "texto"
    },
    "FECHA DE GASTO": {
        "xpath": "//input[@type='date']",  # Campo de fecha
        "tipo": "fecha"
    },
    "UBICACION": {
        "xpath": "//div[@jsname='wQNmvb' and @data-value='Est. Muñiz']",  # Selección en lista
        "tipo": "lista"
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

# 📌 Iterar sobre cada fila del Excel y llenar los campos correspondientes
for _, fila in df.iterrows():
    try:
        # 📌 Rellenar el campo de "CORREO"
        campo_correo = driver.find_element(By.XPATH, mapeo_campos["CORREO"]["xpath"])
        campo_correo.clear()  # Limpiar la caja antes de ingresar el dato
        campo_correo.send_keys(fila["CORREO"])
        time.sleep(1)

        # 📌 Rellenar el campo de "FECHA DE GASTO"
        campo_fecha = driver.find_element(By.XPATH, mapeo_campos["FECHA DE GASTO"]["xpath"])
        if pd.notna(fila["FECHA DE GASTO"]):  # Evitar valores nulos
            fecha_formateada = fila["FECHA DE GASTO"].strftime("%d-%m-%Y")
            campo_fecha.send_keys(fecha_formateada)
        else:
            print("⚠️ Advertencia: Fecha inválida en el Excel, saltando fila.")

        time.sleep(1)


        try:
            # 📌 Obtener el valor de "ENTIDAD" desde el archivo Excel
            entidad = fila["ENTIDAD"].strip()  # Asegurarse de que no haya espacios extra

            # 📌 Verificar que la entidad esté en el mapeo
            if entidad in mapeo_entidad_xpath:
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

            else:
                print(f"⚠️ Advertencia: El valor '{entidad}' no está en la lista de opciones.")

        except Exception as e:
            print(f"⚠️ Error seleccionando la entidad: {e}")

        # 📌 Hacer clic en el botón "Enviar"
        boton_enviar = driver.find_element(By.XPATH, "//span[text()='Enviar']")
        boton_enviar.click()
        time.sleep(3)  # Esperar envío

        # 📌 Recargar formulario para la siguiente fila
        driver.get(url_formulario)
        time.sleep(3)

    except Exception as e:
        print(f"Error al ingresar datos: {e}")

# Mantener el navegador abierto para ver los datos ingresados
input("Presiona Enter para cerrar el navegador...")
driver.quit()
