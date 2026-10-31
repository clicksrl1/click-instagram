"""Esporta i caroselli di un file HTML in JPEG 1080x1080 e controlla gli errori di impaginazione.

Uso:  python3 bot/render.py <file.html> <cartella_output>

Nel file HTML ogni carosello è un <div class="post" data-id="AAAA-MM-GG_tema">
con dentro le sue <div class="slide"> in ordine. Per ogni carosello vengono
creati <cartella_output>/<data-id>/slide1.jpg ... slideN.jpg.

Controlli automatici (il programma esce con errore se ne trova):
- testo che esce dai bordi della slide o dal margine di sicurezza;
- contatori "k / N" che non corrispondono alla posizione reale della slide;
- caroselli con meno di 2 o più di 10 slide (limite di Instagram).
"""
import io
import json
import os
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

TEXT_SELECTORS = ".tag, .title, .body, .cta-ey, .cta-t, .cta-s, .cta-btn, .cover-eyebrow, .cover-title, .cover-sub, .check-text, .label-text"
SAFE_MARGIN = 18  # px su slide 540: il testo deve restare dentro questo margine

CHECK_JS = """
(args) => {
  const [selectors, margin] = args;
  const out = [];
  document.querySelectorAll('.post').forEach(post => {
    const slides = [...post.querySelectorAll('.slide')];
    const id = post.dataset.id;
    slides.forEach((s, i) => {
      const r = s.getBoundingClientRect();
      s.querySelectorAll(selectors).forEach(el => {
        const e = el.getBoundingClientRect();
        if (e.width === 0 && e.height === 0) return;
        if (e.left < r.left + margin || e.right > r.right - margin ||
            e.top < r.top + margin || e.bottom > r.bottom - margin) {
          out.push(`${id} slide${i+1}: testo fuori margine -> "${el.textContent.trim().slice(0,50)}"`);
        }
        if (el.scrollWidth > el.clientWidth + 2) {
          out.push(`${id} slide${i+1}: parola troppo lunga -> "${el.textContent.trim().slice(0,50)}"`);
        }
      });
      const c = s.querySelector('.slide-counter');
      if (c) {
        const m = c.textContent.match(/(\\d+)\\s*\\/\\s*(\\d+)/);
        if (!m || +m[1] !== i+1 || +m[2] !== slides.length) {
          out.push(`${id} slide${i+1}: contatore "${c.textContent.trim()}" sbagliato (atteso ${i+1} / ${slides.length})`);
        }
      }
    });
    if (slides.length < 2 || slides.length > 10) {
      out.push(`${id}: ${slides.length} slide (Instagram ne accetta da 2 a 10)`);
    }
  });
  return out;
}
"""


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    html_path, out_root = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_context(device_scale_factor=2).new_page()
        page.set_viewport_size({"width": 4000, "height": 1200})
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(1500)

        problems = page.evaluate(CHECK_JS, [TEXT_SELECTORS, SAFE_MARGIN])
        written = []
        for post in page.query_selector_all(".post"):
            post_id = post.get_attribute("data-id")
            folder = os.path.join(out_root, post_id)
            os.makedirs(folder, exist_ok=True)
            for i, slide in enumerate(post.query_selector_all(".slide"), start=1):
                png = slide.screenshot()
                img = Image.open(io.BytesIO(png)).convert("RGB")
                if img.size != (1080, 1080):
                    img = img.resize((1080, 1080), Image.LANCZOS)
                path = os.path.join(folder, f"slide{i}.jpg")
                img.save(path, "JPEG", quality=90, optimize=True)
                written.append(os.path.relpath(path, out_root))
        browser.close()

    print(json.dumps({"slide_create": written, "problemi": problems}, ensure_ascii=False, indent=2))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
