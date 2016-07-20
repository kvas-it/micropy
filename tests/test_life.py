import life
import pytest


@pytest.fixture(scope='function')
def gol():
    data = [[0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1]]
    return life.GameOfLife(data)


def test_neighbour_counts(gol):
    expect = [[2, 2, 4, 3, 3],
              [1, 1, 4, 3, 2],
              [1, 2, 3, 2, 2],
              [1, 2, 5, 5, 4],
              [1, 1, 3, 4, 3]]
    assert gol.neighbour_counts() == expect


def test_step(gol):
    expect = [[0, 0, 0, 1, 1],
              [0, 0, 0, 1, 0],
              [0, 0, 1, 1, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 1, 0, 1]]
    gol.step()
    assert gol.data == expect


def test_image(gol):
    expect = '00090:09000:00990:00090:00999'
    assert gol.gen_image().data == expect
    gol.move(2, 2)
    moved_expect = '99000:09000:99900:09000:00009'
    assert gol.gen_image().data == moved_expect
    gol.move(-2, -2)
    assert gol.gen_image().data == expect
    gol.move(-3, -3)
    assert gol.gen_image().data == moved_expect


def is_alive(gol):
    assert gol.is_alive()
    gol.data = [[0] * 5] * 5
    assert not gol.is_alive()
