"""CRUD module to find entries."""
from maven.maven_db.maven_adapter import MavenAdapter
from maven.models.case import Case


def get_case(case_id: str, maven_adapter: MavenAdapter) -> Case | None:
    """Retrieve a case document from the database."""
    case: dict = maven_adapter.maven_db.case.find_one({"id": case_id})
    if not case:
        return None
    return Case.model_validate(case)
