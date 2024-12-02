from fastapi import APIRouter
from typing import List
from api.model import Issue, IssueSchema
from crud import crud

router = APIRouter()


@router.get("/show-issues", response_model=List[IssueSchema], status_code=200)
def get_issues(issues_id: int | None = None):
    if issues_id is None:
        return crud.read_issues()
    else:
        return crud.read_issue(issues_id)


@router.post("/issues", response_model=IssueSchema, status_code=201)
def insert_issue(issue: Issue):
    return crud.create_issue(issue)
