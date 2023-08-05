from typing import Any, List

from dekespo_ai_sdk.core.dimensions import Dim2D


class RawDataHandler:
    def __init__(self, raw_data: List[List[Any]]):
        self._raw_data: List[List[Any]] = raw_data
        raw_data_map: List[str] = []
        # TODO: give information from shape2D instead?
        for row_list in self._raw_data:
            # TODO: Find a good way to get maximum character
            # (it should be run once for th map and while adding)
            formatted_row_list = [f"{value: <2}" for value in row_list]
            raw_data_map.append("|".join(formatted_row_list))
        self._raw_data_map: str = "\n".join(raw_data_map)

    def __str__(self):
        return self._raw_data_map

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    @property
    def raw_data(self) -> List[List[Any]]:
        return self._raw_data

    def get_value(self, position: Dim2D) -> Any:
        return self._raw_data[int(position.y)][int(position.x)]

    def set_value(self, position: Dim2D, value: Any):
        self._raw_data[int(position.y)][int(position.x)] = value
