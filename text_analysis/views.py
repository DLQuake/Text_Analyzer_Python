from django.shortcuts import render
from .utils import get_text_from_url, analyze_text, save_report_to_file
from django.http import HttpResponse
from .forms import URLForm
from urllib.parse import unquote
from urllib.parse import quote
import os


def home(request):
    form = URLForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        url_to_analyze = form.cleaned_data['url_to_analyze']
        text_data = get_text_from_url(url_to_analyze)
        word_freq = analyze_text(text_data)
        save_report_to_file(url_to_analyze, word_freq)

        # Pobierz 10 najczęściej występujących słów
        top_words = word_freq.most_common(10)

        # Użyj quote przed przekazaniem do reverse
        encoded_url = quote(url_to_analyze)

        return render(request, 'text_analysis/results.html', {'top_words': top_words, 'url_to_analyze': url_to_analyze, 'encoded_url': encoded_url})

    return render(request, 'text_analysis/home.html', {'form': form})


def download_report(request, url):
    # Dekoduj zakodowany URL
    decoded_url = unquote(url)
    file_path = f"raporty/raport_z_{decoded_url.replace('http://', '').replace('https://', '').replace('/', '_')}.txt"

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            response = HttpResponse(file.read(), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename=raport_z_{decoded_url.replace("http://", "").replace("https://", "").replace("/", "_")}.txt'
            return response
    else:
        return HttpResponse("Plik nie istnieje.")
