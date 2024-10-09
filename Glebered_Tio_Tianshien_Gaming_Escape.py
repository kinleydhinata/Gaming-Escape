import pygame
import random
import time
import math
import sys
import os

# Function to locate bundled assets
def resource_path(relative_path):
    """ Get the absolute path to resource, works for PyInstaller and during development """
    try:
        # PyInstaller stores data in a temp folder called _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # In development, it uses the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600  # Screen size
FPS = 60

# Colors
DARK_ROOM = (30, 30, 30)  # Darker room color
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
BROWN = (139, 69, 19)
GREY = (169, 169, 169)
LIGHT_GREY = (211, 211, 211)
DARK_GREY = (90, 90, 90)
SKIN = (255, 224, 189)
DARK_BLUE = (0, 0, 128)
NEON_GREEN = (57, 255, 20)
WHITE = (255, 255, 255)
WOOD = (160, 82, 45)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Glebered Tio Tianshien's Gaming Escape")

# Load sound effects using the resource_path function
try:
    background_music = pygame.mixer.Sound(resource_path('background_music.wav'))
    caught_sound = pygame.mixer.Sound(resource_path('caught.wav'))
    warning_sound = pygame.mixer.Sound(resource_path('warning.wav'))
except pygame.error as e:
    print(f"Error loading sound: {e}")
    background_music = None
    caught_sound = None
    warning_sound = None

# Fonts
font = pygame.font.SysFont('arial', 36)
title_font = pygame.font.SysFont('arial', 48, bold=True)

# Game variables
gamer_playing = False
game_over = False
score = 0
gaming_time = 0  # Track the actual time spent gaming
enemy_timer = 0
enemy_interval = random.randint(5, 10) * FPS  # Random time for the enemy to appear
caught = False
enemy_present = False
enemy_type = None
restart = False
in_main_menu = True
in_settings = False
caught_time = 0  # Time when the player is caught
show_caught = False  # Flag to show caught message

# Settings
music_volume = 0.5
sound_volume = 0.5
difficulty = 1  # 1 for easy, 2 for medium, 3 for hard

# Enemy wait time per difficulty
enemy_display_times = {1: 180, 2: 120, 3: 60}  # Adjusted for difficulty levels
enemy_display_time = enemy_display_times[difficulty]

# Positions
gamer_x, gamer_y = 150, 300
door_x, door_y = WIDTH - 200, HEIGHT - 300

# Start background music
if background_music:
    background_music.set_volume(music_volume)
    pygame.mixer.Sound.play(background_music, loops=-1)

# Draw Text
def draw_text(text, x, y, color, font_type=font):
    label = font_type.render(text, True, color)
    screen.blit(label, (x, y))

