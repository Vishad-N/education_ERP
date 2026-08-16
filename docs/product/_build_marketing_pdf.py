"""One-off builder for docs/product/marketing-features.pdf."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "marketing-features.md"
OUTPUT = ROOT / "marketing-features.pdf"

NAVY = colors.HexColor("#1B365D")
TEAL = colors.HexColor("#0E7C7B")
INK = colors.HexColor("#243040")
MUTED = colors.HexColor("#5B6775")
RULE = colors.HexColor("#D5DDE6")
PANEL = colors.HexColor("#F3F6F9")
ACCENT_BG = colors.HexColor("#E8F4F3")


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("`", "")
    )


def parse_markdown(path: Path) -> list[tuple[str, object]]:
    blocks: list[tuple[str, object]] = []
    paragraph: list[str] = []
    bullets: list[str] = []
    numbers: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(("p", " ".join(paragraph)))
            paragraph = []

    def flush_bullets() -> None:
        nonlocal bullets
        if bullets:
            blocks.append(("ul", bullets[:]))
            bullets = []

    def flush_numbers() -> None:
        nonlocal numbers
        if numbers:
            blocks.append(("ol", numbers[:]))
            numbers = []

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line:
            flush_paragraph()
            flush_bullets()
            flush_numbers()
            continue
        if line.startswith("# "):
            flush_paragraph()
            flush_bullets()
            flush_numbers()
            blocks.append(("h1", line[2:].strip()))
            continue
        if line.startswith("## "):
            flush_paragraph()
            flush_bullets()
            flush_numbers()
            blocks.append(("h2", line[3:].strip()))
            continue
        if line.startswith("- "):
            flush_paragraph()
            flush_numbers()
            bullets.append(line[2:].strip())
            continue
        numbered = False
        for i in range(1, 20):
            prefix = f"{i}. "
            if line.startswith(prefix):
                flush_paragraph()
                flush_bullets()
                numbers.append(line[len(prefix) :].strip())
                numbered = True
                break
        if numbered:
            continue
        flush_bullets()
        flush_numbers()
        paragraph.append(line.strip())

    flush_paragraph()
    flush_bullets()
    flush_numbers()
    return blocks


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "kicker": ParagraphStyle(
            "Kicker",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=9,
            leading=12,
            textColor=TEAL,
            tracking=1.2,
            spaceAfter=4,
        ),
        "title": ParagraphStyle(
            "DocTitle",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=24,
            leading=28,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=11,
            leading=15,
            textColor=MUTED,
            spaceAfter=14,
        ),
        "h2": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=13.5,
            leading=17,
            textColor=NAVY,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=15,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10.2,
            leading=14.2,
            textColor=INK,
        ),
        "mark": ParagraphStyle(
            "BulletMark",
            parent=base["Normal"],
            fontName="ZapfDingbats",
            fontSize=7,
            leading=14.2,
            textColor=TEAL,
            alignment=TA_CENTER,
        ),
        "num": ParagraphStyle(
            "NumberMark",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=10.2,
            leading=14.2,
            textColor=NAVY,
            alignment=TA_RIGHT,
        ),
        "panel": ParagraphStyle(
            "Panel",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10.4,
            leading=14.8,
            textColor=INK,
            alignment=TA_JUSTIFY,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def draw_page(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 8 * mm, width, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, height - 9.4 * mm, width, 1.4 * mm, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 12 * mm, width, 1.1 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(18 * mm, 5 * mm, "Education ERP  |  Feature Overview")
    canvas.drawRightString(width - 18 * mm, 5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def marked_list(
    items: list[str],
    text_style: ParagraphStyle,
    mark_style: ParagraphStyle,
    marks: list[str],
    mark_width,
) -> Table:
    rows = [
        [Paragraph(esc(mark), mark_style), Paragraph(esc(item), text_style)]
        for mark, item in zip(marks, items)
    ]
    table = Table(rows, colWidths=[mark_width, 174 * mm - mark_width])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 3),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2),
            ]
        )
    )
    table.spaceAfter = 8
    return table


def bullet_list(items: list[str], styles: dict[str, ParagraphStyle]) -> Table:
    return marked_list(
        items,
        styles["bullet"],
        styles["mark"],
        ["l"] * len(items),
        5 * mm,
    )


def numbered_list(items: list[str], styles: dict[str, ParagraphStyle]) -> Table:
    return marked_list(
        items,
        styles["bullet"],
        styles["num"],
        [f"{index}." for index in range(1, len(items) + 1)],
        8 * mm,
    )


def panel(text: str, style: ParagraphStyle, background: colors.Color) -> Table:
    table = Table([[Paragraph(esc(text), style)]], colWidths=[174 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("BOX", (0, 0), (-1, -1), 0.4, TEAL),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def build() -> None:
    styles = make_styles()
    blocks = parse_markdown(SOURCE)
    story: list = []
    section: list = []

    def flush_section() -> None:
        if section:
            story.append(KeepTogether(section[:]))
            section.clear()

    first_h1 = True
    for kind, payload in blocks:
        if kind == "h1":
            flush_section()
            if first_h1:
                story.append(Paragraph("CLIENT BRIEFING", styles["kicker"]))
                story.append(Paragraph(esc(str(payload)), styles["title"]))
                first_h1 = False
            else:
                section.append(Paragraph(esc(str(payload)), styles["h2"]))
        elif kind == "h2":
            flush_section()
            section.append(Paragraph(esc(str(payload)), styles["h2"]))
        elif kind == "p":
            text = str(payload)
            if text.startswith("This document summarizes"):
                story.append(Paragraph(esc(text), styles["subtitle"]))
            elif text.startswith("The application has a strong") or text.startswith(
                "Education ERP helps institutions"
            ):
                flush_section()
                story.append(panel(text, styles["panel"], ACCENT_BG))
                story.append(Spacer(1, 6))
            elif text.startswith("It is built for real institutional"):
                flush_section()
                story.append(panel(text, styles["panel"], PANEL))
                story.append(Spacer(1, 6))
            elif section:
                section.append(Paragraph(esc(text), styles["body"]))
            else:
                story.append(Paragraph(esc(text), styles["body"]))
        elif kind == "ul":
            flush_section()
            story.append(bullet_list(list(payload), styles))
        elif kind == "ol":
            flush_section()
            story.append(numbered_list(list(payload), styles))
    flush_section()

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Education ERP - Feature Overview",
        author="University ERP",
        subject="Client-facing feature overview for marketing, demos and proposals",
    )
    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    print(OUTPUT)


if __name__ == "__main__":
    build()
