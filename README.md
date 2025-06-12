# Opis projektu: System Biblioteczny

## Cel i zakres projektu

Projekt stanowi implementację systemu bibliotecznego, który modeluje złożony problem zarządzania zbiorami mediów (książki, audiobooki), użytkownikami oraz procesami wypożyczeń i rezerwacji. System został zaprojektowany z myślą o dekompozycji problemu na pod-problemy składowe, zgodnie z zasadami SOLID, z wykorzystaniem wzorców projektowych i architektonicznych.

## Technologie

- Python 3.10+
- Flask (interfejs webowy)
- SQLite (baza danych)
- Standardowa biblioteka Python (sqlite3, os)
- Wzorce projektowe: Singleton, Factory, Proxy, Repository, MVC, Command/Registry

## Struktura projektu

```
TO/
├── app.py                # Aplikacja webowa Flask
├── main.py               # Konsolowy interfejs użytkownika
├── lib/
│   ├── db.py             # Singleton DB + inicjalizacja bazy
│   ├── factory.py        # Fabryka mediów (książka, audiobook)
│   └── proxy.py          # Proxy dla książek
├── model/
│   ├── book.py           # Model książki
│   ├── audiobook.py      # Model audiobooka
│   └── user.py           # Model użytkownika
├── repository/
│   ├── BookRepository.py # Repozytorium książek
│   ├── UserRepository.py # Repozytorium użytkowników
│   └── interfaces.py     # Interfejsy repozytoriów
├── service/
│   └── library_service.py # Logika biznesowa i rejestr akcji
├── controller/
│   └── librarycontroller.py # Kontroler (MVC)
├── view/
│   └── consoleview.py    # Widok konsolowy
├── templates/
│   ├── index.html        # Widok listy mediów (Flask)
│   ├── details.html      # Szczegóły książki (Flask)
│   └── add.html          # Formularz dodawania (Flask)
└── README.md
```

## Sposób uruchomienia

1. **Instalacja zależności**  
   (jeśli używasz środowiska wirtualnego, aktywuj je)
   ```
   pip install flask
   ```

2. **Uruchomienie aplikacji webowej (Flask):**
   ```
   python app.py
   ```
   Aplikacja będzie dostępna pod adresem: [http://localhost:5000](http://localhost:5000)

3. **Uruchomienie aplikacji konsolowej:**
   ```
   python main.py
   ```

## Przykładowe użycie

- **Dodawanie książki lub audiobooka:**  
  W interfejsie webowym kliknij "Dodaj nowe medium", wybierz typ, podaj tytuł, autora i ilość.

- **Wypożyczanie, rezerwacja, zwrot, anulowanie rezerwacji:**  
  Wybierz odpowiednią akcję z listy na stronie głównej lub użyj komend w konsoli (`borrow`, `reserve`, `return`).

- **Bezpieczne usuwanie:**  
  Nie można usunąć pozycji, która jest wypożyczona lub zarezerwowana.

## Złożoność i dekompozycja

Złożony problem zarządzania biblioteką został rozbity na następujące pod-problemy:

- **Obsługa różnych rodzajów mediów:** System pozwala na dodawanie i zarządzanie zarówno książkami, jak i audiobookami.
- **Zarządzanie dostępnością i statusami:** Każda pozycja posiada określoną liczbę egzemplarzy. Dostępność jest dynamicznie wyliczana na podstawie liczby wypożyczeń i rezerwacji.
- **Procesy użytkownika:** Użytkownicy mogą wypożyczać, rezerwować, zwracać oraz anulować rezerwacje pozycji.
- **Bezpieczne usuwanie:** System uniemożliwia usunięcie pozycji, która jest aktualnie wypożyczona lub zarezerwowana.
- **Prezentacja i interakcja:** Dostępny jest zarówno interfejs webowy (Flask), jak i konsolowy.

## Zasady SOLID

- **Single Responsibility Principle:** Każda klasa ma jedną odpowiedzialność (np. repozytoria, modele, widoki, kontrolery).
- **Open/Closed Principle:** System jest otwarty na rozszerzenia (np. nowe typy mediów), zamknięty na modyfikacje istniejącego kodu (dzięki fabryce i rejestrowaniu akcji).
- **Liskov Substitution Principle:** Klasy pochodne (np. Audiobook) mogą być używane wszędzie tam, gdzie oczekiwany jest Book.
- **Interface Segregation Principle:** Repozytoria i serwisy mają wąskie, konkretne interfejsy.
- **Dependency Inversion Principle:** Moduły wysokiego poziomu korzystają z repozytoriów przez interfejsy, a nie bezpośrednio z implementacji.

## Wzorce projektowe

- **Singleton:** Zapewnia istnienie tylko jednego połączenia z bazą danych w całej aplikacji (`lib/db.py`).
- **Factory:** Umożliwia dynamiczne tworzenie różnych typów mediów (książka, audiobook) na podstawie typu przekazanego przez użytkownika (`lib/factory.py`).
- **Proxy:** Pośredniczy w dostępie do obiektów książek, umożliwiając np. opóźnione ładowanie (`lib/proxy.py`).
- **Repository:** Oddziela logikę dostępu do danych od logiki biznesowej (`repository/BookRepository.py`, `repository/UserRepository.py`).
- **MVC (Model-View-Controller):**
  - Model: `model/book.py`, `model/audiobook.py`, `model/user.py`
  - Widok: `templates/`, `view/consoleview.py`
  - Kontroler: `controller/librarycontroller.py`, `app.py`, `main.py`
- **Command/Registry:** Pozwala rejestrować i wykonywać różne akcje (wypożyczenie, rezerwacja, zwrot, anulowanie) przez centralny rejestr poleceń (`service/library_service.py`).

---

System jest gotowy do dalszego rozwoju i może być łatwo rozszerzony o nowe typy mediów, dodatkowe procesy lub inne interfejsy użytkownika.
