from django.shortcuts import render
from django.http import HttpResponse
from .forms import URLForm
from .utils import get_text_from_url, analyze_text, analyze_sentiment, extract_keywords, save_report_to_pdf


def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_to_analyze = form.cleaned_data['url_to_analyze']
            text = get_text_from_url(url_to_analyze)
            word_freq = analyze_text(text)
            sentiment = analyze_sentiment(text)
            keywords = extract_keywords(text)
            save_report_to_pdf(url_to_analyze, word_freq, sentiment, keywords)
            return render(request, 'text_analysis/results.html', {'top_words': word_freq.most_common(10), 'url_to_analyze': url_to_analyze, 'sentiment': sentiment, 'keywords': keywords})
    else:
        form = URLForm()

    return render(request, 'text_analysis/home.html', {'form': form})


def download_report(request, url):
    file_path = f"raporty/raport_z_{url.replace('http://', '').replace('https://', '').replace('/', '_')}.pdf"
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=raport_{url.replace("http://", "").replace("https://", "").replace("/", "_")}.pdf'
        return response
