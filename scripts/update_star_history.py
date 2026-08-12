#!/usr/bin/env python3
"""Generate a local Star History SVG from GitHub's stargazers API."""

from __future__ import annotations

import argparse
import html
import json
import os
from collections import Counter
from datetime import date, datetime
from http.client import RemoteDisconnected
from pathlib import Path
from time import sleep
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
DEFAULT_REPOSITORY = "yiqi-7/Cpp-Interviewer"
PAGE_SIZE = 100
MAX_ATTEMPTS = 5


def _parse_starred_date(value: str) -> date:
    """Convert an ISO-8601 GitHub timestamp to its calendar date."""
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).date()


def daily_star_counts(entries: Iterable[dict]) -> list[tuple[date, int]]:
    """Return cumulative star counts keyed by the date each star was added."""
    daily = Counter()
    for entry in entries:
        timestamp = entry.get("starred_at")
        if not timestamp:
            continue
        try:
            daily[_parse_starred_date(timestamp)] += 1
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid starred_at timestamp: {timestamp!r}") from exc

    cumulative = 0
    result = []
    for starred_date in sorted(daily):
        cumulative += daily[starred_date]
        result.append((starred_date, cumulative))
    return result


def load_entries(stream) -> list[dict]:
    """Load stargazer entries from a JSON stream."""
    payload = json.load(stream)
    if not isinstance(payload, list):
        raise ValueError("Star history input must be a JSON list")
    return payload


def _theme_colors(theme: str) -> dict[str, str]:
    if theme == "dark":
        return {
            "background": "#0d1117",
            "text": "#e6edf3",
            "muted": "#8b949e",
            "grid": "#30363d",
            "line": "#58a6ff",
            "point": "#79c0ff",
        }
    if theme == "light":
        return {
            "background": "#ffffff",
            "text": "#24292f",
            "muted": "#57606a",
            "grid": "#d0d7de",
            "line": "#0969da",
            "point": "#1f6feb",
        }
    raise ValueError("theme must be 'light' or 'dark'")


def _format_count(count: int) -> str:
    return f"{count:,} star" + ("" if count == 1 else "s")


