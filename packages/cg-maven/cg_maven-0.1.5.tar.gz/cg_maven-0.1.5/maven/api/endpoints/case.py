from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from maven.crud import create, read
from maven.maven_db.maven_adapter import MavenAdapter, get_maven_adapter
from maven.models.case import Case

case_router = APIRouter()


@case_router.post(
    "/case/",
    response_description="Create a new case document",
    status_code=status.HTTP_201_CREATED,
    response_model=Case,
)
def create_case(
    case: Case = Body(...),
    maven_adapter: MavenAdapter = Depends(get_maven_adapter),
) -> JSONResponse:
    """Create a case document in the database."""
    if read.get_case(case_id=case.id, maven_adapter=maven_adapter):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content="Case already in database.",
        )
    try:
        create.create_case(case=case, maven_adapter=maven_adapter)
    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content=f"Error: {error}"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=f"Case with {case.id} was created."
    )


@case_router.get(
    "/case/{case_id}",
    response_description="Get a case document.",
    status_code=status.HTTP_200_OK,
    response_model=Case,
)
def get_case(case_id: str, maven_adapter: MavenAdapter = Depends(get_maven_adapter)) -> Case:
    """Retrieve a case document from the database."""
    return read.get_case(case_id=case_id, maven_adapter=maven_adapter)
