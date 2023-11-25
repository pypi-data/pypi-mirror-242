import os
import subprocess


def test_example_project_1():
    # Get current working directory
    cwd = os.path.dirname(__file__)

    def _root_path(file_path: str) -> str:
        return os.path.join(cwd, "fixtures/example_project_1", file_path)

    # Run the command
    subprocess.check_call(
        "jtd-codebuild fixtures/example_project_1",
        shell=True,
        cwd=cwd,
    )

    # Check the output

    # Intermediate schema file
    assert os.path.exists(_root_path("gen/schema.jtd.json"))

    # Python code
    assert os.path.exists(_root_path("gen/python/__init__.py"))

    # TypeScript code
    assert os.path.exists(_root_path("gen/typescript/index.ts"))

    # Test python code with `Book` class
    from .fixtures.example_project_1.gen.python import Book

    # It should be able to instantiate the class
    book = Book(id="1", name="Harry Potter")

    # It should be able to access the attributes with dot notation
    assert book.id == "1"

    # It should be able to modify the attributes with dot notation
    book.id = "2"
    assert book.id == "2"

    # It should be able to access the attributes with subscript notation
    assert book["id"] == "2"

    # It should be able to modify the attributes with subscript notation
    book["id"] = "3"
    assert book.id == "3"
