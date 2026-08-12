"""Regression tests for the self-hosted Star History chart."""

from datetime import date
from http.client import RemoteDisconnected
from io import BytesIO, StringIO
from pathlib import Path
from unittest.mock import patch

from scripts.update_star_history import (
    daily_star_counts,
    fetch_stargazers,
    load_entries,
    render_svg,
)


ROOT = Path(__file__).resolve().parents[1]


def test_daily_star_counts_sorts_dates_and_accumulates_same_day():
    entries = [
        {"starred_at": "2026-05-02T15:00:00Z"},
        {"starred_at": "2026-05-01T09:00:00Z"},
        {"starred_at": "2026-05-02T16:00:00Z"},
    ]

    assert daily_star_counts(entries) == [
        (date(2026, 5, 1), 1),
        (date(2026, 5, 2), 3),
    ]


def test_render_svg_is_deterministic_and_contains_no_remote_image_url():
    entries = [{"starred_at": "2026-05-01T09:00:00Z"}]

    first = render_svg(entries, theme="light")
    second = render_svg(entries, theme="light")

    assert first == second
    assert first.startswith("<svg ")
    assert "Star History" in first
    assert "1 star" in first
    assert "api.star-history.com" not in first
    assert "<script" not in first


def test_fetch_stargazers_retries_a_remote_disconnect():
    response = BytesIO(b'[{"starred_at":"2026-05-01T09:00:00Z"}]')

    with patch(
        "scripts.update_star_history.urlopen",
        side_effect=[RemoteDisconnected("closed"), response],
    ) as request, patch("scripts.update_star_history.sleep", create=True) as sleep:
        entries = fetch_stargazers("owner/repo", "token")

    assert entries == [{"starred_at": "2026-05-01T09:00:00Z"}]
    assert request.call_count == 2
    sleep.assert_called_once()


def test_load_entries_accepts_json_from_a_stream():
    stream = StringIO('[{"starred_at":"2026-05-01T09:00:00Z"}]')

    assert load_entries(stream) == [{"starred_at": "2026-05-01T09:00:00Z"}]


def test_readme_uses_local_light_and_dark_charts_in_both_languages():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "api.star-history.com/chart" not in readme
    assert readme.count("./assets/star-history-light.svg") == 4
    assert readme.count("./assets/star-history-dark.svg") == 2


def test_update_workflow_is_scheduled_and_can_push_generated_assets():
    workflow = (ROOT / ".github" / "workflows" / "update-star-history.yml").read_text(
        encoding="utf-8"
    )

    assert "schedule:" in workflow
    assert "workflow_dispatch:" in workflow
    assert "contents: write" in workflow
    assert "scripts/update_star_history.py" in workflow
    assert "git push" in workflow
    assert 'git config user.name "Yiqi"' in workflow
    assert 'git config user.email "yiqi_7@163.com"' in workflow
    assert "github-actions[bot]" not in workflow