# Main menu screen
def main_menu():
    screen.fill(DARK_ROOM)
    title_label = title_font.render("Glebered Tio Tianshien's Gaming Escape", True, YELLOW)
    settings_label = font.render("Press 'S' for Settings", True, WHITE)
    start_label = font.render("Press 'Enter' to Start", True, WHITE)

    screen.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 2 - 150))
    screen.blit(settings_label, (WIDTH // 2 - settings_label.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_label, (WIDTH // 2 - start_label.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# Settings menu
def settings_menu():
    screen.fill(DARK_ROOM)
    draw_text("Settings", WIDTH // 2 - 80, HEIGHT // 2 - 200, YELLOW, title_font)
    draw_text(f"1. Music Volume: {int(music_volume * 100)}% (Use Up/Down)", WIDTH // 2 - 200,
              HEIGHT // 2 - 100, WHITE)
    draw_text(f"2. Sound Volume: {int(sound_volume * 100)}% (Use Left/Right)", WIDTH // 2 - 200,
              HEIGHT // 2 - 50, WHITE)
    draw_text(f"3. Difficulty: {['Easy', 'Medium', 'Hard'][difficulty - 1]} (Press 'D' to change)", WIDTH // 2 - 200,
              HEIGHT // 2, WHITE)
    draw_text("Press 'B' to go back", WIDTH // 2 - 100, HEIGHT // 2 + 100, WHITE)
    pygame.display.flip()

# Game over screen with restart
def game_over_screen():
    screen.fill(DARK_ROOM)
    draw_text("Game Over!", WIDTH // 2 - 150, HEIGHT // 2 - 100, YELLOW, title_font)
    draw_text(f"Your Score: {round(gaming_time, 1)} seconds", WIDTH // 2 - 150, HEIGHT // 2, YELLOW)
    draw_text("Press 'R' to Restart", WIDTH // 2 - 150, HEIGHT // 2 + 50, YELLOW)
    pygame.display.flip()

# Function to restart the game
def reset_game():
    global game_over, score, start_time, enemy_timer, caught, gamer_playing, enemy_present, gaming_time, enemy_display_time, show_caught, caught_time
    game_over = False
    score = 0
    gaming_time = 0
    enemy_timer = 0
    caught = False
    gamer_playing = False
    enemy_present = False
    enemy_display_time = enemy_display_times[difficulty]
    show_caught = False
    caught_time = 0
    start_time = time.time()

# Draw Glebered (the player)
def draw_glebered():
    # Glebered Body
    pygame.draw.rect(screen, BLUE, (gamer_x, gamer_y, 60, 100))  # Body with width increased

    # Head
    pygame.draw.circle(screen, SKIN, (gamer_x + 30, gamer_y - 30), 30)  # Larger head

    # Hair
    pygame.draw.ellipse(screen, BLACK, (gamer_x + 10, gamer_y - 60, 40, 30))  # Hair

    # Face
    pygame.draw.circle(screen, BLACK, (gamer_x + 20, gamer_y - 35), 5)  # Left eye
    pygame.draw.circle(screen, BLACK, (gamer_x + 40, gamer_y - 35), 5)  # Right eye

    # Smiling or neutral expression based on playing status
    if gamer_playing:
        pygame.draw.arc(screen, BLACK, (gamer_x + 15, gamer_y - 25, 30, 20), 3.14, 0, 2)  # Smile
    else:
        pygame.draw.line(screen, BLACK, (gamer_x + 15, gamer_y - 15), (gamer_x + 45, gamer_y - 15), 2)  # Neutral face

    # Arms (leaning towards keyboard)
    pygame.draw.line(screen, SKIN, (gamer_x + 10, gamer_y + 50), (gamer_x - 30, gamer_y + 80), 8)  # Left arm
    pygame.draw.line(screen, SKIN, (gamer_x + 50, gamer_y + 50), (gamer_x + 90, gamer_y + 80), 8)  # Right arm

    # Legs (extended forward)
    pygame.draw.line(screen, BLUE, (gamer_x + 15, gamer_y + 100), (gamer_x - 10, gamer_y + 150), 8)  # Left leg
    pygame.draw.line(screen, BLUE, (gamer_x + 45, gamer_y + 100), (gamer_x + 70, gamer_y + 150), 8)  # Right leg

    # Shoes
    pygame.draw.circle(screen, BLACK, (gamer_x - 10, gamer_y + 150), 10)  # Left shoe
    pygame.draw.circle(screen, BLACK, (gamer_x + 70, gamer_y + 150), 10)  # Right shoe

    # Name tag for fun
    draw_text("Glebered", gamer_x - 20, gamer_y + 160, YELLOW)

# Draw the room (door, window, etc.)
def draw_room():
    # Background wall
    screen.fill(DARK_ROOM)

    # Floor
    pygame.draw.rect(screen, WOOD, (0, HEIGHT - 150, WIDTH, 150))

    # Door
    pygame.draw.rect(screen, BROWN, (door_x, door_y, 120, 250))  # Larger door
    pygame.draw.rect(screen, BLACK, (door_x + 90, door_y + 110, 10, 30))  # Door handle

    # Window
    pygame.draw.rect(screen, LIGHT_GREY, (WIDTH // 2 - 150, 50, 300, 200))
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 150, 50, 300, 200), 5)  # Window frame
    pygame.draw.line(screen, BLACK, (WIDTH // 2 - 150, 150), (WIDTH // 2 + 150, 150), 5)  # Horizontal divider
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 50), (WIDTH // 2, 250), 5)  # Vertical divider

    # Rug
    pygame.draw.ellipse(screen, RED, (gamer_x - 50, gamer_y + 120, 200, 80))

# Draw the computer
def draw_computer():
    # Desk
    pygame.draw.rect(screen, BROWN, (gamer_x + 50, gamer_y + 30, 200, 20))  # Desk surface
    pygame.draw.rect(screen, BROWN, (gamer_x + 50, gamer_y + 50, 10, 100))  # Left leg
    pygame.draw.rect(screen, BROWN, (gamer_x + 240, gamer_y + 50, 10, 100))  # Right leg

    # Monitor
    pygame.draw.rect(screen, BLACK, (gamer_x + 80, gamer_y - 100, 140, 90))  # Monitor frame
    pygame.draw.rect(screen, LIGHT_GREY, (gamer_x + 85, gamer_y - 95, 130, 80))  # Screen

    if gamer_playing:
        draw_text("GAME", gamer_x + 110, gamer_y - 70, NEON_GREEN)
    else:
        draw_text("STUDY", gamer_x + 100, gamer_y - 70, YELLOW)

    # Monitor stand
    pygame.draw.rect(screen, BLACK, (gamer_x + 140, gamer_y - 10, 20, 40))

    # Keyboard
    pygame.draw.rect(screen, BLACK, (gamer_x + 80, gamer_y + 40, 140, 20))  # Keyboard
    pygame.draw.rect(screen, GREY, (gamer_x + 85, gamer_y + 45, 130, 10))  # Keys area

    # Mouse
    pygame.draw.ellipse(screen, BLACK, (gamer_x + 230, gamer_y + 45, 20, 30))
    pygame.draw.line(screen, LIGHT_GREY, (gamer_x + 240, gamer_y + 60), (gamer_x + 250, gamer_y + 70), 2)  # Mouse cord

    # PC Tower under the desk
    pygame.draw.rect(screen, BLACK, (gamer_x + 260, gamer_y + 50, 50, 100))  # PC Tower

    # Power button
    pygame.draw.circle(screen, RED, (gamer_x + 285, gamer_y + 60), 5)  # Red power button

    # USB ports
    for i in range(3):
        pygame.draw.rect(screen, LIGHT_GREY, (gamer_x + 265, gamer_y + 70 + i * 10, 20, 5))

    # Front fan with glowing effect
    pygame.draw.circle(screen, LIGHT_GREY, (gamer_x + 285, gamer_y + 130), 15)  # Fan outer circle
    pygame.draw.circle(screen, NEON_GREEN, (gamer_x + 285, gamer_y + 130), 12)  # Glowing fan blades
    for angle in range(0, 360, 45):
        x_offset = 10 * math.cos(math.radians(angle))
        y_offset = 10 * math.sin(math.radians(angle))
        pygame.draw.line(screen, BLACK, (gamer_x + 285, gamer_y + 130),
                         (gamer_x + 285 + x_offset, gamer_y + 130 + y_offset), 2)

    # Ventilation slots
    for i in range(5):
        pygame.draw.line(screen, DARK_GREY, (gamer_x + 265, gamer_y + 160 + i * 5),
                         (gamer_x + 305, gamer_y + 160 + i * 5), 2)

# Draw mom character
def draw_mom():
    # Dress
    pygame.draw.rect(screen, RED, (door_x + 30, door_y + 130, 60, 120))

    # Head
    pygame.draw.circle(screen, SKIN, (door_x + 60, door_y + 90), 30)

    # Hair (black)
    pygame.draw.ellipse(screen, BLACK, (door_x + 30, door_y + 60, 60, 40))

    # Eyes
    pygame.draw.circle(screen, BLACK, (door_x + 50, door_y + 80), 5)
    pygame.draw.circle(screen, BLACK, (door_x + 70, door_y + 80), 5)

    # Mouth
    pygame.draw.arc(screen, BLACK, (door_x + 45, door_y + 90, 30, 20), 0, 3.14, 2)

    # Arms
    pygame.draw.line(screen, SKIN, (door_x + 30, door_y + 150), (door_x - 20, door_y + 200), 8)
    pygame.draw.line(screen, SKIN, (door_x + 90, door_y + 150), (door_x + 140, door_y + 200), 8)

    # Legs
    pygame.draw.line(screen, RED, (door_x + 45, door_y + 250), (door_x + 45, door_y + 300), 10)
    pygame.draw.line(screen, RED, (door_x + 75, door_y + 250), (door_x + 75, door_y + 300), 10)

    # Shoes
    pygame.draw.circle(screen, BLACK, (door_x + 45, door_y + 300), 10)
    pygame.draw.circle(screen, BLACK, (door_x + 75, door_y + 300), 10)

# Draw police character without hat
def draw_police():
    # Body
    pygame.draw.rect(screen, DARK_BLUE, (door_x + 30, door_y + 130, 60, 120))

    # Head
    pygame.draw.circle(screen, SKIN, (door_x + 60, door_y + 90), 30)

    # Hair (short black hair)
    pygame.draw.ellipse(screen, BLACK, (door_x + 40, door_y + 60, 40, 30))

    # Eyes
    pygame.draw.circle(screen, BLACK, (door_x + 50, door_y + 80), 5)
    pygame.draw.circle(screen, BLACK, (door_x + 70, door_y + 80), 5)

    # Mouth
    pygame.draw.line(screen, BLACK, (door_x + 50, door_y + 95), (door_x + 70, door_y + 95), 2)

    # Arms
    pygame.draw.line(screen, SKIN, (door_x + 30, door_y + 150), (door_x - 20, door_y + 200), 8)
    pygame.draw.line(screen, SKIN, (door_x + 90, door_y + 150), (door_x + 140, door_y + 200), 8)

    # Badge
    pygame.draw.polygon(screen, YELLOW, [(door_x + 80, door_y + 140), (door_x + 90, door_y + 150),
                                         (door_x + 80, door_y + 160), (door_x + 70, door_y + 150)])

    # Legs
    pygame.draw.line(screen, DARK_BLUE, (door_x + 45, door_y + 250), (door_x + 45, door_y + 300), 10)
    pygame.draw.line(screen, DARK_BLUE, (door_x + 75, door_y + 250), (door_x + 75, door_y + 300), 10)

    # Shoes
    pygame.draw.circle(screen, BLACK, (door_x + 45, door_y + 300), 10)
    pygame.draw.circle(screen, BLACK, (door_x + 75, door_y + 300), 10)

# Main game loop
clock = pygame.time.Clock()
start_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if in_main_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    in_main_menu = False
                elif event.key == pygame.K_s:
                    in_settings = True
                    in_main_menu = False
        elif in_settings:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    in_settings = False
                    in_main_menu = True
                elif event.key == pygame.K_UP:
                    music_volume = min(1.0, music_volume + 0.1)
                    if background_music:
                        background_music.set_volume(music_volume)
                elif event.key == pygame.K_DOWN:
                    music_volume = max(0.0, music_volume - 0.1)
                    if background_music:
                        background_music.set_volume(music_volume)
                elif event.key == pygame.K_RIGHT:
                    sound_volume = min(1.0, sound_volume + 0.1)
                elif event.key == pygame.K_LEFT:
                    sound_volume = max(0.0, sound_volume - 0.1)
                elif event.key == pygame.K_d:
                    difficulty = (difficulty % 3) + 1
                    enemy_display_time = enemy_display_times[difficulty]
        elif game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Restart the game
                reset_game()
                in_main_menu = True

    if in_main_menu:
        main_menu()
    elif in_settings:
        settings_menu()
    else:
        # Only run the game logic if not game over
        if not game_over or show_caught:
            # Get key states
            keys = pygame.key.get_pressed()

            # Gamer plays when holding space
            if keys[pygame.K_SPACE]:
                gamer_playing = True
            else:
                gamer_playing = False

            # Update the gaming score only when Glebered is playing
            if gamer_playing and not game_over:
                gaming_time += clock.get_time() / 1000.0  # Convert milliseconds to seconds

            # Adjust enemy interval based on difficulty
            if difficulty == 1:
                enemy_interval = random.randint(6, 10) * FPS
            elif difficulty == 2:
                enemy_interval = random.randint(4, 8) * FPS
            elif difficulty == 3:
                enemy_interval = random.randint(2, 6) * FPS

            # Check for random enemy appearance (mom or police)
            if not enemy_present and not game_over:
                enemy_timer += 1
                if enemy_timer >= enemy_interval:
                    enemy_present = True
                    enemy_type = random.choice(["mom", "police"])
                    if warning_sound:
                        warning_sound.set_volume(sound_volume)
                        pygame.mixer.Sound.play(warning_sound)  # Play warning sound

            # Fill background and draw room
            draw_room()

            # Draw the computer and player (Glebered)
            draw_computer()
            draw_glebered()

            # If the enemy is present, show them for a limited time
            if enemy_present:
                if enemy_type == "mom":
                    draw_mom()
                else:
                    draw_police()

                # Check if player is playing while the enemy is present
                if gamer_playing and not game_over:
                    game_over = True  # Player is caught while playing
                    show_caught = True
                    caught_time = pygame.time.get_ticks()
                    if caught_sound:
                        caught_sound.set_volume(sound_volume)
                        pygame.mixer.Sound.play(caught_sound)  # Play caught sound

                enemy_display_time -= 1
                if enemy_display_time <= 0:
                    enemy_present = False
                    enemy_timer = 0
                    enemy_display_time = enemy_display_times[difficulty]  # Reset for next encounter

            # If player is caught, show caught message for 2 seconds before game over screen
            if show_caught:
                draw_text("You have been caught!", WIDTH // 2 - 150, HEIGHT // 2 - 50, RED, title_font)
                if pygame.time.get_ticks() - caught_time >= 2000:
                    show_caught = False

            # Draw the current gaming time
            draw_text(f"Score: {round(gaming_time, 1)} seconds", 10, 10, YELLOW)

            # Update screen
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)
        else:
            game_over_screen()  # Show game over screen
