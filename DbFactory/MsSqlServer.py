from sqlalchemy import bindparam, create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
import pyodbc

class MSSQLDatabase:
    def __init__(self, connection_string):
      #  self.engine = create_engine(connection_string)
      #  self.meta = MetaData()
      #  self.meta.reflect(bind=self.engine)
      #  self.connection = self.engine.connect()
      #  self.session = sessionmaker(bind=self.engine)()
        self.connectionstring=connection_string
      

    def execute_stored_procedure(self, procedure_name, parameters=None):
        query = f"EXEC {procedure_name} "
        if parameters:
            query += ", ".join([f"@{key}=:{key}" for key in parameters.keys()])
            parameters = {key: bindparam(key, type_=type(value)) for key, value in parameters.items()}
        result = self.connection.execute(text(query), **parameters)
        return result
    
    def execute_reader(self, query):
        result = self.connection.execute(text(query))
        return result
    
    def execute_stored_procedure2(self, procedure_name, parameters=None):
       conn = pyodbc.connect(self.connectionstring)
       cursor = conn.cursor()       
       #parameter_values = list(parameters.values())
       #cursor.execute(procedure_name, parameter_values)
       # Construct the parameter placeholder string for the SQL query
       parameter_placeholders = ', '.join(['?' for _ in parameters])

        # Construct the SQL query with the stored procedure name and parameter placeholders
       sql_query = f"EXEC {procedure_name} {parameter_placeholders}"

        # Execute the SQL query with parameters
       cursor.execute(sql_query, list(parameters.values()))

      # Commit the transaction
       conn.commit()
     # Close the cursor and connection
       cursor.close()
       conn.close()

     