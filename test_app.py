import pytest
from app import calculate_metrics

def test_calculate_metrics_valid():
    total, average = calculate_metrics([80, 90, 70])
    assert total == 240
    assert average == 80.0

def test_calculate_metrics_empty():
    total, average = calculate_metrics([])
    assert total == 0
    assert average == 0
