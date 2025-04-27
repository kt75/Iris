import pytest
from app.utils import validate_csv_fields
from app import utils
from app.iris import IrisSample

def test_validate_csv_fields_correct():
    fields = {"sepal_length", "sepal_width", "petal_length", "petal_width", "species"}
    expected_fields = set(IrisSample.__annotations__.keys())
    validate = utils.validate_csv_fields(expected_fields, fields)
    assert validate is True

def test_validate_csv_fields_missing_column():
    fields = {"sepal_length", "sepal_width", "petal_length", "petal_width"}  # Missing 'species'
    expected_fields = set(IrisSample.__annotations__.keys())
    validate = utils.validate_csv_fields(expected_fields, fields)
    assert validate is False

def test_validate_csv_fields_extra_column():
    fields = {"sepal_length", "sepal_width", "petal_length", "petal_width", "species", "extra_column"}
    expected_fields = set(IrisSample.__annotations__.keys())
    validate = utils.validate_csv_fields(expected_fields, fields)
    assert validate is False
