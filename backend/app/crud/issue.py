from sqlmodel import Session
from app.db.models import Issue

# Updates the story points of an issue, returns None if the issue to be changed doesn't exist in the database
def update_story_point(db: Session, issue_id:int, updated_story_point:int):
    try:
        issue = db.query(Issue).filter(Issue.id == issue_id).first()

        issue.story_points = updated_story_point

        db.commit()
        db.refresh(issue)

        return issue

    except Exception as e:
        db.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500   
