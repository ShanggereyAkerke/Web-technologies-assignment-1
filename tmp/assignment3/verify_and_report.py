"""Build-time verification and draft report; never loaded by the website."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import base64
import hashlib
import json
import re
import textwrap
from PIL import Image, ImageDraw, ImageFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'assignment-3'
OUT = ROOT / 'output' / 'assignment-3'
SHOTS = SITE / 'docs' / 'code-excerpts'
SHOTS.mkdir(parents=True, exist_ok=True)

class Page(HTMLParser):
    def __init__(self, file):
        super().__init__()
        self.file, self.ids, self.elements, self.refs = file, set(), [], []
        self.footer = False
        self.footer_text = ''
        self.feed(file.read_text(encoding='utf-8-sig'))
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.elements.append((tag, a))
        if tag == 'script': assert a.get('src') == 'vendor/bootstrap.bundle.min.js'
        assert not any(k.startswith('on') for k in a), f'Inline event handler in {self.file}'
        if tag == 'footer': self.footer = True
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate ID {a["id"]}'
            self.ids.add(a['id'])
        if tag == 'img': assert a.get('alt'), f'Missing alt in {self.file}'
        for key in ('href', 'src', 'action'):
            if a.get(key): self.refs.append(a[key])
    def handle_endtag(self, tag):
        if tag == 'footer': self.footer = False
    def handle_data(self, data):
        if self.footer: self.footer_text += data

pages = {p.name: Page(p) for p in SITE.glob('*.html')}
assert len(pages) == 5
checks = []
for name, page in pages.items():
    for person in ('Asankhan Shyngys', 'Shangerey Akerke'):
        assert person in page.footer_text, f'Missing team member in {name}'
    for ref in page.refs:
        url = urlsplit(ref)
        assert url.scheme not in ('javascript', 'data')
        if url.scheme or url.netloc: continue
        target = page.file.parent / unquote(url.path) if url.path else page.file
        assert target.exists(), f'Missing file: {name}: {ref}'
        if url.fragment and target.suffix == '.html':
            assert url.fragment in pages[target.name].ids, f'Missing anchor: {name}: {ref}'
    for tag, attrs in page.elements:
        if tag == 'label': assert attrs.get('for') in page.ids
        for ar in ('aria-describedby', 'aria-labelledby'):
            for value in attrs.get(ar, '').split(): assert value in page.ids
    checks.append(f'{name}: references, anchors, labels, image alternatives and both footer names verified; no inline events.')

study = pages['media-queries.html']
assert not any('bootstrap' in r for r in study.refs)
assert sum(tag == 'article' for tag, a in study.elements) == 3
main_css = (SITE / 'css/site.css').read_text()
study_css = (SITE / 'css/media-queries.css').read_text()
for css in (main_css, study_css):
    assert css.count('{') == css.count('}')
assert not re.search(r'(?m)^\s*(margin|padding)(-[a-z]+)?\s*:', main_css)
assert not re.search(r'[{;]\s*(margin|padding)(-[a-z]+)?\s*:', main_css)
assert 'repeat(2, minmax(0, 1fr))' in study_css
assert 'repeat(3, minmax(0, 1fr))' in study_css
assert '@media (min-width: 768px)' in study_css
assert '@media (min-width: 992px)' in study_css
checks.append('Pure-CSS study: exactly three cards, no Bootstrap import, explicit 1/2/3 columns and three typography ranges.')
checks.append('Main theme has no custom margin/padding declarations; Bootstrap utilities control spacing.')

about = pages['about.html']
indicators = [a for tag, a in about.elements if 'data-bs-slide-to' in a]
slides = [a for tag, a in about.elements if tag == 'figure' and 'carousel-item' in a.get('class', '').split()]
assert len(indicators) == len(slides) == 9
assert [a['data-bs-slide-to'] for a in indicators] == list(map(str, range(9)))
assert sum('active' in a.get('class', '').split() for a in slides) == 1
assert sum(a.get('aria-current') == 'true' for a in indicators) == 1
assert {a['data-bs-slide'] for t, a in about.elements if 'data-bs-slide' in a} == {'prev', 'next'}
for t, a in about.elements:
    if 'data-bs-target' in a: assert a['data-bs-target'][1:] in about.ids
assert len({a['src'] for t, a in about.elements if t == 'img'}) == 9
checks.append('Lookbook: nine images and slide indicators, one active slide, matching Bootstrap targets, Previous/Next controls.')
for name in ('index.html', 'collection.html', 'about.html', 'contact.html'):
    page = pages[name]
    assert any(t == 'button' and a.get('data-bs-toggle') == 'collapse' and a.get('data-bs-target') == '#main-navigation' for t, a in page.elements)
    assert sum(t == 'script' for t, a in page.elements) == 1
    assert 'main-navigation' in page.ids
    assert 'vendor/bootstrap.min.css' in page.refs
    assert any('container' in a.get('class', '').split() for t, a in page.elements)
    for t, a in page.elements:
        if t == 'button': assert 'btn' in a.get('class', '').split() or 'navbar-toggler' in a.get('class', '') or 'data-bs-slide-to' in a
checks.append('Four main pages: local Bootstrap CSS and bundle, containers, standard Collapse navbar and styled buttons.')

digest = base64.b64encode(hashlib.sha384((SITE / 'vendor/bootstrap.min.css').read_bytes()).digest()).decode()
assert digest == 'sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB', digest
checks.append('Bootstrap 5.3.8 CSS matches the SHA-384 integrity hash in official documentation.')
js_digest = base64.b64encode(hashlib.sha384((SITE / 'vendor/bootstrap.bundle.min.js').read_bytes()).digest()).decode()
assert js_digest == 'FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI'
checks.append('Bootstrap 5.3.8 JavaScript bundle matches the official SHA-384 hash.')

def luminance(h):
    rgb = [int(h[i:i+2], 16)/255 for i in (0,2,4)]
    rgb = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(a*b for a,b in zip(rgb, (.2126,.7152,.0722)))
ratios = {}
for label,fg,bg in [('body','34282a','fbf6ee'),('secondary','655752','f0e6dd'),('primary button','ffffff','743e4b'),('outline button','743e4b','fbf6ee')]:
    a,b=sorted((luminance(fg),luminance(bg)))
    ratios[label] = round((b+.05)/(a+.05),2)
    assert ratios[label] >= 4.5
checks.append('Core normal-text colour pairs exceed 4.5:1 contrast: ' + str(ratios))
result = {'scope': 'Source-level checks only; not browser execution', 'passed': checks, 'pending': ['Real browser responsive and keyboard tests', 'Genuine webpage screenshots', 'Commit/push and verified deployment URL', 'Both members LMS submission and defense']}
(SITE / 'docs' / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')

tasks = [
 ('1', 'Responsive typography', 'media-queries.html + css/media-queries.css', 'css/media-queries.css', '@media (min-width: 768px)', 18,
  ['Build the exercise with semantic headings, paragraphs and a viewport meta tag.', 'Use small base sizes on phones: 36px h1 and 16px paragraph text.', 'At 768px use 48px headings and 18px paragraphs; at 992px use 64px headings and 20px paragraphs.'],
  'Implemented in source. Check the 767/768px and 991/992px boundaries in a real browser.'),
 ('2', 'Three-card group without Bootstrap', 'media-queries.html + css/media-queries.css', 'css/media-queries.css', '.study-cards {', 8,
  ['Keep this page independent: its only stylesheet is media-queries.css.', 'Use one CSS Grid column by default, two at 768px, and three at 992px.', 'Give each of the three cards an image, title, description and working collection link.'],
  'Implemented. This page is the deliberate exception to Task 4, because Task 2 expressly prohibits Bootstrap.'),
 ('3', 'Bootstrap 12-column grid', 'Home, Collection, About and Contact', 'index.html', '<!-- Task 3: two', 12,
  ['Load the unmodified official Bootstrap 5.3.8 CSS from the local vendor folder.', 'Wrap content in container and row. Home has a two-column col-lg-6 section and a three-column col-lg-4 section.', 'Use col-12, col-sm-6, col-md-6 and col-lg-* where each content layout requires them.'],
  'Implemented. Grid columns stack on smaller screens through Bootstrap CSS.'),
 ('4', 'Bootstrap spacing utilities', 'All four main pages', 'collection.html', '<section id="size-guide"', 5,
  ['Use Bootstrap m-*, p-*, g-* and gap-* classes in HTML.', 'Apply responsive examples such as px-sm-2, p-md-4, p-lg-5 and mt-lg-4.', 'Keep custom margin and padding declarations out of site.css; use it only for theme, images, typography and interactions.'],
  'Automated source check confirms no custom margin or padding declarations in site.css.'),
 ('5', 'Responsive navigation bar', 'All four main pages', 'index.html', '<button class="navbar-toggler', 7,
  ['Use navbar, navbar-expand-lg, navbar-nav, nav-link and bg-light classes with four page links.', 'Use button.navbar-toggler with data-bs-toggle=collapse and a matching collapse.navbar-collapse target.', 'Show the full desktop navigation from the lg breakpoint, and mark the current page with aria-current.'],
  'Uses the standard Bootstrap Collapse plugin. Source wiring checked; browser interaction testing remains pending.'),
 ('6', 'Buttons and button group', 'Home, Collection and Contact', 'collection.html', '<!-- Task 6:', 3,
  ['Use btn-primary, btn-secondary and btn-outline-primary instead of the previous custom button class.', 'Demonstrate btn-lg, btn-sm and a disabled submit state; use real links for navigation.', 'Group Collection section links in btn-group. The Contact reset button is a native functional button.'],
  'Implemented. No inert fake filters, ordering service or custom script is included.'),
 ('7', 'Nine-image carousel', 'About page lookbook', 'about.html', '<div id="lookbook-carousel"', 8,
  ['Place nine distinct images inside Bootstrap carousel-inner and carousel-item markup.', 'Use nine data-bs-slide-to indicator buttons, one active slide, and Previous/Next buttons targeting the carousel ID.', 'Use the official Bootstrap Carousel plugin with descriptive image alternatives and captions. Disable automatic playback with data-bs-interval=false.'],
  'Uses the standard Bootstrap Carousel plugin. Selection, swipe and keyboard behavior need real browser verification.'),
 ('8', 'Bootstrap cards', 'Home and Collection', 'index.html', '<div class="card-group', 10,
  ['Create three Home articles with card, card-img-top, card-body, card-title and card-text classes.', 'Group them using card-group as required by the assignment.', 'Reuse the visual treatment for four Collection cards in Bootstrap columns and two team cards on About.'],
  'Implemented. Images, titles and descriptions are present on all three Home cards.'),
 ('9', 'Responsive form', 'Contact page', 'contact.html', '<div class="row g-3 mb-3">', 10,
  ['Use form-control for text/email/textarea, form-select for topics, and input-group for the email field.', 'Use form-check inputs for radio choices and a checkbox. Associate every field with a visible label.', 'Use responsive Bootstrap columns, required attributes and length constraints. Keep sending disabled and explain the demo status.'],
  'Implemented. There is no backend; the clear-form button uses native type=reset.'),
 ('10', 'Accessibility', 'All pages', 'css/site.css', ':focus-visible', 8,
  ['Use semantic nav, main, section, article, footer, form and fieldset elements.', 'Add image alternatives, labelled controls, skip links, current-page indicators and visible focus.', 'Use button controls and Bootstrap-managed menu state, respect reduced-motion preferences, and verify the main colour pairs numerically.'],
  'Source and core contrast checks passed. Keyboard order, disclosure and slider operation still need real browser testing.')
]

font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 17)
titlefont = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 20)
def code_image(number, source, marker, count):
    lines = (SITE/source).read_text(encoding='utf-8-sig').splitlines()
    start = next(i for i,v in enumerate(lines) if marker in v)
    rendered=[]
    for n,line in enumerate(lines[start:start+count], start+1):
        parts = textwrap.wrap(line, width=106, replace_whitespace=False, drop_whitespace=False) or ['']
        rendered.append(f'{n:3}  {parts[0]}')
        rendered.extend('     '+p for p in parts[1:])
    im=Image.new('RGB',(1200,75+25*len(rendered)), '#20202a')
    draw=ImageDraw.Draw(im)
    draw.text((24,18),f'{source} | Actual source excerpt',font=titlefont,fill='#f4dac8')
    for i,line in enumerate(rendered): draw.text((24,60+i*25),line,font=font,fill='#f4f2ef')
    path=SHOTS/f'task-{number}.png'
    im.save(path)
    return path

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle', fontName='Helvetica-Bold',fontSize=30,leading=35,textColor=HexColor('#743e4b'),spaceAfter=24))
styles.add(ParagraphStyle(name='ReportBody', fontName='Helvetica',fontSize=10.5,leading=16,spaceAfter=12))
styles.add(ParagraphStyle(name='Note',fontName='Helvetica',fontSize=9,leading=12,textColor=HexColor('#655752'),spaceAfter=8))
story=[]
def para(text, style='ReportBody'): story.append(Paragraph(text, styles[style]))
para('FORYOU<br/>Assignment 3', 'ReportTitle')
para('Media Queries + Bootstrap Grid', 'Heading1')
para('DRAFT - browser screenshots and deployment URL pending', 'Heading2')
para('Team FORYOU | Group SE-2504<br/>Asankhan Shyngys - Home and Collection<br/>Shangerey Akerke - About and Contact')
para('Objective', 'Heading2')
para('Build a responsive clothing-store concept using explicit media queries and the Bootstrap 12-column grid. Demonstrate cards, spacing utilities, navigation, buttons, a nine-image lookbook, forms and accessibility with HTML, CSS and the authorized official Bootstrap JavaScript bundle.')
para('Scope and honest compliance', 'Heading2')
para('The four main pages use official Bootstrap 5.3.8 CSS, included locally. A fifth page demonstrates Tasks 1 and 2 without Bootstrap. The four main pages load the official Bootstrap JavaScript bundle locally for the standard Collapse and Carousel plugins. No custom JavaScript is needed. The independent media-query exercise remains HTML and CSS only.')
para('This report includes images of actual source excerpts. It does not contain fabricated webpage screenshots. The environment blocked the browser local-file preview, so genuine rendered screenshots and functional browser checks remain pending. The deployment URL is not yet available.')
para('Source: Web Assignment 3 Media Queries + Bootstrap Grid.pdf, supplied by the user.', 'Note')
story.append(PageBreak())
for number,title,where,source,marker,count,steps,status in tasks:
    para(f'Task {number}', 'Heading2')
    para(title,'ReportTitle')
    para('Evidence location: '+where,'Note')
    for i,step in enumerate(steps,1): para(f'<b>{i}.</b> {step}')
    image_path=code_image(number,source,marker,count)
    with Image.open(image_path) as im: w,h=im.size
    scale=min(475/w,275/h)
    story.append(PDFImage(str(image_path),width=w*scale,height=h*scale))
    story.append(Spacer(1,14))
    para('<b>Verification / limitation:</b> '+status)
    para('Webpage screenshot: pending a real browser capture. Capture the relevant page at phone, tablet and desktop widths before final submission.','Note')
    story.append(PageBreak())
para('Verification &amp; submission', 'ReportTitle')
for check in checks: para('- '+check,'Note')
para('Still required before submission','Heading2')
para('1. Verify the Bootstrap menu and all nine carousel indicators, including Previous/Next wraparound.<br/>2. Test all pages at 375px, 768px and 1440px, including breakpoint boundaries.<br/>3. Capture genuine webpage screenshots and add them to this report.<br/>4. Commit and push the approved site, deploy through GitHub Pages or Netlify, and verify the actual URL.<br/>5. Insert that URL below, export the final report and regenerate the ZIP.<br/>6. Both members submit the report and ZIP and defend the work by the LMS deadline.')
para('<b>Verified deployed URL:</b> PENDING - not deployed.')
para('Reflection draft for team review','Heading2')
para('Media queries provide direct control over typography and card counts. Bootstrap provides consistent layout and spacing across the main pages. Keeping the pure-CSS study separate resolves the different task constraints. Bootstrap handles menu and carousel interaction through HTML data attributes and its official JavaScript bundle. This separates our layout and theme work from the supplied component behavior.')
para('Official references','Heading2')
para('<br/>'.join(['https://getbootstrap.com/docs/5.3/getting-started/introduction/','https://getbootstrap.com/docs/5.3/layout/grid/','https://getbootstrap.com/docs/5.3/utilities/spacing/','https://getbootstrap.com/docs/5.3/components/carousel/','https://getbootstrap.com/docs/5.3/components/card/']), 'Note')

def page_footer(canvas,doc):
    canvas.setStrokeColor(HexColor('#d8c3c1'));canvas.line(42,40,553,40)
    canvas.setFillColor(HexColor('#655752'));canvas.setFont('Helvetica',8)
    canvas.drawString(42,27,'FORYOU | SE-2504 | Assignment 3 | DRAFT')
    canvas.drawRightString(553,27,str(doc.page))
pdf=OUT/'FORYOU-Assignment-3-Report-DRAFT.pdf'
SimpleDocTemplate(str(pdf),pagesize=(595,842),rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=58).build(story,onFirstPage=page_footer,onLaterPages=page_footer)
document=pdfium.PdfDocument(str(pdf))
thumbs=[]
for i in range(len(document)):
    pil=document[i].render(scale=0.65).to_pil().convert('RGB')
    pil.save(OUT/f'report-page-{i+1}.png')
    thumbs.append(pil)
sheet=Image.new('RGB',(thumbs[0].width*3, (thumbs[0].height+24)*((len(thumbs)+2)//3)), '#dedede')
d=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=(i%3)*im.width;y=(i//3)*(im.height+24)
    sheet.paste(im,(x,y));d.text((x+8,y+im.height+4),f'Page {i+1}',fill='black')
sheet.save(OUT/'report-contact-sheet.png')
print(json.dumps({'checks':len(checks),'report_pages':len(document),'pdf':str(pdf),'pending':result['pending']},indent=2))
