"""Restore Keshav Jangid's original portfolio (Aug 27, 2026 Netlify Drop deploy)
and add a "Download Resume" button in the hero and in the contact/footer area.

The original site is a single self-contained index.html. It is fetched from the
preserved Aug 27 deploy permalink, the two resume buttons are inserted, the
co-founding / interior-design venture content is removed, and the result is
written as index.html for Netlify to publish. The resume PDF
(Keshav-Jangid-Resume.pdf) lives in this repo and is published alongside it.

The buttons reuse the exact styling of the original hero button: the
"Get in touch" button markup is cloned, only its link target and label change.
"""

import re
import urllib.request

ORIGINAL_URL = "https://6a9049f197e6ef978594db3d--keshavjangid.netlify.app/"
PDF = "Keshav-Jangid-Resume.pdf"

with urllib.request.urlopen(ORIGINAL_URL, timeout=60) as resp:
    html = resp.read().decode("utf-8")

# The original already links every project to the ksv-py GitHub repos, so no
# link changes are needed; only the resume buttons are added.

# --- DEBUG: print the raw markup around the co-founding mentions and the CSS,
# so the exact blocks can be identified from the build log. ---
for needle in ("Co-Founder", "co-running an interior design"):
    i = html.find(needle)
    if i != -1:
        print(f"--- MARKUP AROUND {needle!r} ---")
        print(html[max(0, i - 1200): i + 2500])
        print(f"--- END MARKUP AROUND {needle!r} ---")
    else:
        print(f"needle not found: {needle!r}")
style_m = re.search(r"<style[^>]*>(.*?)</style>", html, re.DOTALL)
if style_m:
    print("--- STYLE BLOCK ---")
    print(style_m.group(1))
    print("--- END STYLE BLOCK ---")
print("ARTEM present in source:", "artem" in html.lower())

# --- Remove the co-founding / interior-design venture content. ---
# (a) About paragraph about co-running the interior design business.
para_re = re.compile(
    r"<p\b[^>]*>(?:(?!</p>).)*?co-running an interior design and construction "
    r"business(?:(?!</p>).)*?</p>",
    re.DOTALL,
)
html, n_para = para_re.subn("", html, count=1)
print("removed about co-running paragraph:", n_para)

# (b) Co-Founder experience entry. Try an <article> container first; the
# debug markup above shows the real container if this does not match.
art_re = re.compile(
    r"<article\b[^>]*>(?:(?!</article>).)*?Co-Founder(?:(?!</article>).)*?</article>",
    re.DOTALL,
)
html, n_art = art_re.subn("", html, count=1)
print("removed co-founder article:", n_art)

# Safety net: nothing about the venture may survive in the page.
for bad in ("Co-Founder", "Co-founded", "co-running", "Interior Designing",
            "interior design", "Construction Venture", "Artem", "artem"):
    if bad in html:
        print(f"WARNING: still present after removal: {bad!r}")

# --- Resume buttons (clone the hero "Get in touch" button). ---
m = re.search(r"<a\b[^>]*>Get in touch</a>", html)
if not m:
    raise SystemExit("hero 'Get in touch' button not found")
hero_anchor = m.group(0)
open_tag = hero_anchor[: hero_anchor.index(">") + 1]
open_tag = re.sub(
    r"href=([\"'])[^\"']*\1", 'href="Keshav-Jangid-Resume.pdf"', open_tag, count=1
)
open_tag = open_tag.replace("<a", "<a download", 1)
resume_button = open_tag + "Download Resume</a>"

# 1. Hero: add the button right after the "Get in touch" button.
if html.count(hero_anchor) != 1:
    raise SystemExit("hero anchor is not unique")
html = html.replace(hero_anchor, hero_anchor + " " + resume_button, 1)

# 2. Contact/footer: add the button right after the footer's "GitHub" link.
# The footer starts at the email link; the first GitHub link after it is the
# footer's GitHub link.
email_anchor = "keshavjangid301@gmail.com</a>"
pos = html.find(email_anchor)
if pos == -1:
    raise SystemExit("footer email link not found")
gh = html.find("GitHub", pos)
if gh == -1:
    raise SystemExit("footer GitHub link not found")
close = html.find("</a>", gh)
if close == -1:
    raise SystemExit("footer GitHub closing tag not found")
at = close + len("</a>")
html = html[:at] + " " + resume_button + html[at:]

assert html.count("Download Resume") == 2, "expected exactly 2 resume buttons"
assert html.count(PDF) == 2, "expected exactly 2 resume PDF links"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("OK: wrote index.html (original design) with Download Resume buttons in hero and footer")
