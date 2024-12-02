from pydantic import BaseModel


class Issue(BaseModel):
    issue_type: str
    title: str
    # task = report_time = null
    report_time: str
    # bug = task_point = null
    task_point: int


class IssueSchema(Issue):
    id: int
