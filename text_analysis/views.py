from django.shortcuts import render
from django.http import HttpResponse
from .forms import URLForm
from .utils import get_text_from_url
from .utils import analyze_text
from .utils import analyze_sentiment
from .utils import extract_keywords
from .utils import generate_pdf_report
from .utils import generate_summary
from .utils import detect_fake_news


def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_to_analyze = form.cleaned_data['url_to_analyze']
            text = get_text_from_url(url_to_analyze)
            word_freq = analyze_text(text)
            sentiment = analyze_sentiment(text)
            keywords = extract_keywords(text)
            summary = generate_summary(text)
            fake_news_status = detect_fake_news(summary)

            # Zapisz raport w formie pliku PDF
            generate_pdf_report(url_to_analyze, word_freq, sentiment, keywords, summary, fake_news_status)

            # Przygotuj dane do przekazania do szablonu HTML
            context = {
                'top_words': word_freq.most_common(10),
                'url_to_analyze': url_to_analyze,
                'sentiment': sentiment,
                'keywords': keywords,
                'summary': summary,
                'fake_news_status': fake_news_status
            }

            # Renderuj szablon HTML
            return render(request, 'text_analysis/results.html', context)
    else:
        form = URLForm()

    return render(request, 'text_analysis/home.html', {'form': form})


def download_report(request, url):
    file_path = f"raporty/raport_z_{url.replace('http://', '').replace('https://', '').replace('/', '_')}.pdf"
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(
            pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=raport_{url.replace("http://", "").replace("https://", "").replace("/", "_")}.pdf'
        return response
