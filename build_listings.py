"""Builds every listing page and the home page's listing cards from listings/*.txt.

    python build_listings.py

For each listings/<name>.txt (TEMPLATE.txt is skipped) it writes <name>.html,
rewrites the block between <!-- LISTINGS:START --> and <!-- LISTINGS:END -->
in index.html, and adds the page to sitemap.xml. Only the Python standard
library is used. See listings/TEMPLATE.txt for the fields.
"""
import html, os, re, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
LISTINGS = os.path.join(HERE, "listings")
STATUS_ORDER = {"for sale": 0, "under contract": 1, "sold": 2}


def read_listing(path):
    data, photos, details, features = {}, [], [], []
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip().lower(), value.strip()
        if key == "photo":
            file, _, caption = value.partition("|")
            photos.append((file.strip(), caption.strip()))
        elif key == "detail":
            label, _, text = value.partition("|")
            details.append((label.strip(), text.strip()))
        elif key == "feature":
            group, _, text = value.partition("|")
            features.append((group.strip(), text.strip()))
        else:
            data[key] = value
    for need in ("address", "city", "status", "price", "photos_folder"):
        if not data.get(need):
            sys.exit(f"{os.path.basename(path)}: '{need}' is empty")
    if not photos:
        sys.exit(f"{os.path.basename(path)}: add at least one 'photo:' line")
    data["photos"] = photos
    data["details"] = details
    data["features"] = features
    data["slug"] = os.path.splitext(os.path.basename(path))[0]
    return data


def e(text):
    return html.escape(text, quote=True)


def money(price):
    digits = re.sub(r"[^0-9]", "", price)
    return f"${int(digits):,}" if digits else price


def short_facts(d):
    out = []
    if d.get("beds"): out.append(f"{e(d['beds'])} bd")
    if d.get("baths"): out.append(f"{e(d['baths'])} ba")
    if d.get("sqft"): out.append(f"{int(re.sub(r'[^0-9]', '', d['sqft'])):,} sq ft")
    return "".join(f"<span>{x}</span>" for x in out)


def img(d, file):
    return f"img/listings/{d['photos_folder']}/{file}"


