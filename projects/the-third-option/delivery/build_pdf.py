#!/usr/bin/env python3
import os, re
from reportlab.lib.pagesizes import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, NextPageTemplate)
from reportlab.lib.units import inch as INCH

BASE = "/home/user/book-genesis-v4/projects/the-third-option/manuscript/chapters"
OUT = "/home/user/book-genesis-v4/projects/the-third-option/delivery/The-Third-Option-draft1.pdf"

ORDER = ["chapter-00-introduction","chapter-01-break-the-cycle","chapter-02-know-your-core",
    "chapter-03-choose-what-fits","chapter-04-start-before-youre-ready","chapter-05-learn-whats-yours",
    "chapter-06-the-messy-middle","chapter-07-own-what-you-built","chapter-08-automate-what-you-can",
    "chapter-09-keep-the-momentum","chapter-10-run-the-loop","appendix-fit-audit","chapter-zz-notes",
    "back-matter-about-the-author"]

PAGE_W, PAGE_H = 6*INCH, 9*INCH
MARGIN = 0.72*INCH

def inline(t):
    t = t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    return t

def load_chapter(name):
    with open(os.path.join(BASE, name+".md")) as f:
        text = f.read()
    lines = text.split('\n')
    title = next((l[2:].strip() for l in lines if l.startswith('# ')), name)
    # body = after the first '---' (which follows the italic version line), before '## Draft notes'
    body_lines, started = [], False
    for l in lines:
        if not started:
            if l.strip() == '---':
                started = True
            continue
        if l.startswith('## Draft notes'):
            break
        body_lines.append(l)
    return title, '\n'.join(body_lines).strip()

# ---- styles ----
BODY = ParagraphStyle('body', fontName='Times-Roman', fontSize=11.5, leading=16.5,
                      alignment=TA_LEFT, spaceAfter=7, firstLineIndent=0)
BODY_INDENT = ParagraphStyle('bodyind', parent=BODY, firstLineIndent=16)
H2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=13, leading=17,
                    spaceBefore=16, spaceAfter=8, textColor='#5C1A3B')
H3 = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11.5, leading=15,
                    spaceBefore=12, spaceAfter=6, textColor='#5C1A3B')
QUOTE = ParagraphStyle('quote', parent=BODY, fontName='Times-Italic', leftIndent=24,
                       rightIndent=12, alignment=TA_LEFT, spaceAfter=3, textColor='#2A1220')
LIST = ParagraphStyle('list', parent=BODY, leftIndent=22, firstLineIndent=-14, alignment=TA_LEFT, spaceAfter=4)
CH_NUM = ParagraphStyle('chnum', fontName='Helvetica-Bold', fontSize=11, leading=14,
                        alignment=TA_LEFT, textColor='#FF7FB0', spaceAfter=6)
CH_TITLE = ParagraphStyle('chtitle', fontName='Times-Bold', fontSize=22, leading=26,
                          alignment=TA_LEFT, textColor='#5C1A3B', spaceAfter=24)

def build_blocks(body):
    flow = []
    blocks = re.split(r'\n\s*\n', body)
    first_para = True
    for b in blocks:
        s = b.strip()
        if not s or s == '---':
            continue
        if s.startswith('### '):
            flow.append(Paragraph(inline(s[4:].strip()), H3)); first_para = True; continue
        if s.startswith('## '):
            flow.append(Paragraph(inline(s[3:].strip()), H2)); first_para = True; continue
        nonempty = [l for l in s.split('\n') if l.strip()]
        if nonempty and all(l.lstrip().startswith('>') for l in nonempty):
            for l in nonempty:
                q = l.lstrip()[1:].strip()
                if q:
                    flow.append(Paragraph(inline(q), QUOTE))
            first_para = True; continue
        if nonempty and all(re.match(r'^(\d+\.|-)\s', l.strip()) for l in nonempty):
            for l in nonempty:
                l = l.strip()
                m = re.match(r'^(\d+)\.\s(.*)', l)
                if m:
                    flow.append(Paragraph(f"{m.group(1)}.&nbsp;&nbsp;{inline(m.group(2))}", LIST))
                else:
                    flow.append(Paragraph(f"&bull;&nbsp;&nbsp;{inline(l[2:])}", LIST))
            first_para = True; continue
        # body paragraph: join hard-wrapped lines
        para = ' '.join(l.strip() for l in s.split('\n'))
        style = BODY if first_para else BODY_INDENT
        flow.append(Paragraph(inline(para), style))
        first_para = False
    return flow

# ---- doc ----
def footer(canvas, doc):
    canvas.saveState()
    if doc.page > 2:
        canvas.setFont('Times-Roman', 9)
        canvas.setFillColor('#5C1A3B')
        canvas.drawCentredString(PAGE_W/2, 0.4*INCH, str(doc.page - 2))
    canvas.restoreState()

frame = Frame(MARGIN, MARGIN, PAGE_W-2*MARGIN, PAGE_H-2*MARGIN, id='main')
doc = BaseDocTemplate(OUT, pagesize=(PAGE_W, PAGE_H),
                      leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
                      title="The Third Option", author="Jena Crossland Brooks")
doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=footer)])

story = []
# Title page
story.append(Spacer(1, 1.6*INCH))
story.append(Paragraph("The Third Option", ParagraphStyle('tt', fontName='Times-Bold',
             fontSize=34, leading=40, alignment=TA_CENTER, textColor='#5C1A3B')))
story.append(Spacer(1, 0.25*INCH))
story.append(Paragraph("How to Choose, Build, and Own a Life That Fits",
             ParagraphStyle('ts', fontName='Times-Italic', fontSize=15, leading=20,
             alignment=TA_CENTER, textColor='#2A1220')))
story.append(Spacer(1, 1.4*INCH))
story.append(Paragraph("Jena Crossland Brooks", ParagraphStyle('ta', fontName='Helvetica',
             fontSize=13, leading=18, alignment=TA_CENTER, textColor='#2A1220')))
story.append(Spacer(1, 0.15*INCH))
story.append(Paragraph("Draft 2", ParagraphStyle('td', fontName='Helvetica', fontSize=10,
             leading=14, alignment=TA_CENTER, textColor='#FF7FB0')))
story.append(PageBreak())

# Dedication page
DED_STYLE = ParagraphStyle('ded', fontName='Times-Italic', fontSize=13, leading=20,
                           alignment=TA_CENTER, textColor='#2A1220', spaceAfter=14)
with open(os.path.join(BASE, "..", "front-matter-dedication.md")) as f:
    ded_lines = [l.strip() for l in f.read().split('\n')
                 if l.strip() and not l.startswith('#')]
story.append(Spacer(1, 2.6*INCH))
for dl in ded_lines:
    story.append(Paragraph(inline(dl), DED_STYLE))
story.append(PageBreak())

for name in ORDER:
    title, body = load_chapter(name)
    # split "Chapter N · Title" into small-caps number line + title
    if '·' in title:
        num, ttl = [x.strip() for x in title.split('·', 1)]
        story.append(Spacer(1, 0.3*INCH))
        story.append(Paragraph(num.upper(), CH_NUM))
        story.append(Paragraph(inline(ttl), CH_TITLE))
    else:
        story.append(Spacer(1, 0.3*INCH))
        story.append(Paragraph(inline(title), CH_TITLE))
    story.extend(build_blocks(body))
    story.append(PageBreak())

doc.build(story)
print("wrote", OUT)
# quick page count
import fitz
print("pages:", fitz.open(OUT).page_count)
