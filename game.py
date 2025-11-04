import pygame
import random
import time
import csv

pygame.init()

# Window setup
WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SWSURFACE)
pygame.display.set_caption("Cognitive Science Experiment")

FONT = pygame.font.Font(None, 120)
TEXT = pygame.font.Font(None, 38)

# --- MODULE DEFINITIONS ---

modules = [
    {
        "name": "Text-Based Module",
        "left_group": ["A", "B"],
        "right_group": ["C", "D"],
        "neutral": ["X", "Y"]
    },
    {
        "name": "Emoji Module",
        "left_group": ["🙂", "😁"],
        "right_group": ["🙁", "😞"],
        "neutral": ["😶", "😑"]
    },
    {
        "name": "Color-Shape Module",
        "left_group": ["🔴", "🟥"],
        "right_group": ["❤️", "♦️"],
        "neutral": ["🔻", "🛑"]
    },
    {
        "name": "Classic Shape Module",
        "left_group": ["★"],
        "right_group": ["●"],
        "neutral": ["◇"]
    }
]

key_map = {pygame.K_LEFT: 0, pygame.K_RIGHT: 1}

def draw_text(surface, text, font, color, x, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    surface.blit(render, rect)

def instruction_screen():
    instructions = [
        "Instruction Manual",
        "",
        "Thank you for participating.",
        "",
        "The game has 4 tasks. Each task has:",
        "1) Practice round (3 trials)",
        "2) Experiment round (10 trials)",
        "",
        "Randomly, a RED DOT will appear. Please CLICK it.",
        "",
        "TEXT TASK:",
        "If center is A/B -> Press LEFT    If C/D -> Press RIGHT",
        "",
        "EMOJI TASK:",
        "🙂😁 -> LEFT    🙁😞 -> RIGHT",
        "",
        "SHAPE TASK:",
        "🔴🟥 -> LEFT    ❤️♦️ -> RIGHT",
        "",
        "Press SPACE to begin..."
    ]

    win.fill((255,255,255))
    y = 50
    for line in instructions:
        draw_text(win, line, TEXT, (0,0,0), WIDTH//2, y)
        y += 32
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def module_header(name):
    win.fill((255,255,255))
    draw_text(win, name, TEXT, (0,0,0), WIDTH//2, HEIGHT//2)
    draw_text(win, "Press SPACE to continue", TEXT, (0,0,0), WIDTH//2, HEIGHT//2+60)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def show_mapping(left_group, right_group):
    win.fill((255,255,255))
    draw_text(win, "Key Mapping", TEXT, (0,0,0), WIDTH//2, HEIGHT//2 - 60)
    draw_text(win, f"LEFT ARROW = {left_group}", TEXT, (0,0,0), WIDTH//2, HEIGHT//2)
    draw_text(win, f"RIGHT ARROW = {right_group}", TEXT, (0,0,0), WIDTH//2, HEIGHT//2 + 60)
    draw_text(win, "Press SPACE to begin practice", TEXT, (0,0,0), WIDTH//2, HEIGHT//2+130)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def run_single_trial(left_group, right_group, neutral, record=False, results=None):
    # random attention check (~20%)
    if random.random() < 0.2:
        win.fill((255,255,255))
        x, y = random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)
        pygame.draw.circle(win, (255,0,0), (x, y), 18)
        pygame.display.update()

        start = time.time()
        clicked = False
        rt = None

        while time.time() - start < 3:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if (mx-x)**2 + (my-y)**2 <= 18**2:
                        clicked = True
                        rt = time.time() - start
                        break

        if record:
            results.append(["ATTENTION", "", clicked, clicked, rt])
        return

    # --- NORMAL TRIAL ---
    all_targets = left_group + right_group
    target = random.choice(all_targets)
    group_index = 0 if target in left_group else 1

    condition = random.choice(["congruent", "incongruent", "neutral"])

    if condition == "congruent":
        flanker = random.choice(left_group if group_index==0 else right_group)
    elif condition == "incongruent":
        flanker = random.choice(right_group if group_index==0 else left_group)
    else:
        flanker = random.choice(neutral)

    display = f"{flanker}   {target}   {flanker}"

    win.fill((255,255,255))
    draw_text(win, display, FONT, (0,0,0), WIDTH//2, HEIGHT//2)
    pygame.display.update()

    start = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                response = key_map[event.key]
                rt = time.time() - start
                correct = (response == group_index)
                if record:
                    results.append([target, condition, ("LEFT" if response==0 else "RIGHT"), correct, rt])
                return

def save_results(name, age, results):
    with open("experiment_results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, age])
        writer.writerow(["Target/Check","Condition","Response","Correct","RT"])
        writer.writerows(results)
        writer.writerow([])

def end_screen():
    win.fill((255,255,255))
    draw_text(win, "Experiment Complete. Thank You!", TEXT, (0,0,0), WIDTH//2, HEIGHT//2)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()

# ---------------- MAIN PROGRAM ---------------- #

name = input("Enter name: ")
age = input("Enter age: ")

instruction_screen()

all_results = []

for module in modules:
    module_header(module["name"])
    show_mapping(module["left_group"], module["right_group"])

    # Practice Trials (not recorded)
    for _ in range(3):
        run_single_trial(module["left_group"], module["right_group"], module["neutral"], record=False)

    # Transition
    win.fill((255,255,255))
    draw_text(win, "Practice Completed", TEXT, (0,0,0), WIDTH//2, HEIGHT//2 - 20)
    draw_text(win, "Experiment Begins Now", TEXT, (0,0,0), WIDTH//2, HEIGHT//2 + 40)
    pygame.display.update()
    time.sleep(2)

    # Experiment Trials (recorded)
    for _ in range(10):
        run_single_trial(module["left_group"], module["right_group"], module["neutral"], record=True, results=all_results)

save_results(name, age, all_results)
end_screen()
