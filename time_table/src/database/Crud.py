
from .database import DatabaseManager
from .cruds.TimeTableCruds import TimeTableCRUD


class Crud(TimeTableCRUD):
    def __init__(self, db_manager: DatabaseManager) -> None:
	    self.db_manager = db_manager
    
    
                
                


    
    
          

   