def page_body(d):
    rows = [("Status", d["status"]), ("Price", money(d["price"])), ("Bedrooms", d.get("beds")),
            ("Bathrooms", d.get("baths")),
            ("Living area", f"{int(re.sub(r'[^0-9]', '', d['sqft'])):,} sq ft" if d.get("sqft") else ""),
            ("Year built", d.get("year_built")), ("Garage", d.get("garage")), ("Lot size", d.get("lot_size")),
            ("Community", d.get("community")), ("HOA", d.get("hoa")), ("MLS number", d.get("mls_number"))]
    rows += d["details"]
    table = "\n".join(f"        <div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in rows if v)
    groups = {}
    for g, t in d["features"]:
        groups.setdefault(g, []).append(t)
    features = "".join(
        f'\n      <div><h3>{e(g)}</h3><ul class="checks">' + "".join(f"<li>{e(t)}</li>" for t in items) + "</ul></div>"
        for g, items in groups.items())
    features_section = f'''
<section>
  <div class="wrap">
    <div class="section-head"><h2>Features</h2></div>
    <div class="feature-groups">{features}
    </div>
  </div>
</section>
''' if features else ""
    lead_file, lead_cap = d["photos"][0]
    gallery = "\n".join(
        f'      <a href="{img(d, f)}" target="_blank" rel="noopener"><img src="{img(d, f)}" alt="{e(c)}" loading="lazy"></a>'
        for f, c in d["photos"])
    full = f"{d['address']}, {d['city']}"
    map_src = "https://maps.google.com/maps?q=" + quote(full) + "&z=15&output=embed"
    link = (f'\n      <p><a href="{e(d["listing_link"])}" target="_blank" rel="noopener">See this listing on '
            f'{e(re.sub(r"^https?://(www\\.)?", "", d["listing_link"]).split("/")[0])}</a></p>') if d.get("listing_link") else ""
    tag = d["status"]
    return f'''
<!-- Built by build_listings.py from listings/{d["slug"]}.txt. Edit that file, not this page. -->
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow">{e(tag)} · {e(d["city"].split(",")[0])}</div>
    <h1>{e(d["address"])}</h1>
    <p>{e(d["city"])}</p>
  </div>
</section>

<section>
  <div class="wrap listing">
    <img class="listing-lead" src="{img(d, lead_file)}" alt="{e(lead_cap or d["address"])}">
    <div class="listing-facts">
      <div class="price">{money(d["price"])}</div>
      <div class="facts">{short_facts(d)}{f"<span>Built {e(d['year_built'])}</span>" if d.get("year_built") else ""}</div>
      {f"<p>{e(d['description'])}</p>" if d.get("description") else ""}
      <p><a class="btn btn-gold" href="schedule.html">Book a showing</a></p>
      <p class="muted">Or call or text Ted at (863) 332-2615.</p>{link}
    </div>
  </div>
</section>

<section class="alt tight">
  <div class="wrap listing-more">
    <div>
      <div class="section-head"><h2>Details</h2></div>
      <dl class="details">
{table}
      </dl>
    </div>
    <div>
      <div class="section-head"><h2>Location</h2></div>
      <iframe class="map" title="Map of {e(full)}" src="{map_src}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>

{features_section}
<section class="alt tight">
  <div class="wrap">
    <div class="section-head"><h2>Photos</h2></div>
    <div class="gallery">
{gallery}
    </div>
  </div>
</section>
'''


def card(d):
    f, c = d["photos"][0]
    status = d["status"].lower()
    badge = "" if status == "for sale" else f'<span class="tag">{e(d["status"])}</span>'
    return f'''    <a class="listing-card" href="{d["slug"]}.html">
      <img src="{img(d, f)}" alt="{e(c or d["address"])}" loading="lazy">
      <div class="body">{badge}
        <div class="price">{money(d["price"])}</div>
        <div class="addr">{e(d["address"])}, {e(d["city"].split(",")[0])}</div>
        <div class="facts">{short_facts(d)}</div>
        <span class="more">See photos and details →</span>
      </div>
    </a>'''


def main():
    files = sorted(f for f in os.listdir(LISTINGS) if f.endswith(".txt") and f != "TEMPLATE.txt")
    listings = [read_listing(os.path.join(LISTINGS, f)) for f in files]
    for d in listings:
        for f, _ in d["photos"]:
            if not os.path.exists(os.path.join(HERE, img(d, f))):
                sys.exit(f"{d['slug']}: photo not found: {img(d, f)}")

    shell = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    head_end = shell.index("</header>") + len("</header>")
    foot_start = shell.index("<!-- Phone-only bar")
    for d in listings:
        full = f"{d['address']}, {d['city']}"
        page = shell[:head_end] + "\n" + page_body(d) + "\n" + shell[foot_start:]
        page = re.sub(r"<title>[^<]*</title>", f"<title>{e(full)} | Ridgeline Realty</title>", page, count=1)
        summary = f"{full}: {d.get('beds', '')} bed, {d.get('baths', '')} bath, {money(d['price'])}. {d['status']} with Ridgeline Realty."
        page = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + e(summary) + m.group(2), page, count=1)
        page = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                      lambda m: m.group(1) + f"https://ridgelinerealtyfl.com/{img(d, d['photos'][0][0])}" + m.group(2), page, count=1)
        open(os.path.join(HERE, d["slug"] + ".html"), "w", encoding="utf-8", newline="\n").write(page)
        print("wrote", d["slug"] + ".html")

    shown = sorted(listings, key=lambda d: (STATUS_ORDER.get(d["status"].lower(), 9), d["address"]))
    heading = "Current listing" if len(shown) == 1 else "Listings"
    block = (f'<!-- LISTINGS:START (built by build_listings.py; edit listings/*.txt instead) -->\n'
             f'<section class="alt tight" id="listings">\n  <div class="wrap">\n'
             f'    <div class="section-head"><h2>{heading}</h2></div>\n    <div class="listing-cards">\n'
             + "\n".join(card(d) for d in shown) +
             '\n    </div>\n  </div>\n</section>\n<!-- LISTINGS:END -->') if shown else \
            '<!-- LISTINGS:START (built by build_listings.py; edit listings/*.txt instead) -->\n<!-- LISTINGS:END -->'
    index = re.sub(r"<!-- LISTINGS:START.*?<!-- LISTINGS:END -->", lambda m: block, shell, count=1, flags=re.S)
    if index == shell and "LISTINGS:START" not in shell:
        sys.exit("index.html has no <!-- LISTINGS:START --> marker")
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n").write(index)
    print("updated index.html with", len(shown), "listing card(s)")

    sm_path = os.path.join(HERE, "sitemap.xml")
    sm = open(sm_path, encoding="utf-8").read()
    for d in listings:
        loc = f"https://ridgelinerealtyfl.com/{d['slug']}.html"
        if loc not in sm:
            sm = sm.replace("</urlset>", f"  <url><loc>{loc}</loc></url>\n</urlset>")
    open(sm_path, "w", encoding="utf-8", newline="\n").write(sm)


if __name__ == "__main__":
    main()
