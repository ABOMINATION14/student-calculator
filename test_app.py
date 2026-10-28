import pytest
from app import calculate_metrics

def test_calculate_metrics_valid_grade_a():
    # Pass a valid list of marks to the function
    total, average, grade = calculate_metrics([85, 90, 80])
    assert total == 255
    assert average == 85.0
    assert grade == "A"

def test_calculate_metrics_fail_grade():
    # Pass a failing list of marks to the function
    total, average, grade = calculate_metrics([40, 30, 45])
    assert grade == "F"

def test_calculate_metrics_empty():
    # Test handling of an empty list input gracefully
    total, average, grade = calculate_metrics([])
    assert total == 0
    assert average == 0
    assert grade == "F"
