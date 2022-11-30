"""
sample
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""CREATE TABLE documents (
    id serial PRIMARY KEY,
    rubrics text[],
    text text,
    created_date date,
    is_deleted boolean
    );""",
         """DROP TABLE documents;""")
]
