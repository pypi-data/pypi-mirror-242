from json import loads
from random import choice
from string import ascii_letters, digits, punctuation
from pytest import mark
from SocksDriver import SocksClient

ALPHANUMERIC = ascii_letters + digits


def generate_random_string(num_strings: int, len_strings: int) -> list[str]:
    result = []

    for _ in range(num_strings):
        result.append("".join(choice(ALPHANUMERIC) for _ in range(len_strings)))

    return result


def generate_random_punctuation(num_strings: int, len_strings: int) -> list[str]:
    result = []

    for _ in range(num_strings):
        result.append("".join(choice(punctuation) for _ in range(len_strings)))

    return result


# OS specific line break tests


def test_handle_line_feed(client: SocksClient) -> None:
    result = loads(client.send("foobar\nabc"))
    assert result["message"] == "foobar\nabc"


def test_handle_line_feed_strip_newline(client: SocksClient) -> None:
    result = loads(client.send("foobar\n"))
    assert result["message"] == "foobar\n"


def test_handle_carriage_return(client: SocksClient) -> None:
    result = loads(client.send("foobar\rabc"))
    assert result["message"] == "foobar\rabc"


def test_handle_carriage_return_strip_carriage_return(client: SocksClient) -> None:
    result = loads(client.send("foobar\r"))
    assert result["message"] == "foobar\r"


def test_handle_end_of_line_strip_end_of_line(client: SocksClient) -> None:
    result = loads(client.send("foobar\r\n"))
    assert result["message"] == "foobar\r\n"


def test_handle_end_of_line(client: SocksClient) -> None:
    result = loads(client.send("foobar\r\nabc"))
    assert result["message"] == "foobar\r\nabc"


# Test "empty" messages
# Note that a true empty message, '', would be considered an EOF / hangup by the server


def test_handle_single_line_feed(client: SocksClient) -> None:
    result = loads(client.send("\n"))
    assert result["message"] == "\n"


def test_handle_single_carriage_return(client: SocksClient) -> None:
    result = loads(client.send("\r"))
    assert result["message"] == "\r"


def test_handle_single_end_of_line(client: SocksClient) -> None:
    result = loads(client.send("\r\n"))
    assert result["message"] == "\r\n"


# Echo tests


@mark.parametrize("string", generate_random_string(num_strings=250, len_strings=75))
def test_echo_250_byte_string(client: SocksClient, string: str) -> None:
    # 250 * 75 = 18750 which exceeds 16384 byte buffer size

    result = loads(client.send(string))
    assert string == result["message"]


@mark.parametrize(
    "string", generate_random_punctuation(num_strings=250, len_strings=75)
)
def test_echo_250_byte_punctuation(client: SocksClient, string: str) -> None:
    # 250 * 75 = 18750 which exceeds 16384 byte buffer size

    result = loads(client.send(string))
    assert string == result["message"]
