# Browser verification still required

The automated checks in verification.json inspect source only. This checklist has not been marked as passed.

1. Open index.html, collection.html, about.html, contact.html and media-queries.html.
2. Inspect each at 375px, 768px and 1440px viewport width, plus 767/768px and 991/992px boundary pairs.
3. Confirm no page-level horizontal overflow or overlapping text. A size-table region may scroll if needed.
4. On media-queries.html, confirm one, two and three card columns respectively. Check the heading and paragraph font-size changes.
5. On each main page at mobile width, open and close Menu using pointer, Enter and Space. Follow each link. On desktop, confirm the full navigation is visible and the mobile disclosure is hidden.
6. On About, select every numbered slide; verify the picture, caption and number agree. Use Previous on slide 1 and Next on slide 9 to verify wraparound.
7. With the keyboard, Tab to the selected slide radio and use arrow keys. Confirm focus stays visible and no hidden slide links enter the tab order.
8. On Contact, enter dummy values, select radio/checkbox states and use Clear form. Confirm defaults return and Sending unavailable remains disabled.
9. Follow all collection buttons and check that the size-guide anchor is visible.
10. Check reduced-motion mode and 200% browser zoom.
11. Save genuine screenshots of the five pages at the three main widths, plus open mobile navigation, a later carousel slide and the form.
12. Add those screenshots to the draft report, record only the results actually observed, and regenerate the final PDF and ZIP.

Do not present source-code excerpt images as screenshots of a rendered website.
