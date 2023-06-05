import xml.etree.ElementTree as ET

from ..utils.rss import get_feed, get_items


def test_get_items():
    assert type(get_items()) == list

def test_get_items_2():
    items = get_items()
    for item in items:
        assert type(item) == dict

def test_get_feed():
    assert isinstance(get_feed(), ET.Element)
