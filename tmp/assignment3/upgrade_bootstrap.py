from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
site = root / 'assignment-3'
for name in ('index.html', 'collection.html', 'about.html', 'contact.html'):
    path = site / name
    html = path.read_text(encoding='utf-8')
    html = html.replace('Bootstrap CSS only; no scripts.', 'Bootstrap CSS and official JavaScript bundle.')
    html = html.replace('Bootstrap navbar styling; native details/summary replaces the JS collapse plugin.', 'Bootstrap navbar with the standard Collapse plugin.')
    start = html.index('      <ul class="navbar-nav d-none')
    end = html.index('      </details>', start) + len('      </details>')
    links = re.search(r'<ul[^>]*>(.*?)</ul>', html[start:end], re.S).group(1)
    html = html[:start] + '''      <button class="navbar-toggler border-dark px-3 py-2" type="button"
              data-bs-toggle="collapse" data-bs-target="#main-navigation"
              aria-controls="main-navigation" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon" aria-hidden="true"></span><span class="ms-2 small">Menu</span>
      </button>
      <div class="collapse navbar-collapse" id="main-navigation">
        <ul class="navbar-nav ms-auto">''' + links + '''</ul>
      </div>''' + html[end:]
    html = html.replace('</body>', '<script src="vendor/bootstrap.bundle.min.js"></script>\n</body>')
    if name == 'about.html':
        start = html.index('<!-- Task 7 adaptation:')
        end = html.index('</fieldset>', start) + len('</fieldset>')
        figures = re.findall(r'<figure class="carousel-item.*?</figure>', html[start:end], re.S)
        figures = [re.sub(r'frame-\d+ ', '', f) for f in figures]
        figures[0] = figures[0].replace('carousel-item ', 'carousel-item active ', 1)
        indicators = '\n'.join(f'    <button type="button" data-bs-target="#lookbook-carousel" data-bs-slide-to="{i}"' + (' class="active" aria-current="true"' if i == 0 else '') + f' aria-label="Slide {i+1} of 9"></button>' for i in range(9))
        html = html[:start] + '''<!-- Task 7: standard Bootstrap Carousel plugin; manual playback. -->
<p id="lookbook-help" class="small text-secondary mb-3">Use the slide indicators or Previous and Next to explore all nine images.</p>
<div id="lookbook-carousel" class="carousel slide" data-bs-interval="false"
     role="region" aria-roledescription="carousel" aria-label="FORYOU lookbook" aria-describedby="lookbook-help">
  <div class="carousel-indicators position-static mb-3" data-bs-theme="dark">
''' + indicators + '''
  </div>
  <div class="carousel-inner bg-soft" aria-live="polite">
''' + '\n'.join(figures) + '''
  </div>
  <div class="d-flex justify-content-between gap-3 mt-3">
    <button class="btn btn-outline-primary px-4" type="button" data-bs-target="#lookbook-carousel" data-bs-slide="prev"><span aria-hidden="true">←</span> Previous</button>
    <button class="btn btn-primary px-4" type="button" data-bs-target="#lookbook-carousel" data-bs-slide="next">Next <span aria-hidden="true">→</span></button>
  </div>
</div>''' + html[end:]
    path.write_text(html, encoding='utf-8')

path = site / 'css/site.css'
css = path.read_text().replace('and CSS-only interaction.', 'and focus styles.')
css = '\n'.join(line for line in css.splitlines() if not any(s in line for s in ('.mobile-menu', '.css-carousel', '.carousel-actions', '#look-')))
css = css.replace('.lookbook-image {', '.carousel-indicators [data-bs-target] { min-height: 44px; background-clip: content-box; }\n.lookbook-image {', 1)
path.write_text(css + '\n')
