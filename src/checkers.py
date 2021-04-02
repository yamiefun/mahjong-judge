from tile import Tiles
from tile import InvalidOperationError
from tile import TILE_PATTERN
import re
import logging


class UnknownInputError(Exception):
    pass

class BaseChecker:
    yakuman_type = None   # 役滿牌型

    def __init__(self):
        assert self.yakuman_type
        self.logger = logging.getLogger(__name__)
        self.init_pools()

    def init_pools(self):
        kwargs = self.get_init_pools_kwargs()
        self._pools = Tiles(**kwargs)

    def get_init_pools_kwargs(self):
        return {}

    def parse_input(self, input_value):
        if input_value == 'reset':
            self.init_pools()
        else:
            matched = re.match(TILE_PATTERN, input_value)
            if matched:
                try:
                    self._pools.remove_tile(**matched.groupdict())
                except InvalidOperationError:
                    pass
            else:
                raise UnknownInputError(f'Unknown input {input_value}')
        possibility = list(self._pools.win_combinations)
        if possibility:
            self.logger.info("Still possible to {self.yakuman_type}.")
            self.logger.info(f"Ex: {possibility}")
        else:
            self.logger.info("Not enough for {self.yakuman_type}.")


class RyuisoChecker(BaseChecker):
    yakuman_type = 'ryuiso'

    def get_init_pool_kwargs(self):
        return {
            'sou': '23468' * 4,
            'tsu': '6' * 4
        }
