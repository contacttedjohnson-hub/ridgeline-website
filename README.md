# Ridgeline Realty website

The public site for Ridgeline Realty, the brokerage of Integrity Management
and Realty LLC (broker Theodore Johnson, BK3329952). Six plain HTML pages,
one stylesheet, one small script. No build step.

Moved here on 2026-10-20 from `business/real-estate/website`, which keeps
the logo drafts and design history. Built by Opus 5.5 in the chat session.

## Pages

| File | What it is |
|---|---|
| `index.html` | Home page |
| `buy.html` | Buyers: the process, financing readiness, featured homes, FAQ |
| `sell.html` | Sellers: pricing, process, the "what is my home worth" form |
| `commercial.html` | Commercial leasing and sales |
| `about.html` | Ted's background and service area |
| `schedule.html` | Appointment form and a spot for a booking calendar |
| `404.html` | Shown for any address that does not exist |
| `css/site.css` | All styling. Colours are in the `:root` block at the top. |
| `js/site.js` | Phone menu, time-slot buttons, form fallback |
| `img/` | Favicon, phone home-screen icon, link-preview picture. Put photos here too. |

## Listings

Each listing is a short text file in `listings/` (copy `listings/TEMPLATE.txt`)
plus photos in `img/listings/<folder>/`. Running `python build_listings.py`
builds the listing page, the cards on the home page and the sitemap entry.
Never edit a listing page by hand. The steps for adding and updating listings
are in `CLAUDE.md`.

## Editing

Open a page in Notepad, change the words between the tags, save, and
refresh the browser. Words that will most likely change are marked with
`<!-- EDIT -->` comments.

To preview the whole site, double-click `index.html`. It works straight
from the folder.

## Hosting

GitHub Pages, from the `main` branch, root folder, the same as the
Vineland site. Any push to `main` goes live a minute or two later.

The custom domain is **ridgelinerealtyfl.com**, registered at Porkbun on
2026-10-20 through 2029-10-20. DNS is at Porkbun. The site went live on
2026-10-20 with the featured-homes sections hidden (the `hidden` word on
each section) until real listings exist.

How the launch was done, kept for reference:

1. **No `CNAME` file yet.** Once one exists, GitHub sends every visitor to
   ridgelinerealtyfl.com, and that address does not work until the domain
   is bought and pointed here.
2. **Pages is not switched on yet.** Switching it on publishes the site,
   and the featured homes on the home and buy pages are invented. They
   come off or get replaced first.

### Turning it on

1. Buy ridgelinerealtyfl.com (Porkbun, $11.08 a year as of 2026-10-20).
2. In Porkbun's DNS for the domain, add the four GitHub Pages `A` records
   for the bare domain (185.199.108.153, 185.199.109.153, 185.199.110.153,
   185.199.111.153) and a `CNAME` record for `www` pointing at
   `contacttedjohnson-hub.github.io`. Delete Porkbun's default parking
   records.
3. Add a file named `CNAME` to this repo holding the single line
   `ridgelinerealtyfl.com`.
4. Repo Settings > Pages: source `main`, folder `/ (root)`. Enter the
   custom domain, wait for the DNS check, then tick **Enforce HTTPS**.

## Before launch

- [ ] Domain bought and DNS set (above)
- [ ] Email working at ted@ridgelinerealtyfl.com, which every page shows.
      Google Workspace (about $7 a month) or Porkbun's free forwarding to Gmail.
- [ ] Featured homes on `index.html` and `buy.html` replaced with real
      listings or removed. They are invented today.
- [ ] Grey photo blocks replaced with real photos, or left as plain colour
- [ ] Formspree form ID in place of `YOUR_FORM_ID` on the home, sell and
      schedule pages. Until then the forms open the visitor's email app,
      which only works once the email above exists.
- [ ] Licence year confirmed on DBPR (the pages say 2015)
- [ ] "Four houses renovated and resold, three in the last three years"
      confirmed
- [ ] Every page checked on a phone after it goes live

## Rules this site has to follow

Florida rule 61J2-10.025: every advertisement shows the licensed brokerage
name. The footer of every page carries "Ridgeline Realty is a registered
trade name of Integrity Management and Realty LLC, Licensed Real Estate
Broker". Do not remove it. DBPR shows the trade name on company licence
CQ1073686, so the Ridgeline name can be used.

No street address on the site. The rule does not require one. Office
meetings are by appointment, and the address goes out in the booking
confirmation.

The Equal Housing Opportunity mark stays in every footer.

Some claims about Ted carry conditions. He manages commercial property as a
salaried employee, which is not brokerage work. He is not a licensed home
inspector, and the pages say so. Credit help is advice, never "credit repair",
which is a regulated business in Florida. Commission is negotiable and no rate
is posted. Keep all four when editing.
