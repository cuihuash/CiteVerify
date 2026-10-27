# Changelog

## Unreleased - DOI parsing and cleanup fixes

- Preserved paired angle brackets in older Wiley/SICI DOIs, including DOI
  components wrapped after a hyphen in PDFs, to prevent truncated lookups
  and false conflict results.
- Protected DOIs during reference cleanup so identifier components such as
  `1099-0992` are not removed as apparent page ranges.
- Preserved balanced parentheses within DOIs while removing citation wrappers.
- Added five regression tests covering extraction, cleanup, lookup requests,
  and HTML reports; confirmed the full DOI is retained in the original PDF.
  Lookup and report tests use simulated metadata; live lookup was unavailable.

## 0.1.4 - Running-header parsing fix

- Removed journal running headers that were being mistaken for separate
  references when a citation continued across a PDF page break.

## 0.1.3 - DOI line-wrap fix

- Preserved numeric DOI suffixes split onto the next PDF line or page when
  the preceding DOI ends with a hyphen.

## 0.1.2 - Two-column reference parsing fixes

- Joined separately positioned reference numbers and citation text.
- Preserved the correct left-column-then-right-column reading order.
- Removed publisher headers and download footers from reference lists.
- Rejoined soft-hyphenated words split across PDF lines.
- Recognized author-year references whose year is not followed by a period.
- Preserved DOI and web URLs split across PDF line breaks.
- Improved title candidates for books, reports, and conference papers.

## 0.1.1 - PDF extraction fixes

- Preserved reference lines at the top of PDF pages so leading authors are not lost.
- Improved reading order for two-column reference lists.
- Recognized continued-reference headings and avoided stopping at repeated running headers.
- Displayed matched author information when a lookup service provides it.

## 0.1.0 - Initial public release

- Added the CiteVerify HTML interface.
- Added support for uploading multiple PDF and modern Word (`.docx`) files.
- Added HTML reports with DOI links and explanations for unverified results.
- Added document navigation for multi-file reports.
- Added cautious verification using Crossref, DOI resolution, OpenAlex,
  Semantic Scholar, Open Library, and Google Books.
- Added local API-key files so each user can supply their own credentials.
- Added a Windows one-click launcher.
