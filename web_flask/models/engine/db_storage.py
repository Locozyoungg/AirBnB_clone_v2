def close(self):
    """Calls remove() method on the private session attribute (self.__session)"""
    from sqlalchemy.orm import scoped_session
    from models.base_model import Base, Session
    Session.remove()
