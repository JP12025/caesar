"""Test caesar.py"""
import os
import sys
import subprocess
import pytest


caesar_path = os.path.join(os.path.dirname(__file__), "caesar")

def test_caesar_empty():
    """Test caesar.py"""
    param = [caesar_path]
    if sys.platform == "win32":
        param = ["python", caesar_path]
    result = subprocess.run(
        param,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: ./caesar key\n"

def test_caesar_bad_key_01():
    """Test caesar.py"""
    param = [caesar_path, "HELLO"]
    if sys.platform == "win32":
        param = ["python", caesar_path, "HELLO"]
    result = subprocess.run(
        param,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: ./caesar key\n"


def test_caesar_bad_key_02():
    """Test caesar.py"""
    param = [caesar_path, "1 2 3"]
    if sys.platform == "win32":
        param = ["python", caesar_path, "1 2 3"]
    result = subprocess.run(
        param,
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
    param = [caesar_path, input_data[0]]
    if sys.platform == "win32":
        param = ["python", caesar_path, input_data[0]]
    result = subprocess.run(
        param,
        input=input_data[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == f"plaintext : ciphertext: {expected_output}\n"

def test_caesar_reverse_01():
    """Test caesar.py"""
    param = [caesar_path, "13", "-r"]
    if sys.platform == "win32":
        param = ["python", caesar_path, "13", "-r"]
    result = subprocess.run(
        param,
        input="Uv gurer!",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "ciphertext: plaintext : Hi there!\n"

def test_caesar_reverse_02():
    """Test caesar.py"""
    param = [caesar_path, "19", "-r"]
    if sys.platform == "win32":
        param = ["python", caesar_path, "19", "-r"]
    result = subprocess.run(
        param,
        input="Ab maxkx!",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "ciphertext: plaintext : Hi there!\n"
