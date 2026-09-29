from pathlib import Path
root = Path(__file__).resolve().parents[2]
p = root / 'tmp/assignment3/verify_and_report.py'
s = p.read_text()
replacements = {
"'Instructor acceptance of CSS-only navbar/carousel substitutions', ": '',
"'<details class=\"mobile-menu'": "'<button class=\"navbar-toggler'",
'Use native details and summary.navbar-toggler for a mobile hamburger disclosure.': 'Use button.navbar-toggler with data-bs-toggle=collapse and a matching collapse.navbar-collapse target.',
'ADAPTATION: Bootstrap styling is genuine, but native disclosure replaces the JavaScript Collapse plugin. Instructor acceptance is required for strict grading.': 'Uses the standard Bootstrap Collapse plugin. Source wiring checked; browser interaction testing remains pending.',
"'css/site.css', '#look-1:checked', 8": "'about.html', '<div id=\"lookbook-carousel\"', 8",
'Use nine native radio inputs with numbered labels; CSS checked selectors choose the visible slide and corresponding Previous/Next labels.': 'Use nine data-bs-slide-to indicator buttons, one active slide, and Previous/Next buttons targeting the carousel ID.',
'Support wraparound navigation, native radio arrow-key selection, descriptive alternative text and captions. Keep playback manual.': 'Use the official Bootstrap Carousel plugin with descriptive image alternatives and captions. Disable automatic playback with data-bs-interval=false.',
'ADAPTATION: This is a CSS-only state controller, not the Bootstrap JavaScript Carousel plugin. Selection and layout need real browser verification.': 'Uses the standard Bootstrap Carousel plugin. Selection, swipe and keyboard behavior need real browser verification.',
'Use native menu/radio semantics': 'Use button controls and Bootstrap-managed menu state',
'while respecting the requirement to use only HTML and CSS.': 'with HTML, CSS and the authorized official Bootstrap JavaScript bundle.',
'The website contains no JavaScript. Native HTML and CSS replace the usual Bootstrap Collapse and Carousel plugins; these are declared adaptations, not claims of strict plugin compliance.': 'The four main pages load the official Bootstrap JavaScript bundle locally for the standard Collapse and Carousel plugins. No custom JavaScript is needed. The independent media-query exercise remains HTML and CSS only.',
'1. Confirm acceptance of the CSS-only navigation/carousel with the instructor.': '1. Verify the Bootstrap menu and all nine carousel indicators, including Previous/Next wraparound.',
'The HTML/CSS-only requirement creates a real trade-off for the standard interactive Bootstrap plugins; native controls can provide the interaction, but the instructor must accept that substitution.': 'Bootstrap handles menu and carousel interaction through HTML data attributes and its official JavaScript bundle. This separates our layout and theme work from the supplied component behavior.',
}
for old,new in replacements.items():
    assert old in s, old
    s=s.replace(old,new)
p.write_text(s)
p=root/'assignment-3/README.md'
s=p.read_text()
s=s.replace('Bootstrap 5.3.8 CSS and all nine images', 'Bootstrap 5.3.8 CSS, its official JavaScript bundle, and all nine images')
s=s.replace('There are no scripts, JavaScript dependencies, build steps, analytics, or form services.', 'The four main pages use only the official Bootstrap JavaScript bundle for interactive components. There is no custom JavaScript or build step. The independent media-query exercise remains HTML/CSS only.')
s=s.replace('CSS-only lookbook', 'Bootstrap lookbook')
s=s.replace('Mobile `summary.navbar-toggler` uses native `details` disclosure.', 'Mobile `button.navbar-toggler` targets `collapse.navbar-collapse` through Bootstrap data attributes.')
s=s.replace('CSS-only adaptation: not Bootstrap\'s JS Collapse plugin', 'Standard Bootstrap Collapse plugin; browser check pending')
s=s.replace('numbered indicators, previous/next labels, Bootstrap carousel markup, and CSS radio-state selection.', 'nine indicator buttons, Previous/Next buttons, and the standard Bootstrap Carousel plugin.')
s=s.replace('CSS-only adaptation: not Bootstrap\'s JS Carousel plugin', 'Standard Bootstrap Carousel plugin; browser check pending')
s=s.replace('native disclosure/radio controls', 'semantic buttons, Bootstrap-managed menu state and labelled radio controls')
start=s.index('## Important compatibility note')
end=s.index('## Files',start)
s=s[:start]+'''## Bootstrap interaction

The user authorized Bootstrap JavaScript after reviewing the lecture slides. All four main pages now load the official local 5.3.8 bundle. Navbar togglers use `data-bs-toggle="collapse"` with a matching target; the About carousel uses `data-bs-slide-to` and `data-bs-slide` buttons. The old CSS radio controller has been removed.

The lookbook stays manual with `data-bs-interval="false"`. Use the nine indicators or Previous/Next buttons. Verify keyboard, swipe and wraparound behavior in a real browser before submission.

'''+s[end:]
s=s.replace('Main theme and CSS-only interaction', 'Main theme and focus styles')
s=s.replace('- Official Bootstrap CSS:', '- Official Bootstrap bundle: `vendor/bootstrap.bundle.min.js`.\n- Official Bootstrap CSS:')
s=s.replace('all nine slide numbers', 'all nine slide indicators')
p.write_text(s)
