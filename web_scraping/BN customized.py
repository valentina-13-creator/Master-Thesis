from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure options for Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome

# Set path to the ChromeDriver executable
chrome_service = Service(r'C:\Users\alime\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Update this path

# Initialize the WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Open the target URL
url = "https://forum.alfemminile.com/search?domain=all_content&query=bulimia&page=3&scope=site&source=community"
driver.get(url)

# Increase the timeout to handle slow loading
wait = WebDriverWait(driver, 20)

# Print the page source for debugging
try:
    time.sleep(10)  # Wait for the page to load completely
    print(driver.page_source)
except Exception as e:
    print(f"An error occurred while waiting for the page to load: {e}")

# Close the WebDriver
driver.quit()

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Funzioni per la verifica delle condizioni
def count_occurrences(patterns, text):
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count

def contains_past_reference(text):
    past_phrases = [
        r'\bstavo cadendo in\b(?:\W+\w+){0,5}\W*\bbulimia\b',
        r'\bsono caduta in\b(?:\W+\w+){0,5}\W*\bbulimia\b',
        r'\bsono caduto in\b(?:\W+\w+){0,5}\W*\bbulimia\b',
        r'\bsono stata\b(?:\W+\w+){0,8}\W*\bbulimica\b',
        r'\bho sofferto\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\bho avuto\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\bsono stato\b(?:\W+\w+){0,8}\W*\bbulimico\b',
        r'\bsofferto di\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\bbambina\b(?:\W+\w+){0,8}\W*\bbulimica\b',
        r'\bbambina\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\bbambino\b(?:\W+\w+){0,8}\W*\bbulimico\b',
        r'\badolescente\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\badolescente\b(?:\W+\w+){0,8}\W*\bbulimica\b',
        r'\badolescente\b(?:\W+\w+){0,8}\bbulimica\b',
        r'\badolescente\b(?:\W+\w+){0,8}\bbulimia\b',
        r'\bpassato\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\bpassato\b(?:\W+\w+){0,8}\W*\bbulimica\b',
        r'\bpassato\b(?:\W+\w+){0,6}\W*\bbulimico\b',
        r'\bdai \d+ ai \d+ anni\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\banno di\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\banno in\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\bnon sono mai caduta\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\blontana\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\blontano\b(?:\W+\w+){0,8}\W*\bbulimia\b',
        r'\bho avuto problemi\b(?:\W+\w+){0,11}\W*\bbulimia\b'
    ]
    return any(re.search(phrase, text, re.IGNORECASE) for phrase in past_phrases)

def contains_present_reference(text):
    present_phrases = [
        r"\btutt'ora\b(?:\W+\w+){0,10}\W*\bbulimia\b",
        r"\bbulimia\b(?:\W+\w+){0,9}\W*\btutt'ora\b",
        r"\bancora\b(?:\W+\w+){0,10}\W*\bbulimia\b",
        r"\bbulimia\b(?:\W+\w+){0,9}\W*\bancora\b",
        r"\btutt'oggi\b(?:\W+\w+){0,10}\W*\bbulimia\b",
        r"\bbulimia\b(?:\W+\w+){0,9}\W*\btutt'oggi\b",
        r"\bho iniziato\b(?:\W+\w+){0,5}\W*\bsempre più\babbuffata\b",
        r"\bho iniziato\b(?:\W+\w+){0,5}\W*\bsempre più\babbuffate\b"
    ]
    return any(re.search(phrase, text, re.IGNORECASE) for phrase in present_phrases)

def extract_contexts(text, keywords, window=15):
    words = text.split()
    contexts = []

    for keyword in keywords:
        keyword_indices = [i for i, word in enumerate(words) if re.search(r'\b' + re.escape(keyword) + r'\b', word, re.IGNORECASE)]
        for index in keyword_indices:
            start = max(0, index - window)
            end = min(len(words), index + window + 1)
            context = ' '.join(words[start:end])
            contexts.append(context)

    return contexts

def is_relevant_comment(text):
    # Liste di verbi presenti e passati
    present_verbs = [r'\bsono\b', r'\bho\b', r'\bvivo\b', r'\bfaccio\b', r'\bassumo\b', r'\bsto\b', r'\bho\b', r'\bmangio\b', r'\bvomito\b', r'\bsento\b', r'\bpenso\b', r'\bsoffro\b', r'\bvoglio\b', r'\bcerco\b', r'\bso\b', r'\bposso\b', r'\bdevo\b', r'\briesco\b', r'\bvorrei\b', r'\bpotrei\b', r'\bdovrei\b', r'\briuscirei\b', r'\bavrei\b', r'\bsarei\b']
    past_verbs = [r'\bstavo\b', r'\bfacevo\b', r'\bvivevo\b', r'\bassumevo\b', r'\bavevo\b', r'\bmangiavo\b', r'\bvomitavo\b', r'\bsentivo\b', r'\bpensavo\b', r'\bsoffrivo\b', r'\bvolevo\b', r'\bcercavo\b', r'\bsapevo\b', r'\bpotevo\b', r'\bdovevo\b', r'\briuscivo\b']

    # Liste di verbi in prima persona e di altre persone
    first_person_verbs = present_verbs
    other_person_verbs = [r'\bè\b', r'\bvive\b', r'\bha\b', r'\bmangia\b', r'\bvomita\b', r'\bsente\b', r'\bpensa\b', r'\bsoffre\b', r'\bvogliono\b']

    # Liste di pronomi
    first_person_pronouns = [r'\bio\b', r'\bme\b', r'\bmio\b', r'\bmia\b', r'\bmiei\b', r'\bmie\b', r'\w+mi\b', r'\bmi\b']
    other_pronouns = [r'\blui\b', r'\blei\b', r'\bsuo\b', r'\bsua\b', r'\bsuoi\b', r'\bsue\b']

    # Conta le occorrenze di verbi presenti e passati
    present_count = count_occurrences(present_verbs, text)
    past_count = count_occurrences(past_verbs, text)

    # Conta le occorrenze di pronomi in prima persona e di altre persone
    first_person_count = count_occurrences(first_person_pronouns, text)
    other_pronouns_count = count_occurrences(other_pronouns, text)

    # Conta le occorrenze di verbi in prima persona e di altre persone
    first_person_verbs_count = count_occurrences(first_person_verbs, text)
    other_person_verbs_count = count_occurrences(other_person_verbs, text)

    # Escludi i commenti con parole chiave indesiderate
    unwanted_keywords = [r'\bnon ho mai sofferto di\b(?:\W+\w+){0,2}\W*\bbulimia\b', r'\bmia moglie\b', r'\bnon è mai sfociata in\b(?:\W+\w+){0,2}\W*\bbulimia\b', r'\bmi ha fatto guarire\b(?:\W+\w+){0,2}\W*\bbulimia\b', r'\bsono guarita\b(?:\W+\w+){0,2}\W*\bbulimia\b']
    if any(re.search(keyword, text, re.IGNORECASE) for keyword in unwanted_keywords):
        return False

    # Controlla i riferimenti passati
    if contains_past_reference(text) and not contains_present_reference(text):
        return False

    # Verify general conditions
    if present_count > past_count and first_person_count > other_pronouns_count and first_person_verbs_count > other_person_verbs_count and len(text.split()) > 135:
      return True
    elif present_count > past_count and first_person_count > other_pronouns_count and first_person_verbs_count > other_person_verbs_count and len(text.split()) <= 135:
            # Check context around the keywords "bulimia" and "malattia"
            keywords = ["bulimia", "malattia", 'abbuffarmi', "abbuffata", "abbuffate"]
            contexts = extract_contexts(text, keywords)
            for context in contexts:
                context_first_person_verbs_count = count_occurrences(first_person_verbs, context)
                context_other_person_verbs_count = count_occurrences(other_person_verbs, context)


                if context_first_person_verbs_count > context_other_person_verbs_count:
                  return True

    return False

# Configura le opzioni per Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Esegui Chrome in modalità headless

# Imposta il percorso all'eseguibile ChromeDriver
chrome_service = Service(r'C:\Users\alime\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Aggiorna questo percorso

# Inizializza il WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Variabili di configurazione
current_page = 215
max_pages = 267  # Numero massimo di pagine
output_file = "output_bulimia_fem.txt"

# Apri il file di output
with open(output_file, "w", encoding="utf-8") as file:
    while current_page <= max_pages:
        # Costruisci l'URL per la pagina corrente
        URL = f"https://forum.alfemminile.com/search?domain=places&query=bulimia&page={current_page}&scope=site&source=community"
        driver.get(URL)

        # Aumenta il timeout per gestire il caricamento lento
        wait = WebDriverWait(driver, 20)

        # Attendi il caricamento della sezione dei commenti
        try:
            comments_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pageBoxNoCompat.css-10oxk8k")))
            
            # Trova gli elementi contenenti i commenti
            comments = comments_section.find_elements(By.CSS_SELECTOR, "div.css-1gk1rmt-ListItem-styles-item")

            if comments:
                print(f"Pagina {current_page}")
                # Estrai e scrivi il testo di ciascun commento nel file
                for comment in comments:
                    try:
                        title = comment.find_element(By.CSS_SELECTOR, "div.css-k17v61-ListItem-styles-titleContainer").text
                        link = comment.find_element(By.CSS_SELECTOR, "a.css-9iw9as-ListItem-styles-titleLink")
                        href = link.get_attribute("href")
                        
                        # Clicca sul link per aprire il commento completo
                        driver.execute_script("window.open(arguments[0]);", href)
                        driver.switch_to.window(driver.window_handles[1])
                        
                        # Verifica se esiste un bottone per tornare alla prima pagina delle risposte
                        try:
                            first_page_button = driver.find_element(By.CSS_SELECTOR, "a.Pager-p.p-1.FirstPage")
                            first_page_button.click()
                            
                            # Attendi il caricamento della prima pagina
                            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.Message.userContent")))
                        except Exception:
                            pass  # Il bottone non esiste, quindi siamo già sulla pagina giusta

                        # Attendi il caricamento del commento completo
                        full_comment = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.Message.userContent"))).text

                        if ("bulimia" in full_comment.lower() or "bulimia" in title.lower()) and is_relevant_comment(full_comment):
                            # Scrivi titolo e contenuto completo nel file
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
            time.sleep(15)  # Attendi il caricamento della pagina successiva

        except Exception as e:
            print(f"Si è verificato un errore durante l'attesa della sezione dei commenti: {e}")
            break
    
# Chiudi il WebDriver
driver.quit()