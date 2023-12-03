import os
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter


def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([paragraph.get_text() for paragraph in paragraphs])
    return text


def analyze_text(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word not in stop_words]
    word_freq = Counter(words)
    return word_freq


def save_report_to_file(url, word_freq):
    if not os.path.exists('raporty'):
        os.makedirs('raporty')

    file_name = f"raporty/raport_z_{url.replace('http://', '').replace('https://', '').replace('/', '_')}.txt"

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"Raport dla linku: {url}\n\n")
        file.write("Najczęściej występujące słowa:\n")
        for word, freq in word_freq.most_common(10):
            file.write(f'{word}: {freq} razy\n')
