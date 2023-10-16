import os
from PIL import Image
from utils.processing import increase_framerate, reverse


def test_increase_framerate():
    gif_path = "tests/fixtures/sample.gif"
    output_path = "tests/fixtures/output.gif"

    gif = Image.open(gif_path)
    increase_framerate(gif, output_path, factor=2)

    # would be nice to check the duration etc.
    assert os.path.exists(output_path)
    os.remove(output_path)


def test_reverse():
    gif_path = "tests/fixtures/sample.gif"
    output_path = "tests/fixtures/reversed.gif"

    gif = Image.open(gif_path)
    reverse(gif, output_path)

    # would be nice to check order of frames
    assert os.path.exists(output_path)
    os.remove(output_path)