import pytest
from barista.utils.sequential_queue import SequentialQueue
import threading


@pytest.fixture
def sq():
    return SequentialQueue()


def test_add_and_get_next(sq):
    sq.add("Item 1", 1)
    sq.add("Item 2", 2)
    assert sq.get_next() == "Item 1"
    assert sq.get_next() == "Item 2"


def test_ordering(sq):
    sq.add("Item 2", 2)
    sq.add("Item 1", 1)
    assert sq.get_next() == "Item 1"
    assert sq.get_next() == "Item 2"


def test_mark_end(sq):
    sq.add("Item 1", 1)
    sq.mark_end(2)
    assert sq.get_next() == "Item 1"
    assert sq.get_next() is None
