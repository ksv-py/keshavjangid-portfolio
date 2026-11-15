"""Restore Keshav Jangid's original portfolio (Aug 27, 2026 Netlify Drop deploy)
and add a "Download Resume" button in the hero and in the contact/footer area.

The original site is a single self-contained index.html. It is fetched from the
preserved Aug 27 deploy permalink, the two resume buttons are inserted, and the
result is written as index.html for Netlify to publish. The resume PDF
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

# Clone the hero "Get in touch" button so the resume button matches it exactly.
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
