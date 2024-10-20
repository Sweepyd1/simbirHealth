from .database import DatabaseManager
from .cruds.DocumentCruds import DocumentCRUD


class Crud(DocumentCRUD):
    def __init__(self, db_manager: DatabaseManager) -> None:
	    self.db_manager = db_manager