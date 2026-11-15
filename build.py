"""Restore Keshav Jangid's original portfolio (Aug 27, 2026 Netlify Drop deploy),
remove the co-founding / interior-design venture content, and add a
"Download Resume" button in the hero and in the contact/footer area.

The original site is a single self-contained index.html. It is fetched from the
preserved Aug 27 deploy permalink, edited as below, and written as index.html
for Netlify to publish. The resume PDF (Keshav-Jangid-Resume.pdf) lives in this
repo and is published alongside it.

The buttons reuse the exact styling of the original hero button: the
"Get in touch" button markup is cloned, only its link target and label change.
The buttons link to /Keshav-Jangid-Resume.pdf (site root).
"""

import re
import urllib.request

ORIGINAL_URL = "https://6a9049f197e6ef978594db3d--keshavjangid.netlify.app/"
PDF = "Keshav-Jangid-Resume.pdf"

with urllib.request.urlopen(ORIGINAL_URL, timeout=60) as resp:
    html = resp.read().decode("utf-8")

# The original already links every project to the ksv-py GitHub repos, so no
# link changes are needed.

# --- Remove the co-founding / interior-design venture content. ---
# (a) About paragraph about co-running the interior design business.
para_re = re.compile(
    r"<p\b[^>]*>(?:(?!</p>).)*?co-running an interior design and construction "
    r"business(?:(?!</p>).)*?</p>",
    re.DOTALL,
)
html, n_para = para_re.subn("", html, count=1)
assert n_para == 1, "about co-running paragraph not found"

# (b) Co-Founder experience entry: the <div class="commit"> block holding the
# "Co-Founder" heading. Remove that whole block (up to the next entry).
h3 = html.find("<h3>Co-Founder</h3>")
assert h3 != -1, "Co-Founder heading not found"
start = html.rfind('<div class="commit">', 0, h3)
assert start != -1, "Co-Founder entry container not found"
next_commit = html.find('<div class="commit">', h3)
assert next_commit != -1, "next experience entry not found"
end = html.rfind("</div>", 0, next_commit) + len("</div>")
removed = html[start:end]
assert "Co-Founder" in removed, "removed block is not the Co-Founder entry"
assert "Interior Designing" in removed, "removed block is not the venture entry"
html = html[:start] + html[end:]

# Safety net: no trace of the venture may survive in the page.
for bad in ("Co-Founder", "Co-founded", "co-running", "Interior Designing",
            "interior design", "Construction Venture", "Artem"):
    assert bad not in html, f"venture content still present: {bad!r}"

# --- Resume buttons (clone the hero "Get in touch" button). ---
m = re.search(r"<a\b[^>]*>Get in touch</a>", html)
if not m:
    raise SystemExit("hero 'Get in touch' button not found")
hero_anchor = m.group(0)
open_tag = hero_anchor[: hero_anchor.index(">") + 1]
open_tag = re.sub(
    r"href=([\"'])[^\"']*\1", 'href="/Keshav-Jangid-Resume.pdf"', open_tag, count=1
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

# --- Small-screen fixes (keeps the original design). ---
# The original hides the nav links below 640px with no fallback, so the nav is
# unusable on phones. Show the links wrapped under the brand instead. Also
# guard the footer links and status-card values against overflow on narrow
# screens. This is an extra <style> block; the original CSS is untouched.
responsive_css = (
    "<style>\n"
    "@media (max-width:640px){\n"
    "  nav .wrap{flex-wrap:wrap; row-gap:2px; padding-top:12px; padding-bottom:12px;}\n"
    "  nav ul{display:flex; flex-wrap:wrap; gap:6px 18px; font-size:13px;}\n"
    "  .footer-links a{overflow-wrap:anywhere;}\n"
    "  .status-card .row{gap:12px;}\n"
    "  .status-card .v{overflow-wrap:break-word; min-width:0;}\n"
    "}\n"
    "</style>\n"
)
assert "</head>" in html, "no </head> found"
html = html.replace("</head>", responsive_css + "</head>", 1)

# Print the final file to the build log so its exact contents can be placed
# in the repo as a plain static file.
print("===FINAL INDEX.HTML START===")
print(html)
print("===FINAL INDEX.HTML END===")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("OK: wrote index.html (original design, venture content removed) with Download Resume buttons in hero and footer")
