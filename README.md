# Opis projektu: System Biblioteczny

## Cel i zakres projektu

Projekt stanowi implementację systemu bibliotecznego, który modeluje złożony problem zarządzania zbiorami mediów (książki, audiobooki), użytkownikami oraz procesami wypożyczeń i rezerwacji. System został zaprojektowany z myślą o dekompozycji problemu na pod-problemy składowe, zgodnie z zasadami SOLID, z wykorzystaniem wzorców projektowych i architektonicznych.

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

- **Factory:** Umożliwia dynamiczne tworzenie różnych typów mediów (książka, audiobook) na podstawie typu przekazanego przez użytkownika (`lib/factory.py`).
- **Proxy:** Pośredniczy w dostępie do obiektów książek, umożliwiając np. opóźnione ładowanie (`lib/proxy.py`).
- **Repository:** Oddziela logikę dostępu do danych od logiki biznesowej (`repository/BookRepository.py`, `repository/UserRepository.py`).
- **MVC (Model-View-Controller):**
  - Model: `model/book.py`, `model/audiobook.py`, `model/user.py`
  - Widok: `templates/`, `view/consoleview.py`
  - Kontroler: `controller/librarycontroller.py`, `app.py`, `main.py`
- **Command/Registry:** Pozwala rejestrować i wykonywać różne akcje (wypożyczenie, rezerwacja, zwrot, anulowanie) przez centralny rejestr poleceń (`service/library_service.py`).
- **Observer (uproszczony):** Powiadamia użytkowników o zmianie statusu książki (`model/book.py`).

System jest gotowy do dalszego rozwoju i może być łatwo rozszerzony o nowe typy mediów, dodatkowe procesy lub inne interfejsy użytkownika.
