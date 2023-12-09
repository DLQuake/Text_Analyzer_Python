import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template


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


def save_report_to_pdf(url, word_freq, sentiment, keywords):
    # Ścieżka do szablonu HTML
    template_path = 'text_analysis/pdf_template.html'
    
    # Kontekst danych do przekazania do szablonu
    context = {
        'url_to_analyze': url,
        'top_words': word_freq.most_common(10),
        'sentiment': sentiment,
        'keywords': ', '.join(keywords)
    }

    # Renderowanie szablonu HTML
    template = get_template(template_path)
    html = template.render(context)

    # Tworzenie strumienia bajtów do zapisu PDF
    result = BytesIO()

    # Utwórz plik PDF z obsługą polskich znaków
    pdf_kwargs = {'encoding': 'UTF-8'}
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=result, encoding='UTF-8', pdf_kwargs=pdf_kwargs)

    if not pdf.err:
        # Zapisz wynikowy plik PDF
        file_path = f"raporty/raport_z_{url.replace('http://', '').replace('https://', '').replace('/', '_')}.pdf"
        with open(file_path, 'wb') as pdf_file:
            pdf_file.write(result.getvalue())


def analyze_sentiment(text):
    # Utwórz obiekt TextBlob
    blob = TextBlob(text)

    # Pobierz sentyment tekstu
    sentiment = blob.sentiment.polarity

    # Oceń sentyment
    if sentiment > 0:
        return 'Pozytywny'
    elif sentiment < 0:
        return 'Negatywny'
    else:
        return 'Neutralny'


def extract_keywords(text):
    # Utwórz wektorizer TF-IDF
    vectorizer = TfidfVectorizer(max_features=10)  # Wybierz maksymalnie 10 słów kluczowych
    tfidf_matrix = vectorizer.fit_transform([text])

    # Pobierz indeksy słów kluczowych
    feature_names = vectorizer.get_feature_names_out()
    keywords_idx = tfidf_matrix.indices

    # Pobierz słowa kluczowe
    keywords = [feature_names[idx] for idx in keywords_idx]

    return keywords
