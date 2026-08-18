from sqlalchemy import inspect
from db import engine

inspector = inspect(engine)
schemas = inspector.get_schema_names()

with open("schema.sql", "w") as f:
    for schema in schemas:
        for table in inspector.get_table_names(schema=schema):
            f.write(f"-- {schema}.{table}\n")
            cols = inspector.get_columns(table, schema=schema)
            f.write(f"CREATE TABLE [{schema}].[{table}] (\n")
            for col in cols:
                f.write(f"    [{col['name']}] {col['type']},\n")
            f.write(");\n\n")

print("schema.sql created!")
