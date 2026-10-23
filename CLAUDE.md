# CLAUDE.md, ridgeline-website

Public site for Ridgeline Realty. Plain static HTML on GitHub Pages from
`main`. Read `README.md` first: it has the launch checklist and the rules
the site must follow.

- Never remove the footer legal line (licensed brokerage name) or the
  Equal Housing Opportunity mark from any page. Florida rule 61J2-10.025.
- Never put Ted's home or office address on the site. Listing addresses
  are fine. The repo is public, so keep private details out of the files.
- No invented listings, reviews or numbers on the live site.
- Public copy says **Ted Johnson**. The licence line alone reads
  `Theodore "Ted" Johnson, Broker, BK3329952`.
- The logo is the Playfair R over Florida. The master drawing is
  `business/real-estate/marketing/brand/ridgeline-mark.svg` in the
  business repo (copied here as `img/ridgeline-mark.svg`); it is pasted
  inline in each page's header (on a navy tile) and footer.
- Pushing to `main` publishes. Work on a branch and land through a PR
  unless the owner says otherwise. After a merge, check that GitHub Pages
  built the new commit (`gh api repos/contacttedjohnson-hub/ridgeline-website/pages/builds/latest`);
  if it did not start, request one with `gh api -X POST .../pages/builds`.
- Verify changes by opening the pages in a browser at desktop and phone
  width, not by reading the HTML.

## Listings

Every listing is one text file, `listings/<page-name>.txt` (see
`listings/TEMPLATE.txt`), plus its photos in `img/listings/<folder>/`.
`python build_listings.py` writes `<page-name>.html`, the cards on the home
page between `<!-- LISTINGS:START -->` and `<!-- LISTINGS:END -->`, and the
sitemap entry. Never edit a listing page or that home-page block by hand;
edit the text file and rebuild.

**Adding a listing.** Ted sends a filled-in copy of the template and his
photos. Use only photos Ted took or has the rights to, and never the AI
"Regenerated" sets. Resize photos to 1600 px on the long side and save
them without EXIF data (no GPS). Run the script, check the new page and
the home page at desktop and phone width, open a PR.

**"Update the listings" (run for every file in `listings/`).**
1. For each address, search public listing sites (Realtor.com, Redfin,
   Zillow, Movoto) and the Polk County Property Appraiser for status,
   price, beds, baths, square footage and year built.
2. Report every difference to Ted in a short table. Do not change a file
   on the strength of a third-party site alone: the MLS listing is the
   source of truth and Ted is the listing broker, so he confirms first.
3. When Ted confirms a change (for example "505 is under contract" or
   "sold at 235,000"), edit the text file, update `checked:` with the date
   and source, run the script, and open a PR.
4. Sold listings stay on the site with status `Sold` as a track record
   unless Ted asks to remove them.

Do not scrape Zillow or the MLS into the site. Their terms forbid copying
their data and photos; the facts on these pages come from Ted.
