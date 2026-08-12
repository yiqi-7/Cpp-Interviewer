"""Repository-root compatibility package for ``python -m coach.cli``.

The real backend lives under ``skills/coach/coach`` so it can be installed as
an Agent Skill. This shim keeps clone-and-run usage working from the repo root.
"""
from pathlib import Path
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

_real_package = Path(__file__).resolve().parent.parent / "skills" / "coach" / "coach"
if _real_package.exists():
    __path__.append(str(_real_package))
