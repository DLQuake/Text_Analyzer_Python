import re
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
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


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


def get_html_content(url, word_freq, sentiment, keywords, summary, fake_news_status):
    # Ścieżka do szablonu HTML
    template_path = 'text_analysis/pdf_template.html'

    # Kontekst danych do przekazania do szablonu
    context = {
        'url_to_analyze': url,
        'top_words': word_freq.most_common(10),
        'sentiment': sentiment,
        'keywords': ', '.join(keywords),
        'summary': summary,
        'fake_news_status': fake_news_status
    }

    # Renderowanie szablonu HTML
    template = get_template(template_path)
    html_content = template.render(context)
    return html_content


def save_report_to_pdf(html_content, url):
    # Tworzenie strumienia bajtów do zapisu PDF
    result = BytesIO()

    # Utwórz plik PDF z obsługą polskich znaków
    pdf_kwargs = {'encoding': 'utf-8'}
    pdf = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')),
                         dest=result, encoding='utf-8', pdf_kwargs=pdf_kwargs)

    if not pdf.err:
        # Zapisz wynikowy plik PDF
        file_path = f"raporty/raport_z_{url.replace('http://', '').replace('https://', '').replace('/', '_')}.pdf"
        with open(file_path, 'wb') as pdf_file:
            pdf_file.write(result.getvalue())


def generate_pdf_report(url, word_freq, sentiment, keywords, summary, fake_news_status):
    html_content = get_html_content(url, word_freq, sentiment, keywords, summary, fake_news_status)
    save_report_to_pdf(html_content, url)


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
    if not text.strip():
        return []

    try:
        cleaned_text = re.sub(r'\W', ' ', text)
        vectorizer = TfidfVectorizer(
            max_features=10, stop_words=stopwords.words('english'))
        tfidf_matrix = vectorizer.fit_transform([cleaned_text])
        feature_names = vectorizer.get_feature_names_out()
        keywords_idx = tfidf_matrix.indices
        keywords = [feature_names[idx] for idx in keywords_idx]

        return keywords

    except Exception as e:
        print(f"An error occurred during text analysis: {e}")
        return []


def generate_summary(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)


def detect_fake_news(text):
    blob = TextBlob(text)
    if blob.sentiment.polarity < -0.2:
        return "Podejrzane informacje"
    else:
        return "Prawdziwe informacje"
