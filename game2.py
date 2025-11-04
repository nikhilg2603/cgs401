import pygame
import sys
import time
import random
import csv
import os
from datetime import datetime

# -------------------- CONFIG --------------------
SCREEN_W, SCREEN_H = 1000, 600
BG_COLOR = (30, 30, 30)
TRIALS = 30
FIX_MS = 500
STIM_MS = 1500
ITI_MS = 400
FACE_SIZE = 160
FPS = 60
RESPONSE_MAP = {'happy': pygame.K_LEFT, 'sad': pygame.K_RIGHT}

# -------------------- INIT --------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Emoji Flanker Task")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# -------------------- LOAD EMOJI IMAGES --------------------
def load_emoji_images(base_path='emojis'):
    categories = ['happy', 'sad', 'neutral']
    emoji_imgs = {}
    for cat in categories:
        folder = os.path.join(base_path, cat)
        files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg'))]
        imgs = []
        for file in files:
            img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
            img = pygame.transform.smoothscale(img, (FACE_SIZE, FACE_SIZE))
            imgs.append(img)
        emoji_imgs[cat] = imgs
    return emoji_imgs

emojis = load_emoji_images()

# -------------------- TRIAL GENERATION --------------------
trial_types = ['congruent', 'incongruent', 'neutral']
trials = []
for i in range(TRIALS):
    ttype = random.choice(trial_types)
    center_cat = random.choice(['happy', 'sad'])
    if ttype == 'congruent':
        flank_cat = center_cat
    elif ttype == 'incongruent':
        flank_cat = 'sad' if center_cat == 'happy' else 'happy'
    else:
        flank_cat = 'neutral'
    trials.append({
        'trial_index': i+1,
        'ttype': ttype,
        'center_cat': center_cat,
        'flank_cat': flank_cat
    })
random.shuffle(trials)

# -------------------- INSTRUCTION SCREEN --------------------
def draw_text_lines(lines):
    screen.fill(BG_COLOR)
    y = 100
    for line in lines:
        surf = font.render(line, True, (230, 230, 230))
        rect = surf.get_rect(center=(SCREEN_W//2, y))
        screen.blit(surf, rect)
        y += 35
    pygame.display.flip()

instructions = [
    "Emoji Flanker Task",
    "",
    "Focus on the MIDDLE emoji.",
    "If it's HAPPY, press LEFT ARROW (←).",
    "If it's SAD, press RIGHT ARROW (→).",
    "Neutral (yellow) emojis only appear as flankers — IGNORE them.",
    "",
    "Respond quickly and accurately.",
    "",
    "Press any key to begin!"
]

draw_text_lines(instructions)
waiting = True
while waiting:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if ev.type == pygame.KEYDOWN:
            waiting = False
    clock.tick(FPS)

# -------------------- RUN TRIALS --------------------
positions_x = [SCREEN_W//2 - 220, SCREEN_W//2, SCREEN_W//2 + 220]
ypos = SCREEN_H//2
results = []

for tr in trials:
    # Fixation cross
    screen.fill(BG_COLOR)
    fix = font.render("+", True, (220, 220, 220))
    screen.blit(fix, fix.get_rect(center=(SCREEN_W//2, ypos)))
    pygame.display.flip()
    pygame.time.delay(FIX_MS)

    # Choose images
    center_img = random.choice(emojis[tr['center_cat']])
    flank_img = random.choice(emojis[tr['flank_cat']])

    # Draw stimuli (Flanker - Target - Flanker)
    screen.fill(BG_COLOR)
    screen.blit(flank_img, flank_img.get_rect(center=(positions_x[0], ypos)))
    screen.blit(center_img, center_img.get_rect(center=(positions_x[1], ypos)))
    screen.blit(flank_img, flank_img.get_rect(center=(positions_x[2], ypos)))
    pygame.display.flip()

    # Record response
    stim_onset = time.time()
    responded = False
    rt = None
    resp_key = None

    while (time.time() - stim_onset) < (STIM_MS / 1000.0):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and not responded:
                resp_key = ev.key
                rt = (time.time() - stim_onset) * 1000.0
                responded = True
        clock.tick(FPS)

    # Evaluate correctness
    expected = RESPONSE_MAP[tr['center_cat']]
    correct = 1 if (responded and resp_key == expected) else 0

    # Inter-trial interval
    screen.fill(BG_COLOR)
    pygame.display.flip()
    pygame.time.delay(ITI_MS)

    # Store trial data
    results.append({
        'trial': tr['trial_index'],
        'type': tr['ttype'],
        'center': tr['center_cat'],
        'flankers': tr['flank_cat'],
        'response_key': pygame.key.name(resp_key) if resp_key else 'NA',
        'rt_ms': round(rt, 1) if rt else None,
        'correct': correct
    })

# -------------------- SAVE RESULTS --------------------
participant_id = input("Enter participant ID: ")
now = datetime.now().strftime("%Y%m%d_%H%M%S")
fname = f"results_{participant_id}_{now}.csv"

keys = ['trial', 'type', 'center', 'flankers', 'response_key', 'rt_ms', 'correct']
with open(fname, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(results)

# -------------------- SUMMARY SCREEN --------------------
acc = sum(r['correct'] for r in results) / len(results) * 100.0
rt_vals = [r['rt_ms'] for r in results if r['rt_ms'] and r['correct']]
mean_rt = sum(rt_vals)/len(rt_vals) if rt_vals else 0.0

summary = [
    f"Block complete!",
    f"Accuracy: {acc:.1f}%",
    f"Mean RT (correct trials): {mean_rt:.1f} ms",
    "",
    f"Data saved as: {fname}",
    "",
    "Press any key to exit."
]
draw_text_lines(summary)
waiting = True
while waiting:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if ev.type == pygame.KEYDOWN:
            waiting = False
    clock.tick(FPS)

pygame.quit()
print(f"Saved results to {fname}")