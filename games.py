import pygame
import random
import time
import csv
import os
from datetime import datetime

# -------------------- CONFIG --------------------
SCREEN_W, SCREEN_H = 1000, 600
BG_COLOR = (255, 255, 255)
TRIALS = 30
PRACTICE_TRIALS = 6

FIX_MS = 500        # fixation cross before each trial
STIM_MS = 1500      # time stimulus is visible (fixed)
ITI_MS = 400        # blank inter-trial interval

STIM_SIZE = 150
FPS = 60
FONT_SIZE = 48

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Cognitive Science Experiment")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)
small_font = pygame.font.Font(None, 28)

# -------------------- LOAD STIMULI --------------------
def load_images(folder, names):
    imgs = {}
    for name in names:
        path = os.path.join(folder, f"{name}.png")
        if not os.path.exists(path):
            print(f"⚠️ Missing image: {path}")
            continue
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (STIM_SIZE, STIM_SIZE))
        imgs[name] = img
    return imgs

emoji_imgs = load_images("emoticons", [
    "happy_1", "happy_2", "sad_1", "sad_2", "neutral_1", "neutral_2"
])
shape_imgs = load_images("shapes", [
    "square", "heart", "circle", "triangle", "star", "pentagon"
])

# -------------------- MODULE DEFINITIONS --------------------
modules = [
    {
        "name": "Letter Module",
        "type": "text",
        "left_group": ["A", "B"],
        "right_group": ["C", "D"],
        "neutral": ["X", "Y"]
    },
    {
        "name": "Emoji Module",
        "type": "image",
        "left_group": ["happy_1", "happy_2"],
        "right_group": ["sad_1", "sad_2"],
        "neutral": ["neutral_1", "neutral_2"],
        "img_dict": emoji_imgs
    },
    {
        "name": "Shape Module",
        "type": "image",
        "left_group": ["square", "pentagon"],
        "right_group": ["circle", "triangle"],
        "neutral": ["heart", "star"],
        "img_dict": shape_imgs
    },
    {
        "name": "Letter+Emoji Module",
        "type": "mixed",
        "left_group": ["happy_1", "happy_2"],
        "right_group": ["sad_1", "sad_2"],
        "neutral": ["neutral_1", "neutral_2"],
        "img_dict": emoji_imgs,
        "letters": ["H", "S", "X"]
    }
]

key_map = {pygame.K_LEFT: 0, pygame.K_RIGHT: 1}

