import sys
import math
import pygame
import random
from colorama import Fore
from fuzzywuzzy import process
from typing import List
from typing import Tuple
from typing import Optional


# Funkcja obsługująca grę "pytanie czy wyzwanie"
def pytanie_czy_wyzwanie() -> None:
    # Zapytaj użytkownika czy wybiera pytanie czy wyzwanie
    query: str = input("Pytanie czy wyzwanie? ")
    # Sprawdź co użytkownik wybrał za pomocą fuzzywzuzzy
    pcw: str = process.extractOne(query, ['pytanie', 'wyzwanie'])[0]

    if 'pytanie' == pcw:
        # Obsłuż pytanie
        pytanie: str = input("Podaj pytanie: ")
        print(f"{Fore.RED}{pytanie}{Fore.RESET}")
        odpowiedź: str = input(f"Odpowiedz na pytanie: ")
        print(f"{Fore.BLUE}{odpowiedź}{Fore.RESET}")
    else:
        # Obsłuż wyzwanie
        wyzwanie: str = input("Podaj wyzwanie: ")
        print(f"{Fore.GREEN}{wyzwanie}{Fore.RESET}")


# Funkcja do obracania obiektu (butelki) w grze
def rotate(
        image: pygame.Surface,  # Obrazek butelki
        angle: float,           # Kąt, o który należy obrócić butelkę
        pivot: Tuple[int, int], # Punkt będący osią obrotu
        offset: pygame.Vector2  # Przemieszczenie butelki od osi obrotu (wektor [0,0])
) -> Tuple[pygame.Surface, pygame.Rect]: # Zwraca Surface oraz Rect obróconej butelki
    rotated_image: pygame.Surface = pygame.transform.rotozoom(image, -angle, 1)
    rotated_offset: pygame.Vector2 = offset.rotate(angle)
    rotated_rect: pygame.Rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rotated_rect

# Funkcja rysująca graczy wokół butelki
def draw_players(
        screen: pygame.Surface,     # Ekran
        width: int,                 # Szerokość ekranu
        height: int,                # Wysokość ekranu
        n_players: int,             # Ilość graczy
        player_names: List[str],    # Imiona graczy
        winning_player: int = None  # Gracz wylosowany przez butelkę
) -> None:
    angle_between_players: float = 360 / n_players  # Kąt między każdym z graczy
    radius: int = 300 # Promień koła, na którym znajdują się gracze
    for i in range(n_players):
        angle: float = math.radians(angle_between_players * i)  # Obliczenie miejsca, na którym powinien
        x: int = width // 2 + int(radius * math.cos(angle))     # znajdować się każdy z graczy na kole
        y: int = height // 2 + int(radius * math.sin(angle))

        if i == winning_player:
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 30) # Wyróżnienie wylosowanego gracza - czerwony
        else:
            pygame.draw.circle(screen, (0, 0, 255), (x, y), 20) # Zwykły gracz - niebieski

        font: pygame.font.Font = pygame.font.Font(None, 36) # number gracza
        number_text: pygame.Surface = font.render(str(i + 1), True, (0, 0, 0))
        number_text_rect: pygame.Rect = number_text.get_rect(center=(x, y))
        screen.blit(number_text, number_text_rect)

        name_text: pygame.Surface = font.render(player_names[i], True, (0, 0, 0)) # imię gracza
        name_text_rect: pygame.Rect = name_text.get_rect(center=(x, y - 40))
        screen.blit(name_text, name_text_rect)


# Funkcja obliczająca prędkość obrotu butelki
def calculate_speed(target_angle: float, current_angle: float) -> float:
    distance: float = target_angle - current_angle  # ile jeszcze zostało nam do końca obracania się
    if distance > 0:
        return max(0.5, distance / 20)
    return 0
    # Główna funkcja gry
def main() -> None:
    # Ustawienia początkowe gry
    width: int = 900
    height: int = 700
    screen: pygame.Surface = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Butelka')

    # Ładowanie i skalowanie obrazu butelki
    bottle_image: pygame.Surface = pygame.image.load('assets/bottle.png')
    bottle_image: pygame.Surface = pygame.transform.scale(bottle_image, (339, 407))
    bottle_rect: pygame.Rect = bottle_image.get_rect(center=(width // 2, height // 2))
    
    # Inicjalizacja zmiennych do kontroli obrotu butelki
    angle: float = 0
    speed: float = 0
    target_angle: int = 0
    spinning: bool = False
    winning_player: Optional[int] = None

    # Wczytanie liczby graczy i ich nazw
    n_players: int = int(input("How many players will be playing? "))

    player_names: List[str] = []
    for i in range(n_players):
        player_names.append(input(f"Enter your name player {i}: "))

    # Główna pętla gry
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Wyjście z okienka
                running: bool = False     # -> pygame.quit() i sys.exit()
            if event.type == pygame.KEYDOWN: # Jeżeli przyciśniesz jakiś klawisz to butla
                target_angle: int = random.randint(720, 1440) # zaczyna się kręcić o losowy kąt z przedziału
                speed: float = target_angle / 20 # Prędkość jest zależna od tego ile butla musi się przekręcić
                angle: float = 0 # licznik ile już się przekręciła
                spinning: bool = True

        if spinning:
            # Aktualizacja obrotu butelki
            speed: float = calculate_speed(target_angle, angle)
            angle += speed
            if target_angle - angle < 0.1: # koniec kręcenia
                angle: float = float(target_angle)
                spinning: bool = False
                normalized_angle: int = angle % 360 # wybór gracza
                winning_player: int = (int((normalized_angle // (360 / n_players)) % n_players) - 1) % n_players
                screen.fill((255, 255, 255)) # rysowanie ekranu, graczy i butelki
                draw_players(screen, width, height, n_players, player_names, winning_player)
                screen.blit(rotated_image, rotated_rect)
                pygame.display.flip()
                pytanie_czy_wyzwanie()

        rotated_image, rotated_rect = rotate(bottle_image, angle, bottle_rect.center, pygame.Vector2(0, 0))

        # Rysowanie stanu gry na ekranie
        screen.fill((255, 255, 255))
        draw_players(screen, width, height, n_players, player_names, winning_player)
        screen.blit(rotated_image, rotated_rect)
        pygame.display.flip()

        # Ustawienie liczby klatek na sekundę
        pygame.time.Clock().tick(60)


if _name_ == '_main_':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
