import html
import re

import requests


class ApiService:
    """Thin wrapper around outbound HTTP calls to external APIs."""

    def __init__(self, base_url, api_key=None, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self):
        headers = {
            "Accept": "application/json",
            "User-Agent": "IT401-Web-Intelligence/1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def get(self, path, params=None):
        response = self._get_response(path, params=params)
        return response.json()

    def get_text(self, path, params=None):
        """Return a text response from an HTML or plain-text endpoint."""
        response = self._get_response(
            path,
            params=params,
            accept="text/html,application/xhtml+xml",
        )
        return response.text

    def get_catalog_course(self, path, params=None):
        """Fetch and normalize a Modern Campus catalog course page."""
        page = self.get_text(path, params=params)
        return self._parse_catalog_course(page)

    def _get_response(self, path, params=None, accept=None):
        headers = self._headers()
        if accept:
            headers["Accept"] = accept

        response = requests.get(
            f"{self.base_url}/{path.lstrip('/')}",
            headers=headers,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response

    @classmethod
    def _parse_catalog_course(cls, page):
        course_block = cls._match(
            r"(<h1[^>]+id=['\"]course_preview_title['\"][^>]*>.*?</p>)",
            page,
        )
        if not course_block:
            raise ValueError("The catalog response did not contain course details")

        title = cls._clean_html(
            cls._match(r"<h1[^>]*>(.*?)</h1>", course_block)
        )
        units = cls._clean_html(
            cls._match(
                r"<strong>\s*Units:\s*</strong>\s*<strong>(.*?)</strong>",
                course_block,
            )
        )
        meeting_format = cls._clean_html(
            cls._match(
                r"<strong>\s*\d+\s*</strong>\s*<br\s*/?>(.*?)<br\s*/?>\s*<em>\s*Prerequisite",
                course_block,
            )
        )
        prerequisite = cls._clean_html(
            cls._match(
                r"<em>\s*Prerequisite\(s\):\s*</em>\s*(.*?)<br\s*/?>",
                course_block,
            )
        )
        description = cls._clean_html(
            cls._match(
                r"Prerequisite\(s\):\s*</em>.*?<br\s*/?>\s*(.*?)<br\s*/?>\s*<em>\s*</em>\s*<em>\s*Graded:",
                course_block,
            )
        )
        grading = cls._clean_html(
            cls._match(
                r"<em>\s*Graded:\s*</em>\s*<em>(.*?)</em>",
                course_block,
            )
        )
        catalog = cls._clean_html(
            cls._match(
                r"<span[^>]+id=['\"]acalog-catalog-name['\"][^>]*>(.*?)</span>",
                page,
            )
        )

        if not title or not description:
            raise ValueError("The catalog course details were incomplete")

        return {
            "title": title,
            "units": units,
            "meeting_format": meeting_format,
            "prerequisite": prerequisite,
            "description": description,
            "grading": grading,
            "catalog": catalog,
        }

    @staticmethod
    def _match(pattern, text):
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        return match.group(1) if match else ""

    @staticmethod
    def _clean_html(value):
        value = re.sub(r"<[^>]+>", " ", value or "")
        value = html.unescape(value).replace("\xa0", " ")
        return re.sub(r"\s+", " ", value).strip()

    def post(self, path, payload=None):
        response = requests.post(
            f"{self.base_url}/{path.lstrip('/')}",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
