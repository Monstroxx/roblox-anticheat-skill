#!/usr/bin/env python3
"""Fetch selected official Roblox Markdown pages or search results, without caching."""

import argparse
import json
import sys
import unittest
from unittest.mock import patch
from urllib.parse import quote, unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = "https://create.roblox.com"
INDEXES = {
    "concepts": "/docs/llms.txt",
    "engine": "/docs/reference/engine/llms.txt",
    "deprecated": "/docs/reference/engine/deprecated.md",
}
MAX_BYTES = 2 * 1024 * 1024


def official_url(value):
    url = urljoin(ROOT + "/", value)
    parsed = urlsplit(url)
    decoded = unquote(parsed.path).lower()
    if (
        parsed.scheme != "https"
        or parsed.netloc != "create.roblox.com"
        or not parsed.path.startswith("/docs/")
        or parsed.query
        or "llms-full" in decoded
        or ".." in decoded.split("/")
    ):
        raise ValueError("Use an official /docs/ URL; llms-full and queries are refused")
    # Engine search results include section anchors. They select a section,
    # but are not part of the HTTP request for its Markdown page.
    return parsed._replace(fragment="").geturl()


def fetch(value):
    url = official_url(value)
    request = Request(url, headers={"User-Agent": "roblox-anticheat-docs/1.0"})
    with urlopen(request, timeout=30) as response:
        official_url(response.geturl())
        body = response.read(MAX_BYTES + 1)
    if len(body) > MAX_BYTES:
        raise ValueError("Response exceeds 2 MiB; select individual pages instead")
    text = body.decode("utf-8")
    if text.lstrip().lower().startswith(("<!doctype html", "<html")):
        raise ValueError("Received HTML instead of documentation; use the official search/index")
    return text


def search_path(question):
    question = question.strip().replace(".", " ")
    if not question.strip():
        raise ValueError("Provide a non-empty search question")
    return "/docs/api/search/" + quote(question, safe="")


def search(question):
    data = json.loads(fetch(search_path(question)))
    if not isinstance(data, dict) or "error" in data:
        raise ValueError("Malformed search response: " + json.dumps(data, ensure_ascii=False))
    results = data.get("results")
    if not isinstance(results, list):
        raise ValueError("Search response has no results array")
    selected = []
    for item in results[:20]:
        if not isinstance(item, dict) or not isinstance(item.get("url"), str):
            raise ValueError("Search result has no usable URL")
        url = official_url(item["url"])
        if not urlsplit(url).path.endswith(".md"):
            raise ValueError("Search did not return a Markdown URL; inspect the official index")
        selected.append({"title": item.get("title"), "summary": item.get("summary"), "url": url})
    return {"results": selected, "total_returned": len(results)}


class SelfTests(unittest.TestCase):
    def test_official_page(self):
        self.assertEqual(official_url("/docs/en-us/luau.md"), ROOT + "/docs/en-us/luau.md")
        self.assertEqual(official_url("/docs/en-us/luau.md#types"), ROOT + "/docs/en-us/luau.md")

    def test_refused_urls(self):
        for value in (
            "https://example.com/docs/a.md", "http://create.roblox.com/docs/a.md",
            "//example.com/docs/a.md", "/docs/llms-full.txt", "/docs/%6clms-full.txt",
            "/docs/a.md?q=1", "/docs/../a.md",
            "/docs/%2e%2e/a.md", "https://create.roblox.com@evil.test/docs/a.md",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                official_url(value)

    def test_search_encoding(self):
        self.assertEqual(search_path("Vector3.new range"), "/docs/api/search/Vector3%20new%20range")
        self.assertEqual(search_path("touch/interaction"), "/docs/api/search/touch%2Finteraction")
        with self.assertRaises(ValueError):
            search_path("  ")

    def test_search_contract(self):
        sample = {"results": [{"title": "Event", "url": ROOT + "/docs/en-us/remote.md#FireServer"}]}
        with patch(__name__ + ".fetch", return_value=json.dumps(sample)):
            self.assertEqual(search("remote")["results"][0]["url"], ROOT + "/docs/en-us/remote.md")
        for sample in ({"error": "malformed", "results": []}, {"results": [{}]}, {"results": "bad"}):
            with patch(__name__ + ".fetch", return_value=json.dumps(sample)), self.assertRaises(ValueError):
                search("remote")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="Run offline URL/search contract tests")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("search").add_argument("question")
    sub.add_parser("page").add_argument("path", help="Exact Markdown path discovered in an index/search")
    sub.add_parser("index").add_argument("name", choices=INDEXES)
    args = parser.parse_args()
    if args.selftest:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(SelfTests)
        return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
    try:
        if args.command == "search":
            print(json.dumps(search(args.question), ensure_ascii=False, indent=2))
        elif args.command == "page":
            url = official_url(args.path)
            if not urlsplit(url).path.endswith(".md"):
                raise ValueError("Pass an exact .md page discovered in the official index/search")
            print("Source: " + url + "\n\n" + fetch(url))
        elif args.command == "index":
            print(fetch(INDEXES[args.name]))
        else:
            parser.print_help()
            return 2
    except (OSError, ValueError) as error:
        print("Documentation lookup failed: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
