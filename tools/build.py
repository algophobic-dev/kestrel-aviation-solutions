#!/usr/bin/env python3
"""Builds the Kestrel Aviation Solutions site. Run: python3 tools/build.py

Page bodies are in tools/pages/. The product cards come from products.json: add one entry there to list a new product.
Writes index.html, products.html, about.html, contact.html, 404.html, sitemap.xml and robots.txt."""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://kestrelaviation.tech"
EFB = "https://efb.kestrelaviation.tech"

PAGES = {
    "index": ("Kestrel Aviation Solutions · Aviation software for pilots",
              "Kestrel Aviation Solutions builds software that makes flying simpler and more affordable, for pilots, students, instructors and anyone in aviation."),
    "products": ("Products · Kestrel Aviation Solutions",
                 "Software from Kestrel Aviation Solutions, including Kestrel EFB, a free electronic flight bag for Mac, Windows, iPad and iPhone."),
    "about": ("About · Kestrel Aviation Solutions", "About Kestrel Aviation Solutions and the software we build for aviation."),
    "contact": ("Contact · Kestrel Aviation Solutions", "Contact Kestrel Aviation Solutions, or report a problem with one of our products."),
    "404": ("Page not found · Kestrel Aviation Solutions", "There is no page at this address."),
}
NAV = [("products", "Products"), ("about", "About"), ("contact", "Contact")]
e = lambda s: html.escape(str(s), quote=True)


def url_of(name):
    return "/" if name == "index" else f"/{name}.html"


def product_cards():
    items = json.loads((ROOT / "products.json").read_text())
    cards = []
    for p in items:
        external = lambda u: u.startswith("http")
        links = "".join(
            f'<a class="{"btn" if i == 0 else "link"}" href="{e(l["url"])}">{e(l["label"])}</a>' for i, l in enumerate(p.get("links", [])))
        pic = f'<a class="pic" href="{e(p["url"])}" tabindex="-1" aria-hidden="true"><img src="/{e(p["image"])}" width="1200" height="750" alt="{e(p.get("image_alt", ""))}" loading="lazy"></a>' if p.get("image") else ""
        status = p.get("status", "")
        cards.append(f"""<article class="product">
    {pic}
    <div class="body">
      <div class="top"><h3>{e(p["name"])}</h3>{f'<span class="tag{" on" if status == "Available" else ""}">{e(status)}</span>' if status else ""}</div>
      <p class="summary">{e(p.get("summary", ""))}</p>
      <p class="desc">{e(p.get("description", ""))}</p>
      <div class="acts">{links}</div>
    </div>
  </article>""")
    return f'<div class="products{" one" if len(items) == 1 else ""}">\n  ' + "\n  ".join(cards) + "\n</div>"


def page(name, products):
    title, desc = PAGES[name]
    links = "".join(f'<li{" class=opt" if n == "about" else ""}><a href="{url_of(n)}"{" aria-current=page" if n == name else ""}>{label}</a></li>' for n, label in NAV)
    body = (ROOT / "tools" / "pages" / f"{name}.html").read_text().replace("{{PRODUCTS}}", products)
    canonical = "" if name == "404" else f'\n<link rel="canonical" href="{BASE}{url_of(name)}">'
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#10161a">{canonical}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kestrel Aviation Solutions">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{BASE}{url_of(name)}">
<meta property="og:image" content="{BASE}/img/kestrel-efb.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/icon.svg" type="image/svg+xml">
<link rel="icon" href="/img/icon-180.png" type="image/png" sizes="180x180">
<link rel="apple-touch-icon" href="/img/icon-180.png">
<link rel="stylesheet" href="/css/site.css">
</head>
<body>
<header class="nav">
  <a class="mark" href="/"><img src="/img/icon-180.png" width="28" height="28" alt="">Kestrel Aviation Solutions</a>
  <nav aria-label="Main"><ul>{links}<li><a class="btn sm" href="{EFB}">Kestrel EFB</a></li></ul></nav>
</header>
<main>
{body}
</main>
<footer>
  <div class="in">
    <div>Kestrel Aviation Solutions</div>
    <nav aria-label="Footer"><a href="/products.html">Products</a><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="{EFB}">Kestrel EFB</a></nav>
    <div>© 2026 Kestrel Aviation Solutions</div>
  </div>
</footer>
</body>
</html>
"""
    (ROOT / ("index.html" if name == "index" else f"{name}.html")).write_text(out)


products = product_cards()
for n in PAGES:
    page(n, products)
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                  + "".join(f"  <url><loc>{BASE}{url_of(n)}</loc></url>\n" for n in PAGES if n != "404") + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
print("Built", ", ".join(PAGES), "and sitemap.xml, robots.txt")
