# import logging
#
import app.crud.user as crud_user
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# def init() -> None:
#     with Session(engine) as session:
#         init_db(session)
#
#
# def main() -> None:
#     logger.info("Creating initial data")
#     init()
#     logger.info("Initial data created")
crud_user.add_admin_user()

if __name__ == "__main__":
    main()
