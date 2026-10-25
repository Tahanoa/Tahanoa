import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

# Ensure assets directory exists
os.makedirs('assets', exist_ok=True)

# Color Palette
BG_COLOR = (3, 6, 5)          # #030605
BG_SEC_COLOR = (7, 17, 11)     # #07110B
NEON_GREEN = (0, 255, 102)     # #00FF66
EMERALD = (0, 200, 83)         # #00C853
MUTED_GREEN = (114, 168, 137)  # #72A889
PRIMARY_TEXT = (230, 255, 237) # #E6FFED
SEC_TEXT = (156, 183, 163)     # #9CB7A3
DARK_GREEN = (15, 35, 22)      # Cyber dark green

# Try to load mono fonts
FONT_PATH_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_PATH_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_PATH_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_header = load_font(FONT_PATH_MONO_BOLD, 12)
font_title_big = load_font(FONT_PATH_SANS_BOLD, 52)
font_sub = load_font(FONT_PATH_MONO_BOLD, 16)
font_tags = load_font(FONT_PATH_MONO_BOLD, 12)
font_mascot = load_font(FONT_PATH_MONO_BOLD, 11)

# --- 1. HERO BANNER GENERATOR ---
def generate_hero_banner():
    width, height = 850, 280
    num_frames = 24
    frames = []

    # Matrix columns setup
    random.seed(42)
    matrix_cols = 16
    col_x = [random.randint(10, width - 20) for _ in range(matrix_cols)]
    col_y = [random.randint(0, height) for _ in range(matrix_cols)]
    col_speed = [random.randint(4, 12) for _ in range(matrix_cols)]
    col_chars = ["0", "1", "X", "7", "A", "F", ">", "<", "/", "{", "}", "[", "]"]

    for frame in range(num_frames):
        # Create base image
        img = Image.new("RGB", (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw subtle grid background
        for x in range(0, width, 25):
            draw.line([(x, 0), (x, height)], fill=(8, 20, 14), width=1)
        for y in range(0, height, 25):
            draw.line([(0, y), (width, y)], fill=(8, 20, 14), width=1)

        # Draw Matrix digital rain in background
        for i in range(matrix_cols):
            y_pos = (col_y[i] + frame * col_speed[i]) % (height + 40) - 20
            char = col_chars[(frame + i) % len(col_chars)]
            # Draw tail
            draw.text((col_x[i], y_pos - 15), char, fill=MUTED_GREEN, font=font_header)
            draw.text((col_x[i], y_pos), char, fill=NEON_GREEN, font=font_header)

        # Draw tech border
        margin = 10
        # Main outer box
        draw.rectangle([(margin, margin), (width - margin, height - margin)], outline=DARK_GREEN, width=1)
        draw.rectangle([(margin + 3, margin + 3), (width - margin - 3, height - margin - 3)], outline=EMERALD, width=1)

        # Tech Corner Brackets
        corner_len = 20
        # Top-Left
        draw.line([(margin, margin), (margin + corner_len, margin)], fill=NEON_GREEN, width=3)
        draw.line([(margin, margin), (margin, margin + corner_len)], fill=NEON_GREEN, width=3)
        # Top-Right
        draw.line([(width - margin, margin), (width - margin - corner_len, margin)], fill=NEON_GREEN, width=3)
        draw.line([(width - margin, margin), (width - margin, margin + corner_len)], fill=NEON_GREEN, width=3)
        # Bottom-Left
        draw.line([(margin, height - margin), (margin + corner_len, height - margin)], fill=NEON_GREEN, width=3)
        draw.line([(margin, height - margin), (margin, height - margin - corner_len)], fill=NEON_GREEN, width=3)
        # Bottom-Right
        draw.line([(width - margin, height - margin), (width - margin - corner_len, height - margin)], fill=NEON_GREEN, width=3)
        draw.line([(width - margin, height - margin), (width - margin, height - margin - corner_len)], fill=NEON_GREEN, width=3)

        # Top Header Bar
        draw.rectangle([(margin + 15, margin + 8), (width - margin - 15, margin + 32)], fill=BG_SEC_COLOR, outline=DARK_GREEN)
        header_text = " [ SYSTEM // TAHANOA_OS v4.2.0 ]   [ STATUS: ONLINE ]   [ LOC: IRAN ]"
        draw.text((margin + 25, margin + 12), header_text, fill=MUTED_GREEN, font=font_header)

        # Pulse indicator in header
        pulse_color = NEON_GREEN if (frame // 3) % 2 == 0 else EMERALD
        draw.ellipse([(width - margin - 35, margin + 17), (width - margin - 27, margin + 25)], fill=pulse_color)

        # Big Title: TAHANOA
        title_str = "TAHANOA"
        title_x = width // 2 - 130
        title_y = 75

        # Glitch effect on certain frames
        glitch_frame = frame in [5, 6, 17, 18]
        if glitch_frame:
            offset_x = random.randint(-4, 4)
            offset_y = random.randint(-2, 2)
            # Glitch shadow behind
            draw.text((title_x + offset_x, title_y + offset_y), title_str, fill=(0, 100, 50), font=font_title_big)
            draw.text((title_x - offset_x, title_y - offset_y), title_str, fill=(0, 255, 200), font=font_title_big)

        # Main Title Glow & Text
        draw.text((title_x + 2, title_y + 2), title_str, fill=EMERALD, font=font_title_big)
        draw.text((title_x, title_y), title_str, fill=PRIMARY_TEXT, font=font_title_big)

        # Underline accent for title
        draw.line([(title_x - 10, title_y + 62), (title_x + 270, title_y + 62)], fill=NEON_GREEN, width=2)
        draw.rectangle([(title_x + 120, title_y + 60), (title_x + 140, title_y + 64)], fill=NEON_GREEN)

        # Subtitle with cursor
        subtitle_base = "> FULL-STACK DEVELOPER & CREATIVE ARCHITECT"
        cursor = "_" if (frame // 4) % 2 == 0 else " "
        draw.text((width // 2 - 215, 160), subtitle_base + cursor, fill=NEON_GREEN, font=font_sub)

        # Tech Tags at bottom
        tags = ["JAVA", "SPRING BOOT", "PHP", "JAVASCRIPT", "POSTGRESQL", "C++"]
        tag_x = 60
        tag_y = 210
        for tag in tags:
            tag_fmt = f"[ {tag} ]"
            draw.rectangle([(tag_x, tag_y), (tag_x + len(tag_fmt)*8 + 10, tag_y + 22)], fill=BG_SEC_COLOR, outline=DARK_GREEN)
            draw.text((tag_x + 6, tag_y + 3), tag_fmt, fill=SEC_TEXT, font=font_tags)
            tag_x += len(tag_fmt)*8 + 24

        # Scanning line animation sweep
        scan_y = (frame * 12) % height
        draw.line([(margin + 5, scan_y), (width - margin - 5, scan_y)], fill=(0, 255, 102, 40), width=2)

        # Scanline overlay
        for y in range(0, height, 4):
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, 80), width=1)

        frames.append(img)

    frames[0].save(
        "assets/hero-banner.gif",
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=100,
        loop=0
    )
    print("Generated assets/hero-banner.gif")

# --- 2. CYBERPUNK MASCOT GENERATOR ---
def generate_mascot():
    width, height = 240, 200
    num_frames = 16
    frames = []

    for frame in range(num_frames):
        img = Image.new("RGB", (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Tech frame
        draw.rectangle([(5, 5), (width - 5, height - 5)], outline=DARK_GREEN, width=1)
        draw.rectangle([(8, 8), (width - 8, height - 8)], outline=BG_SEC_COLOR, width=2)

        # Label header
        draw.rectangle([(15, 12), (width - 15, 30)], fill=BG_SEC_COLOR)
        draw.text((22, 14), "[ DAEMON: TAHA_GHOST ]", fill=NEON_GREEN, font=font_mascot)

        # Floating vertical bobbing offset
        bob = int(math.sin(frame * (2 * math.pi / num_frames)) * 4)

        cx, cy = width // 2, height // 2 + 5 + bob

        # Cyber Ghost/Cat Mascot Pixel-Art Drawing
        # Aura / Glow background behind mascot
        draw.ellipse([(cx - 45, cy - 35), (cx + 45, cy + 40)], fill=(8, 30, 20))

        # Ears
        draw.polygon([(cx - 30, cy - 30), (cx - 15, cy - 48), (cx - 5, cy - 25)], fill=BG_SEC_COLOR, outline=NEON_GREEN)
        draw.polygon([(cx + 5, cy - 25), (cx + 15, cy - 48), (cx + 30, cy - 30)], fill=BG_SEC_COLOR, outline=NEON_GREEN)

        # Inner ear glow
        draw.polygon([(cx - 24, cy - 32), (cx - 15, cy - 42), (cx - 10, cy - 28)], fill=EMERALD)
        draw.polygon([(cx + 10, cy - 28), (cx + 15, cy - 42), (cx + 24, cy - 32)], fill=EMERALD)

        # Head / Body Hood
        draw.ellipse([(cx - 35, cy - 30), (cx + 35, cy + 30)], fill=BG_SEC_COLOR, outline=NEON_GREEN, width=2)

        # Cyber Visor / Glasses
        visor_y = cy - 8
        draw.rectangle([(cx - 28, visor_y - 6), (cx + 28, visor_y + 8)], fill=BG_COLOR, outline=NEON_GREEN, width=2)

        # Visor Animated HUD Code / Glint
        glint_x = (cx - 20) + ((frame * 3) % 36)
        draw.line([(glint_x, visor_y - 4), (glint_x + 6, visor_y + 6)], fill=NEON_GREEN, width=2)
        draw.text((cx - 22, visor_y - 5), "01", fill=EMERALD, font=font_mascot)

        # Cute Cyber Mouth
        draw.line([(cx - 6, cy + 12), (cx, cy + 15), (cx + 6, cy + 12)], fill=NEON_GREEN, width=2)

        # Whisker Cyber Antenna Lines
        draw.line([(cx - 32, cy - 2), (cx - 45, cy - 8)], fill=MUTED_GREEN, width=1)
        draw.line([(cx - 32, cy + 6), (cx - 48, cy + 6)], fill=MUTED_GREEN, width=1)
        draw.line([(cx + 32, cy - 2), (cx + 45, cy - 8)], fill=MUTED_GREEN, width=1)
        draw.line([(cx + 32, cy + 6), (cx + 48, cy + 6)], fill=MUTED_GREEN, width=1)

        # Spectral Ghost Tail / Bottom wisps
        for wisp in range(5):
            wx = cx - 24 + wisp * 12
            wy = cy + 28 + int(math.sin(frame + wisp) * 3)
            draw.ellipse([(wx - 4, wy), (wx + 4, wy + 10)], fill=EMERALD)

        # Digital particles floating up
        random.seed(frame + 100)
        for _ in range(6):
            px = random.randint(20, width - 20)
            py = random.randint(40, height - 20)
            draw.rectangle([(px, py), (px + 2, py + 2)], fill=NEON_GREEN)

        # Status footer
        draw.text((22, height - 22), "STATUS: SYSTEM ACTIVE", fill=SEC_TEXT, font=font_mascot)

        frames.append(img)

    frames[0].save(
        "assets/mascot.gif",
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=120,
        loop=0
    )
    print("Generated assets/mascot.gif")

# --- 3. ANIMATED DIVIDER GENERATOR ---
def generate_divider():
    width, height = 850, 16
    num_frames = 20
    frames = []

    for frame in range(num_frames):
        img = Image.new("RGB", (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Center line
        cy = height // 2
        draw.line([(10, cy), (width - 10, cy)], fill=DARK_GREEN, width=2)
        draw.line([(40, cy), (width - 40, cy)], fill=EMERALD, width=1)

        # End nodes
        draw.rectangle([(10, cy - 4), (18, cy + 4)], fill=BG_SEC_COLOR, outline=NEON_GREEN)
        draw.rectangle([(width - 18, cy - 4), (width - 10, cy + 4)], fill=BG_SEC_COLOR, outline=NEON_GREEN)

        # Moving pulse light packet
        pulse_x = int(20 + (frame / num_frames) * (width - 40))

        # Pulse Glow tail
        for tail in range(15):
            tx = pulse_x - tail * 3
            if 20 <= tx <= width - 20:
                alpha_color = (0, 255 - tail * 15, 102 - tail * 5)
                draw.line([(tx, cy), (tx + 3, cy)], fill=alpha_color, width=3)

        # Main Pulse Node
        if 20 <= pulse_x <= width - 20:
            draw.ellipse([(pulse_x - 5, cy - 5), (pulse_x + 5, cy + 5)], fill=PRIMARY_TEXT, outline=NEON_GREEN)

        frames.append(img)

    frames[0].save(
        "assets/divider.gif",
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=80,
        loop=0
    )
    print("Generated assets/divider.gif")

if __name__ == "__main__":
    generate_hero_banner()
    generate_mascot()
    generate_divider()
    print("All assets successfully generated!")
