from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import os
import base64
import time

# Configuração do Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Acesse a página
url = "https://tapevideoprodutora.alboompro.com/proof/s/sesi_2024_-_djalma_pessoa"
driver.get(url)

# Criação de pasta para salvar as imagens
output_folder = 'fotinhas'
os.makedirs(output_folder, exist_ok=True)

# Conjunto para armazenar URLs de imagens já capturadas
captured_images = set()

# Função para rolar a página de forma mais suave e capturar imagens
def scroll_and_capture():
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        imgs = driver.find_elements(By.XPATH, "//img | //div[contains(@style, 'background-image')]")
        
        for img in imgs:
            try:
                if img.tag_name == 'img':
                    img_url = img.get_attribute('src')
                elif 'background-image' in img.get_attribute('style'):
                    img_url = img.value_of_css_property('background-image').replace('url("', '').replace('")', '')

                # Verifica se a imagem já foi capturada
                if img_url in captured_images:
                    continue 

                # Adiciona o URL da imagem ao conjunto
                captured_images.add(img_url)

                if img_url and not img_url.startswith('data:'):
                    try:
                        img_data = requests.get(img_url).content
                        img_name = os.path.join(output_folder, img_url.split("/")[-1])
                        with open(img_name, 'wb') as f:
                            f.write(img_data)
                        print(f"Imagem {img_name} salva!")
                    except Exception as e:
                        print(f"Erro ao baixar a imagem {img_url}: {e}")
                elif img_url and img_url.startswith('data:'):  # Para imagens base64
                    try:
                        img_data = img_url.split(',')[1]  # Extrai a parte base64
                        img_extension = img_url.split(';')[0].split('/')[1]  
                        img_name = os.path.join(output_folder, f"image_{imgs.index(img)}.{img_extension}")
                        with open(img_name, 'wb') as f:
                            f.write(base64.b64decode(img_data))  # Decodifica e salva
                        print(f"Imagem base64 {img_name} salva!")
                    except Exception as e:
                        print(f"Erro ao salvar a imagem base64 {img_url}: {e}")
            except Exception as e:
                print(f"Erro ao processar a imagem: {e}")

        # Rola a página devagar
        driver.execute_script("window.scrollBy(0, 100);")  
        time.sleep(3) 
        
        # Verifica se a página rolou
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  
        last_height = new_height


scroll_and_capture()
driver.quit()
