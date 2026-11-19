# Kestrel Aviation Solutions website

The company website at https://kestrelaviation.tech. Plain HTML hosted on GitHub Pages. There is nothing to build on GitHub.

## Add or change a product

Edit `products.json`. Each product is one entry:

```json
{
  "name": "Product name",
  "status": "Available",
  "summary": "One short line.",
  "description": "Two or three sentences.",
  "url": "https://product.kestrelaviation.tech",
  "image": "img/product.jpg",
  "image_alt": "What the picture shows",
  "links": [{ "label": "Visit Product name", "url": "https://product.kestrelaviation.tech" }]
}
```

Put the picture in `img/` (1200 by 750 px works best), then rebuild:

```bash
python3 tools/build.py
```

## Change a page

Page bodies are in `tools/pages/`. The header, footer and page tags are in `tools/build.py`. Rebuild after any change. The build also writes `sitemap.xml` and `robots.txt`.

## Hosting

`CNAME` holds the custom domain. In the repository, open **Settings > Pages**, set the source to the `main` branch and the root folder, enter `kestrelaviation.tech` as the custom domain, and turn on Enforce HTTPS.
