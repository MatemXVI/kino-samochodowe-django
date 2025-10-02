Wersja 2.1 aplikacja webowej stworzonej we frameworku Django - system do zarządzania kinem samochodowym.  Projekt powstał na bazie wcześniejszej aplikacji w czystym PHP i został przerobiony na framework Django w języku Python, naprawiono w nim kilka błędów.

Funkcjonalności:
- Administrator
  - Zarządzanie filmami, seansami i miejscami seansu.
  - Podgląd i zarządzanie biletami, miejscami parkingowymi i użytkownikami.
  - Główny administrator ma dodatkowo możliwość zarządzania innymi administratorami.
- Użytkownik
  - Przegląd filmów, seansów i miejsc seansu.
  - Wybór miejsca parkingowego i zakup biletu.
  - Rezygnacja z biletu ze zwrotem pieniędzy.
  - Zakup biletów wyłącznie po zalogowaniu.
  - Symulacja płatności elektronicznej (okno płatności, brak realnej integracji).
  - Bilety generowane są z kodem QR zawierającym dane identyfikacyjne użytkownika.
 
Technologie:
- Backend: Python 3.11; Django 5.2.6; JavaScript; 
- Frontend: HTML, CSS (prosty układ stron i przyciski)
- Baza danych: MySQL
- Środowisko programistyczne: PyCharm 2025.2.2(z licencją)
- Generator kodów QR: Django QR Code (https://pypi.org/project/django-qr-code)

Pierwsza wersja: https://github.com/MatemXVI/kino_samochodowe

Opis interfejsu graficznego: https://github.com/MatemXVI/kino-samochodowe-laravel/blob/main/Interfejs%20graficzny.pdf

W projekcie skupiałem się głównie na backendzie, frontend jest głównie w celu pokazania układu pól, przycisków, zdjęć itd.
Aplikacja będzie dalej rozwijana, planowane jest dodanie możliwości pobrania biletu w PDF i formacie graficznym JPG/PNG. Planowane też jest przerobienie interfejsu graficznego.
