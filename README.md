## Czym jest projekt i dlaczego powstał?
Program odczytuje obecnie grany utwór na spotify, a następnie wysyła informacje do arduino.
## Jak program działa?
Program napisany był na podstawie tutorialu na youtube którego nie mogę znaleźć. W dużym skrócie: 
### 
1. Program loguje się w przeglądarce do spotify.
2. Pobiera klucz który ma ważność działania około godziny.
3. Używając klucza pobiera informacje o obecnie granym utworze.
4. Informacja ta wysyłana jest do arduino poprzez port szeregowy.
###
Wszystko uruchamiane jest poprzez lokalny serwer postawiony na flasku. ID użytkownika, secret użytkownika i aplikacji pobierane są ze zmiennych lokalnych.
## Problemy
Program testowałem tylko na swojej maszynie, nie wiem jak będzie działać na innych komputerach. Program wysypuje się w przypadku spauzowania utworu na dłuższy czas, co jest najprawdopodobniej związane z tym jak działa API spotify.
## Wsparcie i plany na przyszlość
Projekt jest ukończony, jeśli wystąpią jakieś błędy, postaram się je naprawić.
