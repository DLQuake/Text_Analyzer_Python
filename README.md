# Text Analyzer

Projekt Text Analyzer umożliwia analizę tekstu z różnych źródeł, takich jak artykuły z Internetu. Skrypt w Pythonie zbiera tekst, przeprowadza analizę częstości słów i generuje raport zawierający najczęściej występujące słowa.

## Instalacja

1. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/DLQuake/Text_Analyzer_Python.git
   ```

2. Utwórz i aktywuj wirtualne środowisko (venv):

   ```bash
   cd Text-Analyzer
   py -3 -m venv venv
   source venv/Scripts/activate  # Dla systemu Unix/Mac # Dla systemu Windows
   ```

3. Zainstaluj wymagane biblioteki:

   ```bash
   pip install -r requirements.txt
   ```

## Użycie

1. Uruchom skrypt i postępuj zgodnie z instrukcjami:

   ```bash
   python main.py
   ```

2. Wprowadź link do tekstu do analizy, a skrypt wygeneruje raport w folderze 'RAPORTY'.

3. Znajdź wyniki w plikach tekstowych w folderze 'RAPORTY'.