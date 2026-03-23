from games.catcher.game import SCREEN_WIDTH

# Documentatie van het Framework
Hieronder vind je een overzicht van de belangrijkste functies en variabelen die het UHack-a-Py framework biedt. Deze functies zijn ontworpen om het maken van games eenvoudiger te maken, zodatje je kunt concentreren op het creatieve aspect van gameontwikkeling zonder je zorgen te maken over de technische details van PyGame.

## Inhoud
- [Hoofdfuncties](#hoofdfuncties)
  - [```playing()```](#playing)
- [Invoer](#invoer)
  - [```input(key)```](#inputkey)
  - [```input_once(key)```](#input_oncekey)
  - [```mouse_position()```](#mouse_position)
  - [```input_mouse(button)```](#input_mousebutton)
- [Tekenen](#tekenen)
  - [```rectangle(x, y, width, height, color)```](#rectanglex-y-width-height-color)
  - [```circle(x, y, radius, color)```](#circlex-y-width-height-color)
  - [```image(image_name, x, y, w, h, transforms=[])```](#imageimage_name-x-y-w-h-transforms)
  - [```text(x, y, content, color, size=30, align="topleft")```](#textx-y-content-color-size30-aligntopleft)
- [Interactie](#interactie)
  - [```colide(object1, object2)```](#colideobject1-object2)
- [Overige functies](#overige-functies)
  - [```out_of_screen(x, y)```](#out_of_screenx-y)
- [Globale variabelen](#globale-variabelen)
  - [```SCREEN_WIDTH```](#screen_width)
  - [```SCREEN_HEIGHT```](#screen_height)

## Hoofdfuncties
### ```playing()```
Deze functie controleert of het spel nog steeds actief is. Je game loop blijft draaien zolang deze functie `True` retourneert. Zodra de speler op de 'escape'-toets drukt, zal deze functie `False` retourneren en zal de game loop worden beëindigd. Dit zal ook automatisch alles regelen rond het tekenen van het scherm.

> [!WARNING]
> Zorg dus ook dat alle tekenopdrachten binnen deze loop worden uitgevoerd, anders zal je ze niet kunnen zien.

> Voorbeeld van gebruik:
> ```python
> while playing():
>     # Hier komt de code van je game loop
> ```

---

## Invoer
### ```input(key)```
Deze functie controleert of een specifieke toets is ingedrukt. Je kunt deze functie gebruiken om te reageren op gebruikersinvoer, zoals beweging of acties in je game.

Parameters:
- `key`: De naam van de toets die je wilt controleren. Gebruik de [lijst van PyGame-toetsen](https://www.pygame.org/docs/ref/key.html) voor de juiste namen (bijvoorbeeld `K_UP`, `K_DOWN`, `K_LEFT`, `K_RIGHT`, etc.).

> Voorbeeld van gebruik:
> ```python
> if input('K_UP'):
>     # Code om de speler omhoog te laten bewegen
> ```

---

### ```input_once(key)```
Deze functie werkt vergelijkbaar met `input(key)`, maar retourneert `True` alleen op het moment dat de toets voor het eerst wordt ingedrukt. Dit is handig voor acties die slechts één keer moeten worden uitgevoerd, zoals springen of schieten.

Parameters:
- `key`: De naam van de toets die je wilt controleren. Gebruik de [lijst van PyGame-toetsen](https://www.pygame.org/docs/ref/key.html) voor de juiste namen (bijvoorbeeld `K_UP`, `K_DOWN`, `K_LEFT`, `K_RIGHT`, etc.).

> Voorbeeld van gebruik:
> ```python
> if input_once('K_SPACE'):
>     # Code om de speler te laten springen
> ```

---

### ```mouse_position()```
Deze functie geeft de huidige positie van de muis terug als een `Vector`.

> Voorbeeld van gebruik:
> ```python
> muis_positie = mouse_position()
> print(f"Muis positie: {muis_positie.x}, {muis_positie.y}")
> ```

---

### ```input_mouse(button)```
Deze functie controleert of een specifieke muisknop is ingedrukt.

Parameters:
- `button`: De knop die je wilt controleren (0 = links, 1 = midden, 2 = rechts).

> Voorbeeld van gebruik:
> ```python
> if input_mouse(0):
>     # Code om te reageren op een linkermuisknopklik
> ```

---

## Tekenen
### ```rectangle(x, y, width, height, color)```
Deze functie tekent een rechthoek op het scherm. Je kunt deze gebruiken om eenvoudige vormen te tekenen, zoals platforms, muren of andere objecten in je game.

Parameters:
- `x`: De x-coördinaat van de linkerbovenhoek van de rechthoek.
- `y`: De y-coördinaat van de linkerbovenhoek van de rechthoek.
- `width`: De breedte van de rechthoek.
- `height`: De hoogte van de rechthoek.
- `color`: De kleur van de rechthoek, opgegeven als een tuple van RGB-waarden (bijvoorbeeld `(255, 0, 0)` voor rood). Het framework voorziet een aantal [standaard kleuren](games/framework/colors.py), die kan je gebruiken door `colors.RED` te gebruiken in plaats van een RGB-tuple.

> Voorbeeld van gebruik:
> ```python
> rectangle(50, 50, 100, 200, colors.BLUE)  # Tekent een blauwe rechthoek
> ```

---

### ```circle(x, y, radius, color)```
Deze functie tekent een cirkel op het scherm. Je kunt deze gebruiken om ronde objecten te tekenen, zoals ballen of planeten.

Parameters:
- `x`: De x-coördinaat van het midden van de cirkel.
- `y`: De y-coördinaat van het midden van de cirkel.
- `radius`: De straal van de cirkel.
- `color`: De kleur van de cirkel, opgegeven als een tuple van RGB-waarden (bijvoorbeeld `(255, 0, 0)` voor rood). Het framework voorziet een aantal [standaard kleuren](games/framework/colors.py), die kan je gebruiken door `colors.RED` te gebruiken in plaats van een RGB-tuple.

> Voorbeeld van gebruik:
> ```python
> circle(200, 200, 50, colors.GREEN)  # Tekent een groene cirkel
> ```

---

### ```image(image_name, x, y, w, h, transforms=[])```
Deze functie tekent een afbeelding op het scherm. Je kunt deze gebruiken om sprites, achtergronden of andere grafische elementen in je game te plaatsen.

Parameters:
- `image_name`: De naam van de afbeelding die je wilt tekenen. Zorg ervoor dat de afbeelding zich in de juiste map bevindt, de `images` folder binnen je project.
- `x`: De x-coördinaat van de linkerbovenhoek van de afbeelding.
- `y`: De y-coördinaat van de linkerbovenhoek van de afbeelding.
- `w`: De breedte van de afbeelding zoals deze op het scherm moet worden weergegeven.
- `h`: De hoogte van de afbeelding zoals deze op het scherm moet worden weergegeven.
- `transforms`: Een optionele lijst van transformaties die op de afbeelding moeten worden toegepast. Mogelijke transformaties zijn:
  - `HORIZONTAL_FLIP`: Draait de afbeelding horizontaal om.
  - `VERTICAL_FLIP`: Draait de afbeelding verticaal om.

> Voorbeeld van gebruik:
> ```python
> image('player.png', 100, 150, 50, 50)  # Tekent de afbeelding 'player.png' op positie (100, 150) met een breedte en hoogte van 50 pixels
> image('enemy.png', 200, 150, 50, 50, ['HORIZONTAL_FLIP'])  # Tekent de afbeelding 'enemy.png' horizontaal gespiegeld
> ```

---

### ```text(x, y, content, color, size=30, align="topleft")```
Deze functie tekent tekst op het scherm. Je kunt deze gebruiken om scores, instructies of andere informatie aan de speler weer te geven.

Parameters:
- `x`: De x-coördinaat van de positie waar de tekst moet worden weergegeven.
- `y`: De y-coördinaat van de positie waar de tekst moet worden weergegeven.
- `content`: De tekstinhoud die je wilt weergeven.
- `color`: De kleur van de tekst, opgegeven als een tuple van RGB-waarden (bijvoorbeeld `(255, 0, 0)` voor rood). Het framework voorziet een aantal [standaard kleuren](games/framework/colors.py), die kan je gebruiken door `colors.RED` te gebruiken in plaats van een RGB-tuple.
- `size`: De grootte van de tekst (standaard is 30).
- `align`: De uitlijning van de tekst. Mogelijke waarden zijn: 
    ```
    topleft, midtop, topright,
    midleft, center, midright,
    bottomleft, midbottom, bottomright
    ```

> Voorbeeld van gebruik:
> ```python
> text(50, 50, "Score: 100", colors.WHITE)  # Tekent de tekst "Score: 100" in wit op positie (50, 50)
> text(400, 300, "Game Over", colors.RED, size=50, align="center")  # Tekent de tekst "Game Over" in rood, gecentreerd op positie (400, 300) met een grootte van 50
> ```

---

## Interactie
### ```colide(object1, object2)```
Deze functie controleert of twee objecten met elkaar botsen. Je kunt deze gebruiken om interacties tussen objecten in je game te detecteren, zoals het raken van een vijand of het oppakken van een item.
Parameters:
- `object1`: Het eerste object dat je wilt controleren. Dit kan een rechthoek, cirkel, afbeelding of `Vector` zijn.
- `object2`: Het tweede object dat je wilt controleren.

> Voorbeeld van gebruik:
> ```python
> player = rectangle(50, 50, 50, 50, colors.BLUE)  # Een rechthoek die de speler vertegenwoordigt
> enemy = rectangle(100, 50, 50, 50, colors.RED)  # Een rechthoek die een vijand vertegenwoordigt
> 
> if colide(player, enemy):
>     # Code om te reageren op de botsing, bijvoorbeeld het verminderen van de gezondheid van de speler
> ```

---

## Overige functies
### ```out_of_screen(x, y)```
Deze functie controleert of een gegeven positie zich buiten het scherm bevindt. Je kunt deze gebruiken om te voorkomen dat objecten buiten de zichtbare speelruimte bewegen.

Parameters:
- `x`: De x-coördinaat van de positie die je wilt controleren.
- `y`: De y-coördinaat van de positie die je wilt controleren.

> Voorbeeld van gebruik:
> ```python
> player_x = 50
> player_y = 50
> 
> if not out_of_screen(player_x, player_y):
>     # Code om de speler te laten bewegen, bijvoorbeeld naar rechts
>     player_x += 5
> ```

---

## Globale variabelen
### ```SCREEN_WIDTH```
Deze variabele geeft de breedte van het spelvenster aan. Je kunt deze gebruiken om de positie van objecten te berekenen of om te controleren of objecten zich binnen het scherm bevinden.
> Voorbeeld van gebruik:
> ```python
> player_x = SCREEN_WIDTH - player_width  # Plaatst de speler aan de rechterkant van het scherm
> ```

---

### ```SCREEN_HEIGHT```
Deze variabele geeft de hoogte van het spelvenster aan. Je kunt deze gebruiken om de positie van objecten te berekenen of om te controleren of objecten zich binnen het scherm bevinden. 
> Voorbeeld van gebruik:
> ```python
> player_y = SCREEN_HEIGHT - player_height  # Plaatst de speler aan de bovenkant van het scherm
> ```

---

