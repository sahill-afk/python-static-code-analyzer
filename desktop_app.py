"""Desktop entry point for Python Static Code Analyzer."""

import sys

from src.analyzer import analyze_code
from src.reports import create_csv_report, create_pdf_report
from src.ui.desktop_app import DesktopAnalyzerApp


def main() -> None:
    DesktopAnalyzerApp().run()


def _packaged_smoke_check() -> int:
    """Exercise bundled analysis/security/report dependencies without a window."""
    sample = (
        '"""Packaging smoke check."""\nimport pickle\n'
        "def load_untrusted(value):\n    return pickle.loads(value)\n"
        'eval("2 + 2")\n'
    )
    try:
        result = analyze_code(sample, "packaged_smoke_check.py")
    except Exception:
        return 15
    rules = {finding.rule_id for finding in result.findings}
    if not result.analyzed:
        return 11
    if not {"B301", "B307"}.issubset(rules):
        return 12
    if not create_csv_report(result).startswith(b"\xef\xbb\xbf"):
        return 13
    try:
        pdf = create_pdf_report(result)
    except Exception:
        return 14
    if not pdf.startswith(b"%PDF"):
        return 16
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(_packaged_smoke_check())
    main()
