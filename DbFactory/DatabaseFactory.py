from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save_data(self, data):
        pass

class SQLDatabase(Database):
    def save_data(self, data):
        # Implementation to save data to a SQL database
        print("Saving data to SQL database")

class MongoDB(Database):
    def save_data(self, data):
        # Implementation to save data to a MongoDB database
        print("Saving data to MongoDB database")

def save_to_database(database_type, data):
    if database_type == 'SQL':
        db = SQLDatabase()
    elif database_type == 'MongoDB':
        db = MongoDB()
    else:
        raise ValueError("Unsupported database type")

    db.save_data(data)

# Example usage
data_to_save = "Sample data"  # Replace this with your actual data
database_type = "SQL"  # Replace this with the desired database type
save_to_database(database_type, data_to_save)
