import threading
from dataclasses import dataclass
from typing import List

from dekespo_ai_sdk.core.utils import error_print
from dekespo_ai_sdk.algorithms.graph_search.utils import (
    Node,
    SearchData,
    update_sets,
)


@dataclass
class DepthFirstSearchData(SearchData):
    depth_size: int


class DepthFirstSearch(threading.Thread):
    def __init__(self, input_data: DepthFirstSearchData, runs_with_thread: bool):
        self.input_data = input_data
        self.runs_with_thread = runs_with_thread
        self._closed_set: List[Node] = []

        if self.runs_with_thread:
            threading.Thread.__init__(self)
            self._thread_name = "DFS_thread"
            self._is_done = False
            self._event = threading.Event()
            self._kill = False

    def run(self):
        if not self.runs_with_thread:
            error_print(
                "You should set runs_with_thread as true in order to run this one"
            )
            return
        error_print(f"Running {self._thread_name}")
        self._is_done = False
        self._depth_first_search()
        self._is_done = True
        error_print(f"Finished running {self._thread_name}")

    def run_without_thread(self):
        self._depth_first_search()

    def _depth_first_search(self):
        open_set: List[Node] = [Node(self.input_data.start_point, 0)]
        # TODO: Check the followıng depth level
        while open_set and self.input_data.depth_size > len(self._closed_set):
            if self.runs_with_thread:
                if self._kill:
                    error_print(f"Killed the {self._thread_name} thread")
                    break
                self._event.wait()
            current_node = open_set.pop()
            update_sets(self._closed_set, open_set, current_node, self.input_data)

    def event_set(self):
        self._event.set()

    def event_clear(self):
        self._event.clear()

    # TODO: Use property instead
    def get_closed_set(self) -> List[Node]:
        return self._closed_set

    def is_done(self):
        return self._is_done

    def kill_thread(self):
        self._kill = True
