"""Test caesar.py"""
import subprocess
import pytest
from os import path

caesar_path = path.join(path.dirname(__file__), "caesar")

def test_caesar_empty():
    """Test caesar.py"""
    result = subprocess.run(
        [caesar_path],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: ./caesar key\n"

def test_caesar_bad_key_01():
    """Test caesar.py"""
    result = subprocess.run(
        [caesar_path, "HELLO"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: ./caesar key\n"


def test_caesar_bad_key_02():
    """Test caesar.py"""
    result = subprocess.run(
        [caesar_path, "1 2 3"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: ./caesar key\n"


DATA_IN = [
    ("13", "Hi there!"),
    ("1", "AA"),
    ("1", "Ab"),
    ("2", "Ab, cD"),
    ("5", "ExPiaLiDoCiouS"),
    ("17", "SuperCaliFragiLisTic"),
    ("21", "JcUnfQnItHntzX"),
]
DATA_OUT = [
    "Uv gurer!",
    "BB",
    "Bc",
    "Cd, eF",
    "JcUnfQnItHntzX",
    "JlgviTrczWirxzCzjKzt",
    "ExPiaLiDoCiouS",
]

@pytest.mark.parametrize(
    "input_data, expected_output",
    zip(DATA_IN, DATA_OUT),
)
def test_caesar_single(input_data, expected_output):
    """Test caesar.py"""
    result = subprocess.run(
        [caesar_path, input_data[0]],
        input=input_data[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == f"plaintext : ciphertext: {expected_output}\n"

def test_caesar_reverse_01():
    """Test caesar.py"""
    result = subprocess.run(
        [caesar_path, "13", "-r"],
        input="Uv gurer!",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "ciphertext: plaintext : Hi there!\n"

def test_caesar_reverse_02():
    """Test caesar.py"""
    result = subprocess.run(
        [caesar_path, "19", "-r"],
        input="Ab maxkx!",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "ciphertext: plaintext : Hi there!\n"
