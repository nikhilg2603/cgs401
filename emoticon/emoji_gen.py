''' This code is to ensure all emoticons used have same brightness and color'''

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import os


emojis = ["🙂", "😁", "🙁", "😞", "🟡", "🟨"]
target_luminance = 120.0           # desired mean brightness (0–255)
output_folder = "normalized_emoji"
font_size = 160


font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"

os.makedirs(output_folder, exist_ok=True)


font = ImageFont.truetype(font_path, font_size)

def compute_luminance(img):
    """Compute average luminance of an RGB PIL image."""
    arr = np.asarray(img.convert("RGB"), dtype=np.float32)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    return lum.mean()

def adjust_luminance(img, target_lum):
    """Adjust brightness to reach target luminance."""
    current_lum = compute_luminance(img)
    if current_lum == 0:
        return img
    factor = target_lum / current_lum
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

def make_yellow_tint(img):
    """Apply a yellow tint (reduce blue channel, enhance red and green)."""
    arr = np.array(img.convert("RGB"), dtype=np.float32)
    
    arr[..., 0] *= 1.1   # red
    arr[..., 1] *= 1.1   # green
    arr[..., 2] *= 0.3   # blue down
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    
    return Image.fromarray(arr)

for emoji in emojis:
    img = Image.new("RGB", (200, 200), "white")
    draw = ImageDraw.Draw(img)

    bbox = draw.textbbox((0, 0), emoji, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((200 - w) / 2, (200 - h) / 2), emoji, font=font, fill="black")

    img = adjust_luminance(img, target_luminance)
    img = make_yellow_tint(img)

    filename = f"{ord(emoji):x}.png"
    img.save(os.path.join(output_folder, filename))
    print(f" Saved yellow-tinted {emoji} -> {filename}")

print(" All emoji images yellow-tinted and saved to:", output_folder)
