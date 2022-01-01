from .mongodb import get_database
from app.core.config import database_name

db = get_database(database_name)