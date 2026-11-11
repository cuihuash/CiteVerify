"""Regression checks for DOI extraction, cleanup, and report verification."""

import unittest
from dataclasses import asdict
from unittest.mock import patch
from urllib.parse import unquote

import citeverify_lookup as lookup
import citeverify_parser as parser
import citeverify_web as web


TITLE = "Habit, information acquisition, and the process of making travel mode choices"
DOI = "10.1002/(SICI)1099-0992(199709/10)27:5<539::AID-EJSP831>3.0.CO;2-A"
REFERENCE = (
    "Verplanken, B., Aarts, H., & Van Knippenberg, A. (1997). "
    f"{TITLE}. European journal of social psychology, 27(5), 539-560. "
    "https://doi.org/" + DOI.replace("AID-", "AID-\n")
)


class DoiParsingTests(unittest.TestCase):
    def test_sici_doi_survives_pdf_wrap_and_cleanup(self):
        item = parser.diagnose_reference(None, REFERENCE)
        self.assertEqual(item.doi, DOI)
        self.assertIn(DOI, item.cleaned_citation)
        self.assertIn("27(5), 539-560.", item.cleaned_citation)
        self.assertEqual(item.raw_citation, REFERENCE)
        self.assertEqual(lookup.best_title_candidate(asdict(item)), TITLE)

    def test_doi_is_not_mistaken_for_page_range(self):
        cleaned, flags = parser.remove_artifacts("https://doi.org/" + DOI)
        self.assertEqual(cleaned, "https://doi.org/" + DOI)
        self.assertEqual(flags, [])

    def test_common_dois_and_citation_wrappers(self):
        cases = {
            "https://doi.org/10.1111/j.1083-6101.2011.01559.x.":
                "10.1111/j.1083-6101.2011.01559.x",
            "<https://doi.org/10.1000/example>": "10.1000/example",
            "(doi: 10.1000/example).": "10.1000/example",
            "doi: 10.1000/example(1997).": "10.1000/example(1997)",
            "doi: 10.1000/wrapped-\nidentifier": "10.1000/wrapped-identifier",
            "doi: " + DOI.replace("<", "%3C").replace(">", "%3E"):
                DOI.replace("<", "%3C").replace(">", "%3E"),
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(parser.extract_identifiers(raw)[0], expected)
                self.assertIn(expected, parser.remove_artifacts(raw)[0])

    def test_trailing_colon_is_not_part_of_doi(self):
        raw = "Available at https://doi.org/10.1000/example: retrieved 2024."
        self.assertEqual(parser.extract_identifiers(raw)[0], "10.1000/example")

    def test_cleanup_preserves_multiple_dois_and_removes_real_artifacts(self):
        raw = f"pp. 539-560 https://doi.org/{DOI}; doi: 10.1000/1234-5678"
        cleaned, flags = parser.remove_artifacts(raw)
        self.assertIn(DOI, cleaned)
        self.assertIn("10.1000/1234-5678", cleaned)
        self.assertNotIn("539-560", cleaned)
        self.assertIn("page_or_line_label", flags)

    def test_full_doi_reaches_lookup_and_web_report(self):
        item = parser.diagnose_reference(None, REFERENCE)
        payload = {"message": {"title": [TITLE], "DOI": DOI}}
        with patch.object(lookup, "fetch_json", return_value=(200, payload, None)) as fetch:
            result = lookup.verify_item(asdict(item), 0, None, None, 1)
        self.assertEqual(unquote(fetch.call_args.args[0]), lookup.DOI_URL.format(DOI))
        self.assertEqual(result["verification"]["status"], "verified")
        report = web.report_body([{"filename": "regression.pdf", "results": [result]}])
        self.assertIn("Verified", report)
        self.assertIn("1099-0992", report)
        self.assertIn("&lt;539::AID-EJSP831&gt;", report)


if __name__ == "__main__":
    unittest.main()
