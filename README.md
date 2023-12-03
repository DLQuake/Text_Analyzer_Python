# Text Analyzer

Projekt Text Analyzer w wersji Django umożliwia analizę tekstu z różnych źródeł, takich jak artykuły z Internetu. Aplikacja zbiera tekst, przeprowadza analizę częstości słów i generuje raport zawierający najczęściej występujące słowa.

## Instalacja

1. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/DLQuake/Text_Analyzer_Python.git
   ```

2. Utwórz i aktywuj wirtualne środowisko (venv):

   ```bash
   cd Text_Analyzer_Python
   py -3 -m venv venv
   source venv/Scripts/activate
   ```

3. Zainstaluj wymagane biblioteki:

   ```bash
   pip install -r requirements.txt
   ```

## Uruchamianie Aplikacji Django

1. Przejdź do folderu projektu Django:

   ```bash
   cd text_analysis_project
   ```

2. Uruchom migracje:

   ```bash
   python manage.py migrate
   ```

3. Uruchom serwer deweloperski:

   ```bash
   python manage.py runserver
   ```

4. Otwórz przeglądarkę i przejdź pod adres http://127.0.0.1:8000/

5. Używaj aplikacji według instrukcji na stronie głównej.

## Użycie

1. Wprowadź link do tekstu do analizy na stronie głównej.

2. Kliknij przycisk "Analizuj".

3. Znajdź wyniki na stronie z wynikami oraz oraz jest możliwość pobrania raportu w formie pliku tekstowego.
