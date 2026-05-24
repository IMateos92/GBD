from __future__ import annotations

from pathlib import Path
import re
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify as md

DOCS = Path("docs")

ROOT_ORDER = [
    "index",
    "00entorno",
    "01intro",
    "02er",
    "03mr",
    "04mr-eer",
    "05ddl",
    "06sql",
    "07sql-group",
    "08sql-subquerys",
    "09dcl-tcl",
    "10plsql",
    "11triggers",
    "12nosql",
    "12redis",
    "13mongodb",
    "validacion",
    "relacion",
    "satisfaccion",
    "vocabulari",
    "tags",
    "print_page",
]


def clean_html_fragment(soup: BeautifulSoup) -> BeautifulSoup:
    for tag in soup.select("a.headerlink"):
        tag.decompose()
    for tag in soup.select("script, style, .mdx-cookie, .md-consent"):
        tag.decompose()
    return soup


def html_to_markdown(html_path: Path) -> tuple[str, str]:
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")

    article = soup.select_one("article.md-content__inner.md-typeset")
    if article is None:
        article = soup.select_one("main") or soup.body or soup

    article = clean_html_fragment(article)
    markdown = md(
        str(article),
        heading_style="ATX",
        bullets="-",
        strip=["span"],
    )

    # Normalize common artifacts.
    markdown = markdown.replace("\u00b6", "")
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip() + "\n"

    # Convert internal links from .html to .md.
    markdown = re.sub(r"\(([^)]+?)\.html(#[^)]+)?\)", r"(\1.md\2)", markdown)

    title = ""
    for line in markdown.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    if not title:
        html_title = soup.title.string.strip() if soup.title and soup.title.string else html_path.stem
        title = html_title.split(" - ")[0].strip()
        markdown = f"# {title}\n\n" + markdown

    return title, markdown


def build_nav(page_titles: dict[str, str], anexos_titles: dict[str, str]) -> list:
    nav: list = []

    for stem in ROOT_ORDER:
        md_name = f"{stem}.md"
        if md_name in page_titles:
            nav.append({page_titles[md_name]: md_name})

    remaining = sorted(k for k in page_titles.keys() if k not in {f"{s}.md" for s in ROOT_ORDER})
    for md_name in remaining:
        nav.append({page_titles[md_name]: md_name})

    if anexos_titles:
        anexos_nav = []
        for md_name in sorted(anexos_titles.keys()):
            anexos_nav.append({anexos_titles[md_name]: f"anexos/{md_name}"})
        nav.append({"Anexos": anexos_nav})

    return nav


def main() -> None:
    if not DOCS.exists():
        raise SystemExit("docs directory not found")

    html_files = sorted(DOCS.rglob("*.html"))
    page_titles: dict[str, str] = {}
    anexos_titles: dict[str, str] = {}

    for html_file in html_files:
        rel = html_file.relative_to(DOCS)
        out_rel = rel.with_suffix(".md")
        out_path = DOCS / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        title, markdown = html_to_markdown(html_file)
        out_path.write_text(markdown, encoding="utf-8")

        if rel.parts[0] == "anexos":
            anexos_titles[out_rel.name] = title
        else:
            page_titles[out_rel.name] = title

    # Remove old html content pages from docs to avoid serving static HTML content.
    for html_file in html_files:
        html_file.unlink()

    config = {
        "site_name": "Gestion de Bases de Datos",
        "docs_dir": "docs",
        "site_dir": "site",
        "use_directory_urls": False,
        "theme": {"name": "material"},
        "plugins": ["search"],
        "nav": build_nav(page_titles, anexos_titles),
    }

    Path("mkdocs.yml").write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")

    print(f"Converted {len(html_files)} HTML files to Markdown")


if __name__ == "__main__":
    main()
