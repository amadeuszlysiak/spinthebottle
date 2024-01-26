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
