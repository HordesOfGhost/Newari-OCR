import requests
from bs4 import BeautifulSoup

def get_translation(text, source_lang='new', target_lang='ne'):
    url = f"https://translate.google.com/m?sl={source_lang}&tl={target_lang}&q={text}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the translation in the parsed HTML
    result = soup.find("div", class_="result-container")
    
    if result:
        return result.text.strip()
    else:
        return "Translation not found"

# # Example usage
# input_text = "विदेशं त्यासा"
# translated_text = get_translation(input_text)
# print(f"Input: {input_text}")
# print(f"Output: {translated_text}")