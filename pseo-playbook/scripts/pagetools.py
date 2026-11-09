"""Shared helpers for the pSEO scripts: fetching pages, and pulling text, links and
SEO tags out of HTML with the standard library only."""
import os
import re
import ssl
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; pseo-playbook-checker/1.0)"
SKIP_TAGS = {"script", "style", "noscript", "svg", "template"}
BOILER_TAGS = {"nav", "header", "footer", "aside", "form"}


def fetch(url, timeout=20):
    """Return (status_code, final_url, html_text, error). Does not follow redirects silently:
    a redirect is reported as its status code."""

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with opener.open(req, timeout=timeout) as r:
            body = r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")
            return r.status, r.geturl(), body, ""
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location", "") if e.headers else ""
        return e.code, urljoin(url, loc) if loc else url, "", ""
    except Exception as e:  # network blocked, DNS, timeout
        return 0, url, "", str(e)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.boiler = 0
        self.text, self.main_text = [], []
        self.links = []          # (href, anchor_text, in_boilerplate)
        self._a = None
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.canonical = ""
        self.h1, self.h2 = [], []
        self._h = None
        self._hbuf = []
        self.jsonld = []
        self._in_jsonld = False
        self._jbuf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._in_jsonld, self._jbuf = True, []
            return
        if tag in SKIP_TAGS:
            self.skip += 1
        if tag in BOILER_TAGS:
            self.boiler += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        if tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = a.get("href", "")
        if tag == "a" and a.get("href"):
            self._a = [a["href"], [], self.boiler > 0]
        if tag in ("h1", "h2"):
            self._h, self._hbuf = tag, []

    def handle_endtag(self, tag):
        if tag == "script" and self._in_jsonld:
            self.jsonld.append("".join(self._jbuf))
            self._in_jsonld = False
            return
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1
        if tag in BOILER_TAGS and self.boiler:
            self.boiler -= 1
        if tag == "title":
            self._in_title = False
        if tag == "a" and self._a:
            self.links.append((self._a[0], " ".join(self._a[1]).strip(), self._a[2]))
            self._a = None
        if tag == self._h:
            txt = " ".join(" ".join(self._hbuf).split())
            (self.h1 if tag == "h1" else self.h2).append(txt)
            self._h = None

    def handle_data(self, data):
        if self._in_jsonld:
            self._jbuf.append(data)
            return
        if self._in_title:
            self.title += data
        if self.skip:
            return
        d = data.strip()
        if not d:
            return
        self.text.append(d)
        if not self.boiler:
            self.main_text.append(d)
        if self._a:
            self._a[1].append(d)
        if self._h:
            self._hbuf.append(d)


def parse(html):
    p = PageParser()
    p.feed(html or "")
    p.title = " ".join(p.title.split())
    return p


def read_html_dir(folder):
    """Yield (filename, html) for every .html/.htm file in a folder (recursively)."""
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            if fn.lower().endswith((".html", ".htm")):
                path = os.path.join(root, fn)
                with open(path, encoding="utf-8", errors="replace") as f:
                    yield path, f.read()


def guess_url(path, html, base=None):
    """Best guess of a saved file's URL: canonical first, then og:url, then base + filename."""
    p = parse(html)
    for cand in (p.canonical, p.meta.get("og:url", "")):
        if cand.startswith("http"):
            return cand
    if base:
        name = os.path.splitext(os.path.basename(path))[0]
        return base.rstrip("/") + "/" + ("" if name == "index" else name)
    return path


def same_site(href, page_url):
    u = urljoin(page_url, href)
    a, b = urlparse(u), urlparse(page_url)
    return a.scheme in ("http", "https") and a.netloc.replace("www.", "") == b.netloc.replace("www.", ""), u


def norm_url(u):
    u = re.sub(r"[#?].*$", "", u.strip())
    return u.rstrip("/") if urlparse(u).path not in ("", "/") else u.rstrip("/") + "/"


def read_url_list(path):
    urls = []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip().split(",")[0]
            if line.startswith("http"):
                urls.append(line)
    return urls
