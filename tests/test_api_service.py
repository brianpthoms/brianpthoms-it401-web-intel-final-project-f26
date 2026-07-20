from services.api_service import ApiService


def test_parse_catalog_course():
    catalog_page = """
        <span id="acalog-catalog-name">2026-2027 Catalog</span>
        <p><h1 id="course_preview_title">IT 401&nbsp;-&nbsp;Web Intelligence</h1>
        <hr><strong>Units:</strong> <strong>3</strong><br>
        Three hours of lecture in the lab per week<br>
        <em>Prerequisite(s):</em> <a href="#">IT 380</a>&nbsp;<br>
        Using web programming to extract information and apply intelligent search.
        <br><em></em><em>Graded:</em> <em>Letter Grade</em></p>
    """

    course = ApiService._parse_catalog_course(catalog_page)

    assert course == {
        "title": "IT 401 - Web Intelligence",
        "units": "3",
        "meeting_format": "Three hours of lecture in the lab per week",
        "prerequisite": "IT 380",
        "description": (
            "Using web programming to extract information and apply intelligent search."
        ),
        "grading": "Letter Grade",
        "catalog": "2026-2027 Catalog",
    }