def render_svg(entries: Iterable[dict], *, theme: str = "light") -> str:
    """Render a deterministic, self-contained SVG chart."""
    colors = _theme_colors(theme)
    series = daily_star_counts(entries)
    width, height = 760, 420
    left, right, top, bottom = 74, 26, 48, 66
    plot_width = width - left - right
    plot_height = height - top - bottom
    max_count = max((count for _, count in series), default=0)
    y_max = max(1, max_count)

    def x_position(index: int) -> float:
        if len(series) <= 1:
            return left + plot_width / 2
        return left + plot_width * index / (len(series) - 1)

    def y_position(count: int) -> float:
        return top + plot_height - plot_height * count / y_max

    def esc(value: object) -> str:
        return html.escape(str(value), quote=True)

    if series:
        points = " ".join(
            f"{x_position(i):.2f},{y_position(count):.2f}"
            for i, (_, count) in enumerate(series)
        )
        first_date = series[0][0].isoformat()
        last_date = series[-1][0].isoformat()
        summary = f"{_format_count(series[-1][1])}; {first_date} to {last_date}"
    else:
        points = ""
        summary = "No star data available"

    title = f"Star History - {_format_count(series[-1][1]) if series else 'no data'}"
    y_ticks = []
    for index in range(5):
        value = round(y_max * index / 4)
        if value not in y_ticks:
            y_ticks.append(value)

    grid_lines = []
    labels = []
    for value in y_ticks:
        y = y_position(value)
        grid_lines.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{width - right}" y2="{y:.2f}" '
            f'stroke="{colors["grid"]}" stroke-width="1" />'
        )
        labels.append(
            f'<text x="{left - 12}" y="{y + 4:.2f}" text-anchor="end" '
            f'fill="{colors["muted"]}" font-size="12">{esc(value)}</text>'
        )

    date_labels = []
    if series:
        label_indexes = [0] if len(series) == 1 else [0, len(series) - 1]
        for index in label_indexes:
            x = x_position(index)
            date_labels.append(
                f'<text x="{x:.2f}" y="{height - 28}" text-anchor="middle" '
                f'fill="{colors["muted"]}" font-size="12">{esc(series[index][0].isoformat())}</text>'
            )

    line = ""
    points_markers = ""
    if series:
        line = (
            f'<polyline points="{points}" fill="none" stroke="{colors["line"]}" '
            'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />'
        )
        points_markers = "".join(
            f'<circle cx="{x_position(i):.2f}" cy="{y_position(count):.2f}" r="4" '
            f'fill="{colors["point"]}" />'
            for i, (_, count) in enumerate(series)
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">{esc(summary)}</desc>
  <rect width="100%" height="100%" fill="{colors["background"]}" rx="8" />
  <text x="{left}" y="28" fill="{colors["text"]}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="20" font-weight="600">Star History</text>
  <text x="{width - right}" y="28" text-anchor="end" fill="{colors["muted"]}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="13">{esc(summary)}</text>
  {''.join(grid_lines)}
  {''.join(labels)}
  <line x1="{left}" y1="{top + plot_height}" x2="{width - right}" y2="{top + plot_height}" stroke="{colors["grid"]}" stroke-width="1" />
  {line}
  {points_markers}
  {''.join(date_labels)}
</svg>
'''


def fetch_stargazers(repository: str, token: str) -> list[dict]:
    """Fetch all stargazers with timestamps using a repository-scoped token."""
    encoded_repository = quote(repository, safe="/")
    entries: list[dict] = []
    page = 1
    while True:
        request = Request(
            f"{API_ROOT}/repos/{encoded_repository}/stargazers?per_page={PAGE_SIZE}&page={page}",
            headers={
                "Accept": "application/vnd.github.star+json",
                "Authorization": f"Bearer {token}",
                "User-Agent": "Cpp-Interviewer-star-history",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        for attempt in range(MAX_ATTEMPTS):
            try:
                with urlopen(request, timeout=60) as response:
                    payload = json.load(response)
                break
            except HTTPError as exc:
                retryable = exc.code == 429 or 500 <= exc.code < 600
                if retryable and attempt < MAX_ATTEMPTS - 1:
                    sleep(2**attempt)
                    continue
                detail = exc.read().decode("utf-8", errors="replace")[:240]
                raise RuntimeError(
                    f"GitHub stargazers request failed ({exc.code}): {detail}"
                ) from exc
            except (URLError, RemoteDisconnected, TimeoutError, OSError) as exc:
                if attempt < MAX_ATTEMPTS - 1:
                    sleep(2**attempt)
                    continue
                reason = getattr(exc, "reason", str(exc))
                raise RuntimeError(f"GitHub stargazers request failed: {reason}") from exc

        if not isinstance(payload, list):
            raise RuntimeError("GitHub stargazers response was not a list")
        entries.extend(payload)
        if len(payload) < PAGE_SIZE:
            return entries
        page += 1


def write_charts(entries: Iterable[dict], output_dir: Path) -> tuple[Path, Path]:
    """Write light and dark charts and return their paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    light_path = output_dir / "star-history-light.svg"
    dark_path = output_dir / "star-history-dark.svg"
    light_path.write_text(render_svg(entries, theme="light"), encoding="utf-8", newline="\n")
    dark_path.write_text(render_svg(entries, theme="dark"), encoding="utf-8", newline="\n")
    return light_path, dark_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=os.getenv("GITHUB_REPOSITORY", DEFAULT_REPOSITORY))
    parser.add_argument("--output-dir", type=Path, default=Path("assets"))
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required to read stargazer timestamps")

    entries = fetch_stargazers(args.repository, token)
    light_path, dark_path = write_charts(entries, args.output_dir)
    count = len(daily_star_counts(entries))
    print(f"Generated {light_path} and {dark_path} from {count} star dates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
