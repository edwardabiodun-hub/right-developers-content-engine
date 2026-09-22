import json
import random
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from .campaigns import CampaignManifest
from .orchestrator import ContentPackage


PLATFORM_DIMENSIONS = {
    "linkedin": (1200, 627),
    "instagram": (1080, 1350),
    "facebook": (1200, 630),
}


def _font(size: int) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                return ImageFont.truetype(str(candidate), size)
            except OSError:
                pass
    return ImageFont.load_default()


def _source_scene(size: tuple[int, int], source_path: Path | None) -> Image.Image:
    if source_path:
        image = Image.open(source_path).convert("RGB")
        return _cover_crop(image, size)
    width, height = size
    image = Image.new("RGB", size, (20, 29, 31))
    pixels = image.load()
    rng = random.Random(42)
    for y in range(height):
        for x in range(width):
            grain = rng.randint(-10, 10)
            band = int(22 * (1 - y / max(height, 1)))
            pixels[x, y] = (max(12, 48 + grain + band), max(17, 39 + grain), max(18, 34 + grain))
    draw = ImageDraw.Draw(image, "RGBA")
    for index in range(28):
        x = rng.randint(-100, width)
        y = rng.randint(-80, height)
        radius = rng.randint(35, 150)
        color = rng.choice([(184, 169, 137, 185), (92, 109, 105, 185), (218, 207, 180, 150), (48, 67, 64, 200)])
        draw.ellipse((x - radius, y - radius // 2, x + radius, y + radius // 2), fill=color)
    return image.filter(ImageFilter.GaussianBlur(1.2))


def _cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize without distorting the source composition, then crop to fill."""
    target_width, target_height = size
    scale = max(target_width / image.width, target_height / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - target_width) // 2)
    top = max(0, (resized.height - target_height) // 2)
    return resized.crop((left, top, left + target_width, top + target_height))


def _overlay(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], alpha: int = 190) -> None:
    draw.rectangle(box, fill=(7, 16, 18, alpha))


def _text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int, fill=(247, 243, 234), anchor=None) -> None:
    draw.text(xy, text, font=_font(size), fill=fill, anchor=anchor)


def _linkedin_image(base: Image.Image, manifest: CampaignManifest) -> Image.Image:
    image = base.copy()
    draw = ImageDraw.Draw(image, "RGBA")
    _overlay(draw, (0, 0, 700, image.height), 205)
    _text(draw, (54, 52), "RIGHT DEVELOPERS", 24, (213, 129, 67))
    _text(draw, (54, 145), "TRADE\nREADINESS", 74)
    _text(draw, (54, 350), "Specification before terms.", 31, (225, 214, 192))
    _text(draw, (54, 515), "Zircon sand | buyer education", 20, (214, 220, 214))
    return image


def _instagram_image(base: Image.Image, manifest: CampaignManifest) -> Image.Image:
    image = base.copy()
    draw = ImageDraw.Draw(image, "RGBA")
    _overlay(draw, (0, 0, image.width, 410), 205)
    _overlay(draw, (0, image.height - 425, image.width, image.height), 215)
    _text(draw, (54, 54), "RIGHT DEVELOPERS", 23, (213, 129, 67))
    _text(draw, (54, 135), "A serious\ninquiry starts\nwith detail.", 62)
    _text(draw, (54, image.height - 360), "01  SPECIFICATION / ASSAY\n02  QUANTITY + CADENCE\n03  DESTINATION + INSPECTION", 27, (247, 243, 234))
    return image


def _facebook_image(base: Image.Image, manifest: CampaignManifest) -> Image.Image:
    image = base.copy()
    draw = ImageDraw.Draw(image, "RGBA")
    _overlay(draw, (0, 0, image.width, image.height), 125)
    draw.rounded_rectangle((56, 54, 760, 570), radius=18, fill=(9, 19, 20, 214), outline=(213, 129, 67, 220), width=2)
    _text(draw, (94, 96), "TRADE READINESS", 28, (213, 129, 67))
    _text(draw, (94, 178), "A price request\nis not yet a\ncommercial inquiry.", 56)
    _text(draw, (94, 450), "Zircon sand | specification • quantity • destination", 20, (225, 214, 192))
    return image


def render_platform_assets(
    package: ContentPackage,
    manifest: CampaignManifest,
    output_dir: Path,
    source_path: Path | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    source = _source_scene((1600, 1600), source_path)
    renderers = {"linkedin": _linkedin_image, "instagram": _instagram_image, "facebook": _facebook_image}
    assets: dict[str, Any] = {}
    for platform in manifest.platforms:
        if platform not in PLATFORM_DIMENSIONS or platform not in renderers:
            continue
        dimensions = PLATFORM_DIMENSIONS[platform]
        scene = _cover_crop(source, dimensions)
        rendered = renderers[platform](scene, manifest).convert("RGB")
        path = output_dir / f"{platform}.png"
        rendered.save(path, format="PNG", optimize=True)
        assets[platform] = {"path": str(path), "dimensions": list(dimensions), "format": "png", "source": "provided_image" if source_path else "deterministic_mineral_scene"}
    manifest_payload = {
        "content_id": package.content_id,
        "human_review_required": package.human_review_required,
        "assets": assets,
    }
    (output_dir / "asset-manifest.json").write_text(json.dumps(manifest_payload, indent=2) + "\n", encoding="utf-8")
    return manifest_payload
