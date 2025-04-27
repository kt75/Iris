import pytest
from unittest.mock import patch, MagicMock
from app import mongodb  # Import your mongodb module where client/collection are defined

# Example sample
sample_data = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
    "species": "setosa"
}

@patch("app.mongodb.db.iris_samples")
def test_remove_samples(mock_collection):
    mock_remove = MagicMock()
    mock_collection.delete_many = mock_remove

    mongodb.remove_samples()

    mock_remove.assert_called_once_with({})

@patch("app.mongodb.db.iris_samples")
def test_insert_sample(mock_collection):
    mock_insert = MagicMock()
    mock_collection.insert_one = mock_insert

    # Act
    mongodb.insert_sample(sample_data)

    # Assert
    mock_insert.assert_called_once_with(sample_data)

@patch("app.mongodb.db.iris_samples")
def test_get_samples(mock_collection):
    expected_samples = [sample_data]
    mock_collection.find.return_value = expected_samples

    samples = mongodb.get_samples()

    assert isinstance(samples, list)
    assert samples == expected_samples
    mock_collection.find.assert_called_once_with({}, {"_id": 0})