# -------------------- DRAW FUNCTIONS --------------------
def draw_text_center(text, y, font_obj=font):
    render = font_obj.render(text, True, (0, 0, 0))
    rect = render.get_rect(center=(SCREEN_W // 2, y))
    screen.blit(render, rect)

def draw_image_center(img, img_dict, y=None, x=None):
    if y is None: y = SCREEN_H // 2
    if x is None: x = SCREEN_W // 2
    image = img_dict[img]
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)

def draw_mixed_triplet(center_img, flank_letter, img_dict):
    spacing = 200
    y = SCREEN_H // 2
    letter_font = pygame.font.Font(None, STIM_SIZE)
    left_text = letter_font.render(flank_letter, True, (0, 0, 0))
    right_text = letter_font.render(flank_letter, True, (0, 0, 0))
    rect_l = left_text.get_rect(center=(SCREEN_W // 2 - spacing, y))
    rect_r = right_text.get_rect(center=(SCREEN_W // 2 + spacing, y))
    rect_c = img_dict[center_img].get_rect(center=(SCREEN_W // 2, y))
    screen.blit(left_text, rect_l)
    screen.blit(img_dict[center_img], rect_c)
    screen.blit(right_text, rect_r)

def draw_small_image_centered(img_key, img_dict, x, y, size=80):
    img = pygame.transform.smoothscale(img_dict[img_key], (size, size))
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

# -------------------- INSTRUCTION SCREENS --------------------
def instruction_screen():
    lines = [
        "Thank you for consenting to participate in this Cognitive Science experiment.",
        "",
        "General Instructions:",
        "The game will consist of 4 tasks.",
        "Each task includes a short practice module followed by the main experiment.",
        "",
        "Please Note:",
        "At random times during your gameplay, a red dot will appear.",
        "Please CLICK on it to proceed.",
        "",
        "Press SPACE to begin."
    ]
    screen.fill(BG_COLOR)
    y = 80
    for line in lines:
        text = small_font.render(line, True, (0, 0, 0))
        rect = text.get_rect(center=(SCREEN_W // 2, y))
        screen.blit(text, rect)
        y += 35
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        clock.tick(FPS)

def module_instructions(module):
    screen.fill(BG_COLOR)
    instruction_font = pygame.font.Font(None, 28)

    def draw_small_text_center(text, y):
        render = instruction_font.render(text, True, (0, 0, 0))
        rect = render.get_rect(center=(SCREEN_W // 2, y))
        screen.blit(render, rect)

    bottom_y = SCREEN_H - 60

    if module["name"] == "Letter Module":
        draw_small_text_center("Text-based Task:", 100)
        draw_small_text_center("You will be shown three letters.", 150)
        draw_small_text_center("If the letter in the middle is A or B, press the < - key", 220)
        draw_small_text_center("If the letter in the middle is C or D, press the - > key", 260)
        bottom_y = 320

    elif module["name"] == "Emoji Module":
        draw_small_text_center("Emoji-based Task:", 100)
        draw_small_text_center("You will be shown three emojis.", 150)
        draw_small_text_center("If the emoji in the middle is:", 220)
        draw_small_image_centered("happy_1", emoji_imgs, SCREEN_W // 2 - 100, 280)
        draw_small_image_centered("happy_2", emoji_imgs, SCREEN_W // 2 + 100, 280)
        draw_small_text_center("Press the < - key", 340)
        draw_small_text_center("If the emoji in the middle is:", 420)
        draw_small_image_centered("sad_1", emoji_imgs, SCREEN_W // 2 - 100, 480)
        draw_small_image_centered("sad_2", emoji_imgs, SCREEN_W // 2 + 100, 480)
        draw_small_text_center("Press the - > key", 560)
        bottom_y = 610

    elif module["name"] == "Shape Module":
        draw_small_text_center("Shape-based Task:", 100)
        draw_small_text_center("You will be shown three shapes.", 150)
        draw_small_text_center("If the shape in the middle is:", 220)
        draw_small_image_centered("square", shape_imgs, SCREEN_W // 2 - 100, 280)
        draw_small_image_centered("pentagon", shape_imgs, SCREEN_W // 2 + 100, 280)
        draw_small_text_center("Press the < - key", 340)
        draw_small_text_center("If the shape in the middle is:", 420)
        draw_small_image_centered("circle", shape_imgs, SCREEN_W // 2 - 100, 480)
        draw_small_image_centered("triangle", shape_imgs, SCREEN_W // 2 + 100, 480)
        draw_small_text_center("Press the - > key", 560)
        bottom_y = 610

    elif module["name"] == "Letter+Emoji Module":
        draw_small_text_center("Emoji + Text-based Task:", 100)
        draw_small_text_center("You will be shown three characters.", 150)
        draw_small_text_center("Focus on the emoji in the middle.", 190)
        draw_small_text_center("If the emoji in the middle is:", 240)
        draw_small_image_centered("happy_1", emoji_imgs, SCREEN_W // 2 - 100, 300)
        draw_small_image_centered("happy_2", emoji_imgs, SCREEN_W // 2 + 100, 300)
        draw_small_text_center("Press the < - key", 360)
        draw_small_text_center("If the emoji in the middle is:", 440)
        draw_small_image_centered("sad_1", emoji_imgs, SCREEN_W // 2 - 100, 500)
        draw_small_image_centered("sad_2", emoji_imgs, SCREEN_W // 2 + 100, 500)
        draw_small_text_center("Press the - > key", 560)
        bottom_y = 610

    draw_small_text_center("Press SPACE to begin", bottom_y)
    pygame.display.flip()

    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                waiting = False
        clock.tick(FPS)

# -------------------- TRIAL FUNCTION --------------------
def run_trial(module, record=False, results=None, forced_condition=None):
    # ---------------- ATTENTION CHECK ----------------
    if forced_condition is None and random.random() < 0.05:
        screen.fill(BG_COLOR)
        x, y = random.randint(100, SCREEN_W - 100), random.randint(100, SCREEN_H - 100)
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 15)
        pygame.display.flip()
        start = time.time()
        clicked, rt = False, None
        while time.time() - start < 3:
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if (mx - x) ** 2 + (my - y) ** 2 <= 15 ** 2:
                        clicked, rt = True, time.time() - start
                        break
        if record and results is not None:
            results.append([module["name"], "ATTENTION", "", "", clicked, clicked, rt])
        return None, None  # <- safe tuple return

    # ---------------- SELECT TARGET AND CONDITION ----------------
    all_targets = module["left_group"] + module["right_group"]
    target = random.choice(all_targets)
    group_index = 0 if target in module["left_group"] else 1
    condition = forced_condition if forced_condition else random.choice(["congruent", "incongruent", "neutral"])

    if condition == "congruent":
        flanker = random.choice(module["left_group"] if group_index == 0 else module["right_group"])
    elif condition == "incongruent":
        flanker = random.choice(module["right_group"] if group_index == 0 else module["left_group"])
    else:
        flanker = random.choice(module["neutral"])

    # ---------------- DISPLAY STIMULI ----------------
    screen.fill(BG_COLOR)
    if module["type"] == "text":
        display = f"{flanker}   {target}   {flanker}"
        draw_text_center(display, SCREEN_H // 2)
    elif module["type"] == "image":
        spacing = 200
        y = SCREEN_H // 2
        x_center = SCREEN_W // 2
        for i, img_key in enumerate([flanker, target, flanker]):
            img = module["img_dict"][img_key]
            rect = img.get_rect(center=(x_center + (i - 1) * spacing, y))
            screen.blit(img, rect)
    elif module["type"] == "mixed":
        flank_letter = random.choice(module["letters"])
        draw_mixed_triplet(target, flank_letter, module["img_dict"])
    pygame.display.flip()

    # ---------------- RESPONSE COLLECTION ----------------
    start = time.time()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_LEFT, pygame.K_RIGHT):
                response = key_map[e.key]
                rt = time.time() - start
                correct = (response == group_index)
                if record and results is not None:
                    results.append([module["name"], target, condition, flanker,
                                    ("LEFT" if response == 0 else "RIGHT"), correct, rt])
                return correct, rt
# -------------------- MAIN --------------------
participant = input("Enter Participant ID: ")
all_results = []
random.shuffle(modules)

instruction_screen()

for module in modules:
    module_instructions(module)

    # ---- PRACTICE ----
    practice_correct, practice_rts = [], []
    for _ in range(PRACTICE_TRIALS):
        c, rt = run_trial(module, record=False)
        if c is not None:
            practice_correct.append(c)
            practice_rts.append(rt)

    acc = (sum(practice_correct) / len(practice_correct) * 100) if practice_correct else 0
    mean_rt = (sum(practice_rts) / len(practice_rts)) if practice_rts else 0

    screen.fill(BG_COLOR)
    draw_text_center("Practice Complete", SCREEN_H // 2 - 40)
    draw_text_center(f"Accuracy: {acc:.1f}%", SCREEN_H // 2)
    draw_text_center("Experiment Begins", SCREEN_H // 2 + 80)
    pygame.display.flip()
    pygame.time.delay(2000)

    # ---- MAIN TRIALS ----
    conditions = ["congruent", "incongruent", "neutral"]
    per_condition = TRIALS // len(conditions)
    condition_list = conditions * per_condition
    while len(condition_list) < TRIALS:
        condition_list.append(random.choice(conditions))
    random.shuffle(condition_list)

    for cond in condition_list:
        run_trial(module, record=True, results=all_results, forced_condition=cond)

# -------------------- SAVE RESULTS --------------------
filename = f"{participant}.csv"
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Module", "Target/Check", "Condition", "Flanker", "Response", "Correct", "RT"])
    writer.writerows(all_results)

# -------------------- END --------------------
screen.fill(BG_COLOR)
draw_text_center("Experiment Complete", SCREEN_H // 2)
draw_text_center("Thank You!", SCREEN_H // 2 + 60)
pygame.display.flip()
time.sleep(2)
pygame.quit()
print(f"Results saved as {filename}")
