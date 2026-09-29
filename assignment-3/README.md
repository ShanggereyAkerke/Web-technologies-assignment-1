# FORYOU - Assignment 3

Open `index.html` in a browser. The website works offline: Bootstrap 5.3.8 CSS, its official JavaScript bundle, and all nine images are included locally. The four main pages use only the official Bootstrap JavaScript bundle for interactive components. There is no custom JavaScript or build step. The independent media-query exercise remains HTML/CSS only.

## Team and ownership

- Team: FORYOU; group: SE-2504.
- Asankhan Shyngys: `index.html` and `collection.html`; Bootstrap navbar, cards, grid, buttons, size table.
- Shangerey Akerke: `about.html` and `contact.html`; Bootstrap navbar, grid, cards, Bootstrap lookbook and Bootstrap form.
- Both members: `media-queries.html`, responsive checks and report review.
- Both names appear in every page's footer.

## Required tasks

| Task | Implementation | Status |
| --- | --- | --- |
| 1. Responsive typography | `media-queries.html` / `css/media-queries.css`: explicit heading and paragraph changes at 768px and 992px. | Implemented; visual check pending |
| 2. Three cards without Bootstrap | Same independent page: 1 column below 768px, 2 columns at 768-991px, 3 columns from 992px. It loads no Bootstrap CSS. | Implemented; visual check pending |
| 3. Bootstrap grid | Home has two `col-lg-6` columns and three `col-lg-4` columns; every main page has a container, rows and responsive columns. | Implemented |
| 4. Spacing utilities | Main pages use Bootstrap `m-*`, `p-*`, `g-*` and `gap-*` utilities, including `mt-lg-4`, `mt-lg-5` and `px-sm-2`. `site.css` contains no custom margin or padding declarations. Pure-CSS Tasks 1-2 are the necessary exception. | Implemented |
| 5. Navbar | Four links on all four main pages, Bootstrap navbar/link/background classes. Mobile `button.navbar-toggler` targets `collapse.navbar-collapse` through Bootstrap data attributes. | Standard Bootstrap Collapse plugin; browser check pending |
| 6. Buttons | Bootstrap primary, secondary, outline, large, small and disabled styles; Collection has a linked `btn-group`; Contact has a native reset button. | Implemented |
| 7. Carousel | About has 9 distinct images, nine indicator buttons, Previous/Next buttons, and the standard Bootstrap Carousel plugin. | Standard Bootstrap Carousel plugin; browser check pending |
| 8. Cards | Home has 3 image/title/description cards in Bootstrap `card-group`. Collection has 4 more cards. | Implemented |
| 9. Form | Contact has `form-control`, `input-group`, `form-select`, `form-check`, radios, a checkbox and responsive Bootstrap columns. | Implemented; submission deliberately disabled |
| 10. Accessibility | Semantic landmarks, labelled inputs, image alternatives, semantic buttons, Bootstrap-managed menu state and labelled radio controls, focus styling, reduced-motion support and high-contrast text. | Source checks complete; keyboard/browser audit pending |

## Bootstrap interaction

The user authorized Bootstrap JavaScript after reviewing the lecture slides. All four main pages now load the official local 5.3.8 bundle. Navbar togglers use `data-bs-toggle="collapse"` with a matching target; the About carousel uses `data-bs-slide-to` and `data-bs-slide` buttons. The old CSS radio controller has been removed.

The lookbook stays manual with `data-bs-interval="false"`. Use the nine indicators or Previous/Next buttons. Verify keyboard, swipe and wraparound behavior in a real browser before submission.

## Files

- Four main pages: `index.html`, `collection.html`, `about.html`, `contact.html`.
- Independent media-query exercise: `media-queries.html`, `css/media-queries.css`.
- Main theme and focus styles: `css/site.css`.
- Official Bootstrap bundle: `vendor/bootstrap.bundle.min.js`.
- Official Bootstrap CSS: `vendor/bootstrap.min.css` (MIT license, header preserved).
- Nine gallery assets: `images/`.
- Submission and verification details: `docs/`.

## Submission status

Source-level checks are automated. Browser preview was blocked by the environment's local-file URL policy, so rendered screenshots and interactive browser verification are still pending. Do not claim these checks passed.

The report is explicitly marked DRAFT until genuine webpage screenshots and the verified deployed URL are added. No commit, push, deployment or LMS submission has been performed. Each team member must submit the final PDF and ZIP and defend the work by the LMS deadline.

## Publication checklist

1. Review this folder and the report with both members.
2. Verify mobile (375px), tablet (768px), desktop (1440px), and 767/768 and 991/992 breakpoint boundaries.
3. Test menu open/close, all nine slide indicators, wraparound Previous/Next, keyboard arrows, all links and form reset.
4. Take genuine code and webpage screenshots and add them to the report.
5. Commit and push the approved folder to the team's chosen shared repository.
6. Deploy with GitHub Pages or Netlify. If the repository root is published, the new entry point is `/assignment-3/`.
7. Open the actual live URL and add it to the report. Do not use an unverified predicted URL.
8. Export the final report, regenerate the ZIP, and have both members submit separately.

## References

- https://getbootstrap.com/docs/5.3/getting-started/introduction/
- https://getbootstrap.com/docs/5.3/layout/grid/
- https://getbootstrap.com/docs/5.3/utilities/spacing/
- https://getbootstrap.com/docs/5.3/components/navbar/
- https://getbootstrap.com/docs/5.3/components/carousel/
- https://getbootstrap.com/docs/5.3/components/card/

Original Assignment 2 pages remain in the parent folder.
