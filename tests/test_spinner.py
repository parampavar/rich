import pytest

from rich.console import Console
from rich.measure import Measurement
from rich.spinner import Spinner


def test_spinner_create():
    Spinner("dots")
    with pytest.raises(KeyError):
        Spinner("foobar")


def test_spinner_render():
    time = 0.0

    def get_time():
        nonlocal time
        return time

    console = Console(
        width=80, color_system=None, force_terminal=True, get_time=get_time
    )
    console.begin_capture()
    spinner = Spinner("dots", "Foo")
    console.print(spinner)
    time += 80 / 1000
    console.print(spinner)
    result = console.end_capture()
    print(repr(result))
    expected = "⠋ Foo\n⠙ Foo\n"
    assert result == expected


def test_spinner_update():
    time = 0.0

    def get_time():
        nonlocal time
        return time

    console = Console(width=80, force_terminal=True, get_time=get_time)
    console.begin_capture()
    spinner = Spinner("dots", "Foo")
    console.print(spinner)
    spinner.update(text="Bar", style="green", speed=2)
    time += 80 / 1000
    console.print(spinner)
    time += 80 / 1000
    console.print(spinner)
    result = console.end_capture()
    print(repr(result))
    expected = f"⠋ Foo\n\x1b[32m⠙\x1b[0m Bar\n\x1b[32m⠸\x1b[0m Bar\n"
    assert result == expected


def test_rich_measure():
    console = Console(width=80, color_system=None, force_terminal=True)
    spinner = Spinner("dots", "Foo")
    min_width, max_width = Measurement.get(console, console.options, spinner)
    assert min_width == 3
    assert max_width == 5
