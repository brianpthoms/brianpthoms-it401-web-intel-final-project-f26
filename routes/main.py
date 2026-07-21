from functools import lru_cache

import requests
from flask import current_app, render_template

from services.api_service import ApiService
from services import github_service


CATALOG_SOURCE_URL = (
    "https://catalog.csuci.edu/preview_course_nopop.php?catoid=64&coid=145299"
)

FALLBACK_COURSE = {
    "title": "IT 401 - Web Intelligence",
    "units": "3",
    "meeting_format": "Three hours of lecture in the lab per week",
    "prerequisite": "IT 380",
    "description": (
        "Using web programming to extract information, using intelligent search "
        "engines, artificial intelligence techniques (expert systems, agents). "
        "Topics include: data mining, data warehousing, natural language processing, "
        "decision support systems, and intelligent agents."
    ),
    "grading": "Letter Grade",
    "catalog": "2026-2027 Catalog",
}


@lru_cache(maxsize=8)
def fetch_catalog_course(base_url, path, catoid, coid):
    service = ApiService(base_url, timeout=6)
    return service.get_catalog_course(
        path,
        params={"catoid": catoid, "coid": coid},
    )


def register_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        catalog_params = current_app.config["CATALOG_COURSE_PARAMS"]
        try:
            course = fetch_catalog_course(
                current_app.config["CATALOG_BASE_URL"],
                current_app.config["CATALOG_COURSE_PATH"],
                catalog_params["catoid"],
                catalog_params["coid"],
            )
            catalog_live = True
        except (requests.RequestException, ValueError):
            course = FALLBACK_COURSE
            catalog_live = False

        return render_template(
            "about.html",
            course=course,
            catalog_live=catalog_live,
            catalog_source_url=CATALOG_SOURCE_URL,
        )

    @app.route("/stats")
    def stats():
        try:
            repository = github_service.fetch_github_stats(
                current_app.config["GITHUB_API_BASE_URL"],
                current_app.config["GITHUB_REPOSITORY_PATH"],
            )
            stats_live = True
        except (requests.RequestException, ValueError):
            repository = {
                "repo_name": "bpthoms/it401_project_template",
                "stars": None,
                "language": None,
            }
            stats_live = False

        return render_template(
            "stats.html",
            repository=repository,
            stats_live=stats_live,
        )
