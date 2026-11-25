from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os

out = "./glacier_aftershave_labels.pdf"
W, H = A4
c = canvas.Canvas(out, pagesize=A4)

navy = HexColor("#233B50")
slate = HexColor("#607E91")
ice = HexColor("#A9C3D1")
paper = HexColor("#F7F8F6")
line = HexColor("#B8C9D2")

label_w, label_h = 40 * mm, 45 * mm
gap = 12 * mm
total_w = 2 * label_w + gap
x1 = (W - total_w) / 2
x2 = x1 + label_w + gap
y = H - 65 * mm


def centered(txt, cx, yy, font="Helvetica", size=7, color=navy):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(cx, yy, txt)


def label_frame(x, y):
    c.setFillColor(paper)
    c.setStrokeColor(line)
    c.setLineWidth(0.55)
    c.roundRect(x, y, label_w, label_h, 2.2 * mm, fill=1, stroke=1)
    # small corner registration accents
    c.setStrokeColor(ice)
    c.setLineWidth(0.8)
    inset = 2.2 * mm
    arm = 2.2 * mm
    for xx, sx in [(x + inset, 1), (x + label_w - inset, -1)]:
        for yy, sy in [(y + inset, 1), (y + label_h - inset, -1)]:
            c.line(
                xx,
                yy,
                xx + sx * arm,
                yy,
            )
            c.line(
                xx,
                yy,
                xx,
                yy + sy * arm,
            )


def wide_line(y):
    c.setStrokeColor(line)
    c.setLineWidth(0.45)
    c.line(
        x2 + 4 * mm,
        y,
        x2 + label_w - 4 * mm,
        y,
    )


# Front label
label_frame(x1, y)
cx = x1 + label_w / 2
centered("GLACIER", cx, y + label_h - 10 * mm, "Helvetica-Bold", 14, navy)
c.setStrokeColor(ice)
c.setLineWidth(0.9)
c.line(
    x1 + 8 * mm,
    y + label_h - 13 * mm,
    x1 + label_w - 8 * mm,
    y + label_h - 13 * mm,
)
centered("INTENSE COOLING", cx, y + label_h - 19 * mm, "Helvetica-Bold", 7, slate)
centered("MENTHOLATED AFTERSHAVE", cx, y + label_h - 23 * mm, "Helvetica", 6, navy)
# Minimal stylized glacier motif, centered
motif_y = y + 13.5 * mm
c.setStrokeColor(ice)
c.setLineWidth(1.0)
c.line(
    cx - 7 * mm,
    motif_y,
    cx - 3 * mm,
    motif_y + 5 * mm,
)
c.line(
    cx - 3 * mm,
    motif_y + 5 * mm,
    cx,
    motif_y + 1.5 * mm,
)
c.line(
    cx,
    motif_y + 1.5 * mm,
    cx + 3 * mm,
    motif_y + 6 * mm,
)
c.line(
    cx + 3 * mm,
    motif_y + 6 * mm,
    cx + 7 * mm,
    motif_y,
)
c.line(
    cx - 7 * mm,
    motif_y,
    cx + 7 * mm,
    motif_y,
)
c.setStrokeColor(line)
c.setLineWidth(0.45)
c.line(
    x1 + 8 * mm,
    y + 9.5 * mm,
    x1 + label_w - 8 * mm,
    y + 9.5 * mm,
)
centered("HERBAL FORMULA - NO ADDED PERFUME", cx, y + 6.2 * mm, "Helvetica", 5, slate)
centered("106 ml", cx, y + 3.5 * mm, "Helvetica-Bold", 6, navy)

# Back label
label_frame(x2, y)
cx2 = x2 + label_w / 2

left = x2 + 4 * mm
right = x2 + label_w - 4 * mm
yy = y + label_h - 16 * mm
yy = y + 40 * mm

c.setFillColor(slate)
c.setFont("Helvetica-Bold", 5.0)
c.drawString(left, yy, "Batch #002")
c.drawRightString(right, yy, "2026-11-22")

yy -= 1.5 * mm
wide_line(yy)

yy -= 2.4 * mm
c.setFillColor(navy)
c.setFont("Helvetica-Bold", 5.5)
c.drawString(left, yy, "INGREDIENTS")

yy -= 2.8 * mm
c.setFillColor(navy)
c.setFont("Helvetica", 5.0)
yyTmp = yy
for line_txt in [
    ["Alcohol Denat.", "40.7% v/v"],
    ["Rosa Damascena Water", "37.7% v/v"],
    ["Salix Alba Water", "18.9% v/v"],
    ["Aqua", "1.7% v/v"],
    ["Glycerin", "1% v/v"],
    ["Menthol", "0.85% w/v"],
]:
    c.drawString(left, yy, line_txt[0])
    c.drawRightString(right, yy, line_txt[1])
    yy -= 2.4 * mm

yy -= 0.5 * mm
c.setFillColor(slate)
c.setFont("Helvetica-Bold", 5.2)
c.drawString(left, yy, "CAUTION")
yy -= 2.7 * mm
c.setFillColor(navy)
c.setFont("Helvetica", 4.55)
for line_txt in [
    "External use only. Avoid eyes and mucous",
    "membranes. Flammable; keep away from heat",
    "and flames. Do not apply to broken skin.",
    "Keep out of reach of children.",
    "Store below 30°C, away from sunlight.",
]:
    c.drawString(left, yy, line_txt)
    yy -= 2.3 * mm

yy -= 1 * mm
c.setStrokeColor(line)
c.setLineWidth(0.45)
wide_line(y + 5.2 * mm)

c.setFillColor(slate)
c.setFont("Helvetica-Bold", 4.6)
c.drawString(left, yy, "PERSONAL BATCH")
c.drawRightString(right, yy, "NOT FOR SALE")

# Print instruction and 50 mm calibration line
c.setFillColor(HexColor("#555555"))
c.setFont("Helvetica", 8)
c.drawCentredString(
    W / 2, y - 12 * mm, "Print at 100% / Actual size. Do not use “Fit to page”."
)
c.setStrokeColor(HexColor("#555555"))
c.setLineWidth(0.6)
cal_y = y - 23 * mm
c.line(
    W / 2 - 25 * mm,
    cal_y,
    W / 2 + 25 * mm,
    cal_y,
)
c.line(
    W / 2 - 25 * mm,
    cal_y - 1.5 * mm,
    W / 2 - 25 * mm,
    cal_y + 1.5 * mm,
)
c.line(
    W / 2 + 25 * mm,
    cal_y - 1.5 * mm,
    W / 2 + 25 * mm,
    cal_y + 1.5 * mm,
)
c.setFont("Helvetica", 6.5)
c.drawCentredString(W / 2, cal_y - 4 * mm, "Calibration line: 50 mm")

c.save()
print(out, os.path.getsize(out))
