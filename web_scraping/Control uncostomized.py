import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Configura le opzioni per Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Esegui Chrome in modalità headless

# Imposta il percorso all'eseguibile ChromeDriver
chrome_service = Service(r'C:\Users\alime\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Aggiorna questo percorso

# Inizializza il WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Variabili di configurazione
current_page = 1
max_pages = 8  # Numero massimo di pagine
save_path = r'C:\Users\alime\Desktop\TESI MAGISTRALE\output_controllo_fem.txt'


# Apri il file di output
with open(save_path, "w", encoding="utf-8") as file:
    while current_page <= max_pages:
        # Costruisci l'URL per la pagina corrente
        URL = f"https://forum.alfemminile.com/discussions/tagged/salute-mentale/p{current_page}"
        driver.get(URL)

        # Aumenta il timeout per gestire il caricamento lento
        wait = WebDriverWait(driver, 5)

        # Attendi il caricamento della sezione dei commenti
        try:
            comments_section = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div[4]/div/div/div/div[2]/section")))
            
            
            # Trova gli elementi contenenti i commenti
            comments = comments_section.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div[4]/div/div/div/div[2]/section/div[2]/table")

            if comments:
                print(f"Pagina {current_page}")
                # Estrai e scrivi il testo di ciascun commento nel file
                for comment in comments:
                    try:
                        title = comment.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div[4]/div/div/div/div[2]/section/div[2]/table/tbody/tr[1]/td[1]").text
                        link = comment.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div[4]/div/div/div/div[2]/section/div[2]/table/tbody/tr[1]/td[1]/div/a")
                        href = link.get_attribute("href")
                        
                        # Clicca sul link per aprire il commento completo
                        driver.execute_script("window.open(arguments[0]);", href)
                        driver.switch_to.window(driver.window_handles[1])
                        
                            
                        # Attendi il caricamento del commento completo
                        full_comment = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div[4]/div/div/div/div[2]/section/section/div[1]/div/div/div[2]/div/div[1]"))).text

                    
                        file.write(f"{title}\n")
                        file.write(f"{full_comment}\n\n")
                        print(f"Title: {title}")
                        print(f"Content: {full_comment}")
                        print("-" * 80 + "\n")

                        # Chiudi la finestra del commento completo e torna alla pagina precedente
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        
                    except Exception as e:
                        print(f"Si è verificato un errore durante l'estrazione dei dati del commento: {e}")

            else:
                print(f"Pagina {current_page}: Nessun commento trovato.")

            # Passa alla pagina successiva
            current_page += 1
            time.sleep(5)  # Attendi il caricamento della pagina successiva

        except Exception as e:
            print(f"Si è verificato un errore durante l'attesa della sezione dei commenti: {e}")
            break

# Chiudi il WebDriver
driver.quit()
