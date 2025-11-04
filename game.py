import pygame
import random
import time
import csv

pygame.init()

# Window setup
WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SWSURFACE)
pygame.display.set_caption("Flanker Task")

FONT = pygame.font.Font(None, 120)
TEXT = pygame.font.Font(None, 40)

# MODULE 1 (Letters)
letter_targets = ["A", "B"]
letter_neutral = "X"

# MODULE 2 (Shapes)
shape_targets = ["★", "●"]
shape_neutral = "◇"

# Key mapping for response
# LEFT = choose first target, RIGHT = choose second target
key_map = {pygame.K_LEFT: 0, pygame.K_RIGHT: 1}

def draw_text(surface, text, font, color, x, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    surface.blit(render, rect)

def ask_user_info():
    name = input("Enter participant name: ")
    age = input("Enter participant age: ")
    return name, age

def run_task(targets, neutral, trials=2, attention_prob=0.2):
    results = []

    for _ in range(trials):
        # RANDOMLY DECIDE IF THIS TRIAL IS AN ATTENTION CHECK
        attention_trial = (random.random() < attention_prob)

        if attention_trial:
            # ---- ATTENTION CHECK TRIAL ----
            win.fill((255,255,255))
            dot_x, dot_y = random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)
            pygame.draw.circle(win, (255,0,0), (dot_x, dot_y), 20)
            pygame.display.update()

            start_time = time.time()
            clicked = False
            rt = None

            while time.time() - start_time < 3:  # 3 second window
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if (mx - dot_x)**2 + (my - dot_y)**2 <= 20**2:
                            clicked = True
                            rt = time.time() - start_time
                            break

            results.append(["ATTENTION_CHECK", "", clicked, clicked, rt])
            time.sleep(0.4)
            continue  # skip normal flanker logic, go to next trial

        # ---- NORMAL FLANKER TRIAL ----
        target_index = random.choice([0, 1])
        target = targets[target_index]

        condition = random.choice(["congruent", "incongruent", "neutral"])

        if condition == "congruent":
            flanker = target
        elif condition == "incongruent":
            flanker = targets[1 - target_index]
        else:
            flanker = neutral
        
        row = f"{flanker}   {flanker}   {target}   {flanker}   {flanker}"

        # Display stimulus for 3 seconds
        win.fill((255,255,255))
        draw_text(win, row, FONT, (0,0,0), WIDTH//2, HEIGHT//2)
        pygame.display.update()
        time.sleep(3)

        # Ask question
        win.fill((255,255,255))
        draw_text(win, "Which was in the middle?", TEXT, (0,0,0), WIDTH//2, HEIGHT//2 - 50)
        draw_text(win, f"LEFT = {targets[0]}    RIGHT = {targets[1]}", TEXT, (0,0,0), WIDTH//2, HEIGHT//2 + 50)
        pygame.display.update()

        start_time = time.time()
        response = None
        rt = None

        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        response = key_map[event.key]
                        rt = time.time() - start_time

        correct = (response == target_index)
        results.append([target, condition, targets[response], correct, rt])
        time.sleep(0.4)

    return results


# ---------------- MAIN PROGRAM ---------------- #

name, age = ask_user_info()

instruction = True
while instruction:
    win.fill((255,255,255))
    draw_text(win, "Flanker Task", TEXT, (0,0,0), WIDTH//2, HEIGHT//2 - 60)
    draw_text(win, "Press SPACE to begin", TEXT, (0,0,0), WIDTH//2, HEIGHT//2 + 20)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            instruction = False

# Run Module 1 (Letters)
results1 = run_task(letter_targets, letter_neutral, trials=10)

# Run Module 2 (Shapes)
results2 = run_task(shape_targets, shape_neutral, trials=10)

# Save combined results
save_results(name, age, results1 + results2)

end_screen()
