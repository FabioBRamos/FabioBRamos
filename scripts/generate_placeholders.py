from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROJECTS = ASSETS / "projects"

COLORS = {
    "bg": "#1a1b27",
    "surface": "#24283b",
    "border": "#414868",
    "muted": "#565f89",
    "text": "#9aa5ce",
    "blue": "#7aa2f7",
    "purple": "#bb9af7",
    "green": "#9ece6a",
    "gold": "#e0af68",
    "panel": "#32344a",
}


def hex_color(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
) -> None:
    x0, y0, x1, y1 = box
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = x0 + (x1 - x0 - text_w) / 2
    y = y0 + (y1 - y0 - text_h) / 2
    draw.multiline_text((x, y), text, font=font, fill=hex_color(fill), align="center")


def dashed_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    outline: str,
    width: int = 2,
    dash: int = 8,
    gap: int = 6,
) -> None:
    x0, y0, x1, y1 = box
    color = hex_color(outline)
    for x in range(x0, x1, dash + gap):
        draw.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)
        draw.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=width)
    for y in range(y0, y1, dash + gap):
        draw.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
        draw.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=width)


def project_card(
    filename: str,
    title: str,
    subtitle: str,
    accent: str,
    layout: str,
) -> None:
    image = Image.new("RGB", (640, 360), hex_color(COLORS["bg"]))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((16, 16, 624, 344), radius=8, fill=hex_color(COLORS["surface"]))
    dashed_rect(draw, (16, 16, 624, 344), COLORS["border"])

    if layout == "sgi":
        draw.rounded_rectangle((40, 48, 200, 312), radius=4, outline=hex_color(COLORS["panel"]), width=1)
        draw.rounded_rectangle((220, 48, 600, 84), radius=3, fill=hex_color(COLORS["panel"]))
        draw.rounded_rectangle((220, 100, 400, 190), radius=4, outline=hex_color(COLORS["panel"]), width=1)
        draw.rounded_rectangle((420, 100, 600, 190), radius=4, outline=hex_color(COLORS["panel"]), width=1)
        draw.rounded_rectangle((220, 210, 600, 312), radius=4, outline=hex_color(COLORS["panel"]), width=1)
    elif layout == "morpho":
        draw.rounded_rectangle((40, 40, 600, 68), radius=3, fill=hex_color(COLORS["panel"]))
        draw.rounded_rectangle((40, 80, 160, 312), radius=4, outline=hex_color(COLORS["panel"]), width=1)
        draw.rounded_rectangle((180, 80, 600, 312), radius=4, outline=hex_color(COLORS["panel"]), width=1)
    elif layout == "carcinicultura":
        draw.rounded_rectangle((40, 48, 600, 56), radius=2, fill=hex_color(COLORS["panel"]))
        for index, x0 in enumerate((40, 190, 340, 490)):
            width = 130 if index < 3 else 110
            draw.rounded_rectangle((x0, 72, x0 + width, 172), radius=4, outline=hex_color(COLORS["panel"]), width=1)
        draw.rounded_rectangle((40, 190, 600, 312), radius=4, outline=hex_color(COLORS["panel"]), width=1)
    elif layout == "solar":
        draw.ellipse((272, 102, 368, 198), outline=hex_color(COLORS["gold"]), width=3)
        draw.ellipse((296, 126, 344, 174), fill=hex_color(COLORS["gold"]))
        draw.rounded_rectangle((80, 230, 560, 240), radius=3, fill=hex_color(COLORS["panel"]))
        draw.rounded_rectangle((120, 255, 520, 263), radius=2, fill=hex_color(COLORS["panel"]))
        draw.rounded_rectangle((160, 275, 480, 283), radius=2, fill=hex_color(COLORS["panel"]))

    draw_centered_text(
        draw,
        (40, 230, 600, 270),
        "Substitua por screenshot",
        load_font(18),
        COLORS["muted"],
    )
    draw_centered_text(
        draw,
        (40, 268, 600, 300),
        subtitle,
        load_font(14),
        accent,
    )
    draw_centered_text(
        draw,
        (40, 308, 600, 340),
        title,
        load_font(16, bold=True),
        COLORS["text"],
    )

    output = PROJECTS / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)


def banner() -> None:
    image = Image.new("RGB", (1100, 280), hex_color(COLORS["bg"]))
    draw = ImageDraw.Draw(image)
    draw.ellipse((800, 0, 1040, 240), fill=(36, 42, 68))
    draw.ellipse((90, 130, 270, 310), fill=(40, 38, 58))
    draw_centered_text(draw, (0, 70, 1100, 130), "Fábio Ramos", load_font(42, bold=True), COLORS["text"])
    draw_centered_text(
        draw,
        (0, 130, 1100, 170),
        "Desenvolvedor Full Stack · Soluções · Automação · Integração",
        load_font(20),
        "#9aa5ce",
    )
    draw.rounded_rectangle((350, 190, 750, 194), radius=2, fill=hex_color(COLORS["blue"]))
    draw_centered_text(draw, (0, 210, 1100, 240), "github.com/FabioBRamos", load_font(14), COLORS["muted"])
    image.save(ASSETS / "banner.png", format="PNG", optimize=True)


def main() -> None:
    banner()
    project_card(
        "gestor-morpho.png",
        "Gestor Morpho — Desktop C#",
        "assets/projects/gestor-morpho.png",
        COLORS["green"],
        "morpho",
    )
    project_card(
        "sgi.png",
        "SGI — Sistema de Gestão Interna",
        "assets/projects/sgi.png",
        COLORS["blue"],
        "sgi",
    )
    project_card(
        "carcinicultura.png",
        "Carcinicultura — Web C#",
        "assets/projects/carcinicultura.png",
        COLORS["purple"],
        "carcinicultura",
    )
    project_card(
        "sistema-solar.png",
        "Sistema Solar — Django",
        "assets/projects/sistema-solar.png",
        COLORS["gold"],
        "solar",
    )
    print("PNG placeholders generated.")


if __name__ == "__main__":
    main()
