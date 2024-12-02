from api.model import Issue, IssueSchema
from db.model import IssueDB
from db.session import session


def create_issue(par_issue: Issue) -> IssueSchema:
    issue_db = IssueDB(
        issue_type=par_issue.issue_type,
        title=par_issue.title,
        report_time=None,
        task_point=par_issue.task_point,
    )

    session.add(issue_db)
    session.commit()

    issue_schema = IssueSchema(
        id=issue_db.id,
        issue_type=issue_db.issue_type,
        report_time=issue_db.report_time,
        task_point=issue_db.task_point,
    )

    return issue_schema


def read_issues() -> list[IssueSchema]:
    issues_db = session.query(IssueDB).all()

    issues_schema = []

    for issue in issues_db:
        issues_schema.append(
            IssueSchema(
                id=issue.id,
                issue_type=issue.issue_type,
                title=issue.title,
                report_time=issue.report_time,
                task_point=issue.task_point,
            )
        )
    return issues_schema


def read_issue(id: int) -> IssueSchema:
    issue_db = session.query(IssueDB).filter(IssueDB.id == id).one()

    issue_schema = IssueSchema(
        id=issue_db.id,
        issue_type=issue_db.issue_type,
        title=issue_db.title,
        report_time=issue_db.report_time,
        task_point=issue_db.task_point,
    )

    return issue_schema


def update_issue(id: int) -> IssueSchema:
    pass


def delete_issue(id: int) -> IssueSchema:
    issue_db = session.query(IssueDB).filter(IssueDB.id == id).one()
    session.query(IssueDB).filter(IssueDB).delete()
    session.commit()

    issue_schema = IssueSchema(
        id=issue_db.id,
        issue_type=issue_db.issue_type,
        title=issue_db.title,
        report_time=issue_db.report_time,
        task_point=issue_db.task_point,
    )

    return issue_schema
