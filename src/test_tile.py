from src.tile import Tiles
from src.tile import InvalidOperationError
from src.tile import UnknownKindError
import pytest


class TestTiles:

    def test_init_tiles(self):
        tiles = Tiles(sou='112', pin='334')
        assert tiles.get('sou') == '112'
        assert tiles.get('pin') == '334'

        assert tiles._counter.get('sou') == {
            '1': 2,
            '2': 1
        }

        assert tiles._counter.get('pin') == {
            '3': 2,
            '4': 1
        }

    class TestRemoveTile:

        def test_remove_tile_in_tiles(self):
            tiles = Tiles(sou='112', pin='334')

            # remove 1sou
            tiles.remove_tile(kind='sou', tile_id='1')

            assert tiles.get('sou') == '12'
            # no change for pins
            assert tiles.get('pin') == '334'

            assert tiles._counter.get('sou') == {
                '1': 1,
                '2': 1
            }

            assert tiles._counter.get('pin') == {
                '3': 2,
                '4': 1
            }

        def test_remove_tile_not_in_tiles(self):
            tiles = Tiles(sou='112', pin='334')

            with pytest.raises(InvalidOperationError) as error:
                # remove 1man which is not in tiles
                tiles.remove_tile(kind='man', tile_id='1')

            assert str(error.value) == "Can't remove 1man from 112sou334pin"

        def test_remove_unknown_tile(self):
            tiles = Tiles(sou='112', pin='334')

            with pytest.raises(UnknownKindError) as error:
                # remove 1man which is not in tiles
                tiles.remove_tile(kind='unknown', tile_id='1')

            assert str(error.value) == "Unknown kind unknown"

    class TestGenerateWinCombinations:

        def test_without_fourteen_tiles(self):
            tiles = Tiles(sou='111', pin='333')
            assert len(list(tiles.win_combinations)) == 0

        def test_exact_one_combination(self):
            tiles = Tiles(sou='111222', pin='333444', man='22')
            combinations = list(tiles.win_combinations)

            assert len(combinations) == 1
            assert combinations[0] == '111222sou22man333444pin'

        def test_multiple_combination(self):
            tiles = Tiles(sou='111222', pin='333444', man='22', tsu='11')
            combinations = sorted(list(tiles.win_combinations))

            assert len(combinations) == 2
            assert combinations[0] == '111222sou22man333444pin'
            assert combinations[1] == '111222sou333444pin11tsu'
