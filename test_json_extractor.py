import pytest
import json
from json_extractor import (
    extract_relational_data,
)  # Assuming the main script is named json_extractor.py

# Test Case 1: Simple nested structure
simple_nested_json = {
    "person": {
        "id": "PERS001",
        "name": "John Doe",
        "age": 30,
        "address": {"id": "ADDR001", "street": "123 Main St", "city": "Anytown"},
    }
}

# Test Case 2: Array of objects
array_of_objects_json = {
    "team": {
        "id": "TEAM001",
        "name": "Dream Team",
        "members": [
            {"id": "MEM001", "name": "Alice", "role": "Developer"},
            {"id": "MEM002", "name": "Bob", "role": "Designer"},
        ],
    }
}

# Test Case 3: Complex nested structure with arrays
complex_nested_json = {
    "company": {
        "id": "COMP001",
        "name": "TechCorp",
        "departments": [
            {
                "id": "DEPT001",
                "name": "Engineering",
                "employees": [
                    {"id": "EMP001", "name": "Eve", "position": "Senior Developer"},
                    {"id": "EMP002", "name": "Frank", "position": "Junior Developer"},
                ],
            },
            {
                "id": "DEPT002",
                "name": "Marketing",
                "employees": [
                    {"id": "EMP003", "name": "Grace", "position": "Marketing Manager"}
                ],
            },
        ],
    }
}

# Test Case 4: Mixed data types and nested arrays
mixed_data_json = {
    "product": {
        "id": "PROD001",
        "name": "Smartphone",
        "price": 599.99,
        "specs": {
            "id": "SPEC001",
            "screen": "6.5 inch",
            "storage": ["64GB", "128GB", "256GB"],
            "colors": [
                {"id": "COL001", "name": "Black", "hex": "#000000"},
                {"id": "COL002", "name": "White", "hex": "#FFFFFF"},
            ],
        },
        "reviews": [
            {"id": "REV001", "user": "User1", "rating": 5, "comment": "Great product!"},
            {
                "id": "REV002",
                "user": "User2",
                "rating": 4,
                "comment": "Good value for money",
            },
        ],
    }
}


@pytest.mark.parametrize(
    "input_json, expected_tables",
    [
        (simple_nested_json, ["person", "address"]),
        (array_of_objects_json, ["team", "members"]),
        (complex_nested_json, ["company", "departments", "employees"]),
        (mixed_data_json, ["colors", "product", "reviews", "specs", "specs_storage"]),
    ],
)
def test_extract_relational_data_structure(input_json, expected_tables):
    result = extract_relational_data(input_json)
    assert set(result.keys()) == set(
        expected_tables
    ), f"Expected tables: {set(expected_tables)}, Got: {set(result.keys())}"


def test_simple_nested_structure():
    result = extract_relational_data(simple_nested_json)
    assert len(result["person"]) == 1
    assert result["person"][0]["id"] == "PERS001"
    assert result["address"][0]["id"] == "ADDR001"
    assert result["address"][0]["person_id"] == "PERS001"


def test_array_of_objects():
    result = extract_relational_data(array_of_objects_json)
    assert len(result["team"]) == 1
    assert len(result["members"]) == 2
    assert result["members"][0]["team_id"] == "TEAM001"
    assert result["members"][1]["team_id"] == "TEAM001"


def test_complex_nested_structure():
    result = extract_relational_data(complex_nested_json)
    assert len(result["company"]) == 1
    assert len(result["departments"]) == 2
    assert len(result["employees"]) == 3
    assert result["departments"][0]["company_id"] == "COMP001"
    assert result["employees"][0]["departments_id"] == "DEPT001"
    assert result["employees"][2]["departments_id"] == "DEPT002"


def test_mixed_data_types():
    result = extract_relational_data(mixed_data_json)
    assert len(result["product"]) == 1
    assert len(result["specs"]) == 1
    assert len(result["specs_storage"]) == 3
    assert len(result["colors"]) == 2
    assert len(result["reviews"]) == 2
    assert result["specs"][0]["product_id"] == "PROD001"
    assert result["colors"][0]["specs_id"] == "SPEC001"
    assert result["reviews"][0]["product_id"] == "PROD001"
    assert all(
        item["specs_id"] == "SPEC001" for item in result["specs_storage"]
    )


def test_id_relationships():
    result = extract_relational_data(complex_nested_json)
    company_id = result["company"][0]["id"]
    dept_ids = [dept["id"] for dept in result["departments"]]
    for employee in result["employees"]:
        assert employee["departments_id"] in dept_ids
    for dept in result["departments"]:
        assert dept["company_id"] == company_id
