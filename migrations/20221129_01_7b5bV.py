"""
sample
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""CREATE TABLE documents (
    id serial,
    rubrics text[],
    text text,
    created_date date
    );""",
         """DROP TABLE documents;""")
]
