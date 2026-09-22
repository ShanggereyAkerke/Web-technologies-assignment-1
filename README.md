# FORYOU - Assignment 2

A four-page clothing-store project for Advanced CSS: Flexbox & Grid.

**Team:** FORYOU · **Group:** SE-2504

- Asankhan Shyngys: Home and Collection.
- Shangerey Akerke: About us and Contact.

## Open the website

Open this folder in VS Code. Open `index.html` in a browser, or use Live Server. No installation or build is required.

## Project structure

```text
FORYOU-assignment-2/
  index.html          Home: three Flexbox product cards
  collection.html     Four Flexbox product cards and size guide
  about.html          Flexbox team panels and nine-image Grid gallery
  contact.html        Grid content columns and Flexbox name/email fields
  css/style.css       Shared colours, Grid areas, Flexbox, media queries
  images/             Existing local photos
```

## Assignment requirements in the code

| Task | Where to look |
| --- | --- |
| Flexbox navigation | Every page; `#main-header` and `nav` in CSS |
| At least three equal-height cards with images, titles, text, buttons | Home has three; Collection has four; `.products`, `.card`, `.card-action` |
| Card gaps and hover effect | `.products` has `gap`; `.card:hover` adds lift and shadow |
| Header/sidebar/main/footer Grid areas | Every page uses `body.page-layout`; CSS defines columns, rows, areas and each element's `grid-area` |
| Nine-image gallery | About us; `.gallery` and `.gallery-item` |
| Equal gallery columns/rows and gaps | `repeat(3, minmax(0, 1fr))`, `grid-auto-rows: 240px`, `gap: 20px` |
| Hover captions | `.gallery-item:hover figcaption`; also keyboard focus and always-visible touch captions |
| Flexbox on both members' pages | Product rows on Home/Collection; team panels on About; form fields on Contact |
| Responsive layout | Tablet breakpoint at 1100px; stacked phone layout at 650px |

The contact form is a visual demonstration; its send button is disabled. Product-card buttons open the Contact page. No backend is included or required by Assignment 2.

## Publication status

This is a local update based on the last supplied Assignment 1 ZIP. It has not been merged into the shared GitHub repository or deployed. Review the separate handover guide before copying changes into a newer checkout.
