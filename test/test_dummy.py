import requests
from pathlib import Path
import pytest
import socket

VERSION_MAJOR = 1
SERVER_URL = 'http://localhost:5000'
PATH_TO_FIXTURE_DATA = Path(__file__).resolve().parent / 'data'


def is_app_reachable(host=SERVER_URL, port=5000):
    """Check if the app is reachable on the given host and port."""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (OSError, ConnectionRefusedError):
        return False


@pytest.mark.skipif(not is_app_reachable(), reason="App is not reachable")
def test_send_process():
    url = SERVER_URL + f'/api/v{VERSION_MAJOR}/test/send_process'

    payload = {
        "param_int": 123,
        "param_str": "hello"
    }

    response = requests.post(url, json=payload)

    assert response.status_code == 200
    assert response.headers.get('content-type') == 'application/json'
    assert response.json() == {k: 2*v for k, v in payload.items()}


@pytest.mark.parametrize(
    'input,output',
    [
        ('a', 0),
        ('b', 1)
    ]
)
def test_parametrised(input, output):
    '''Check that pdf is read correctly by comparing the total number of pages extracted is as 
    expected.'''

    # this is the function you want to test. Normally lives in another module...
    def find_letter_position(letter: str):
        import string
        alphabet = string.ascii_lowercase
        return alphabet.find(letter.lower())

    assert find_letter_position(input) == output, 'Something went wrong...'


def test_exception_is_raised():

    # Function that raises an exception
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
