"""Render a self-contained README workflow animation from saved case-study results.

This is a navigation/explanation graphic, not a new experiment. Requires Pillow (installed with matplotlib).
"""
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "readme"
WIDTH, HEIGHT = 1400, 580
NAVY, PANEL, BORDER = "#081321", "#122238", "#2c4059"
WHITE, MUTED, ACCENT = "#f1f6fd", "#a9bdd5", "#61e1c4"


def font(size, bold=False):
    candidates = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
                  "arialbd.ttf" if bold else "arial.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def number(pattern, text):
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"Missing saved-result field: {pattern}")
    return float(match.group(1))


def values():
    search = (ROOT / "results" / "ma_crossover.txt").read_text()
    main = search.split("Cost 5 bps per change in position\n", 1)[1].split("Cost 10 bps", 1)[0]
    checks = (ROOT / "results" / "case_study_checks.txt").read_text()
    delay = (ROOT / "results" / "delayed_alpha.txt").read_text()
    return (number(r"annual Sharpe ([\d.]+)", main),
            number(r"Buy-and-hold market: annual Sharpe ([\d.]+)", search),
            number(r"DSR, N = 93: ([\d.]+)", main),
            number(r"statistic [\d.]+, p-value ([\d.]+)", checks),
            number(r"p=([0-9]+(?:\.[0-9]+)?)", delay))


def wrapped(draw, text, xy, face, fill, width, spacing=7):
    x, y = xy
    line = ""
    for word in text.split():
        candidate = (line + " " + word).strip()
        if draw.textlength(candidate, font=face) > width and line:
            draw.text((x, y), line, font=face, fill=fill)
            y += face.size + spacing
            line = word
        else:
            line = candidate
    if line:
        draw.text((x, y), line, font=face, fill=fill)


def render(stage, fraction, metrics):
    selected, market, dsr, sharpe_p, alpha_p = metrics
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    draw.text((48, 35), "A backtest is the beginning of the question.", font=font(40, True), fill=WHITE)
    draw.text((50, 97), "93 moving-average rules  /  US market factor  /  5 bps per position change",
              font=font(21), fill=MUTED)
    draw.rounded_rectangle((1140, 137, 1350, 168), radius=10, fill=PANEL)
    draw.text((1157, 142), "RECOMPUTED RESULTS", font=font(14, True), fill=ACCENT)
    cards = [
        ("01  SEARCH", f"{selected:.3f}", "selected annualized Sharpe", f"market: {market:.3f}"),
        ("02  DEFLATE", f"{dsr:.3f}", "2014 DSR", "zero-skill screen"),
        ("03  BENCHMARK", f"p {sharpe_p:.3f}", "Sharpe SPA vs market", "advantage not established"),
        ("04  STRESS EXECUTION", f"p {alpha_p:.3f}", "alpha SPA, extra day of delay", "exploratory sensitivity"),
    ]
    for i, (title, value, line1, line2) in enumerate(cards):
        x = 48 + 330 * i
        color = ACCENT if i == stage else BORDER
        draw.rounded_rectangle((x, 190, x + 312, 395), radius=18, fill=PANEL, outline=color, width=3 if i == stage else 1)
        draw.text((x + 20, 211), title, font=font(16, True), fill=ACCENT if i == stage else MUTED)
        draw.text((x + 20, 251), value, font=font(44, True), fill=WHITE)
        draw.text((x + 20, 326), line1, font=font(17), fill=WHITE)
        draw.text((x + 20, 355), line2, font=font(17), fill=MUTED)
    centers = [204 + 330 * i for i in range(4)]
    draw.line((centers[0], 433, centers[-1], 433), fill=BORDER, width=3)
    for x in centers:
        draw.ellipse((x - 5, 428, x + 5, 438), fill=BORDER)
    progress = centers[0] + (centers[-1] - centers[0]) * fraction
    draw.line((centers[0], 433, progress, 433), fill=ACCENT, width=3)
    draw.ellipse((progress - 8, 425, progress + 8, 441), fill=ACCENT)
    captions = ["A strong historical winner starts the investigation.",
                "A zero-skill screen does not establish superiority to the market.",
                "The standalone Sharpe advantage is not statistically established.",
                "The exploratory alpha finding is sensitive to execution timing."]
    wrapped(draw, captions[stage], (48, 472), font(23), WHITE, 1304)
    draw.text((48, 548), "Working paper  /  Conditional inference  /  No external peer review", font=font(15), fill=MUTED)
    return image


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    metrics = values()
    frames = [render(stage, (stage + step / 16) / 4, metrics)
              for stage in range(4) for step in range(16)]
    frames.append(render(3, 1.0, metrics))
    palette = [frame.quantize(colors=96, dither=Image.Dither.NONE) for frame in frames]
    palette[0].save(OUT / "research-overview.gif", save_all=True, append_images=palette[1:],
                    duration=[110] * (len(palette) - 1) + [1400], loop=0, optimize=True, disposal=1)
    render(3, 1.0, metrics).save(OUT / "research-overview.png", optimize=True)
    print(f"Saved animated and static README overview to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
