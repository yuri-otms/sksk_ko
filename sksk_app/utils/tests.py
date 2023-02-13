# class TestSession(Session):
#     def commit(self):
#         self.flush()
#         self.expire_all()

#     def remove(self):
#         self.expire_all()

#     def real_remove(self):
#         super(TestSession, self).remove()

# class SQLAlchemyWithOption:
#     def aaa():
#         if current_app.testing:
#             return SQLAlchemy(session_options={"class_":TestSession})
#         else:
#             return SQLAlchemy()
