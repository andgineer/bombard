"""
Bombard reporter.

Use:
* `log` to add each request result.
* `report` to generate report.
"""
import statistics
from array import array
from copy import deepcopy
from typing import Any, Callable, Dict, MutableSequence, Optional, Set, Union

from bombard import pretty_ns
from bombard.pretty_sz import pretty_sz
from bombard.terminal_colours import red

ARRAY_UINT64 = "Q"
ARRAY_UINT32 = "L"
SUCCESS_GROUP = "success"
FAIL_GROUP = "fail"
GROUPS = [SUCCESS_GROUP, FAIL_GROUP]
TIME = "time"
SIZE = "size"
TIME_DENOMINATOR = 1  # if 1 we store ns.


class Reporter:
    """
    Report bombard's result

    Access to stat data only by log(), filter(), reduce()
    """

    def __init__(
        self,
        time_units: Optional[str] = "ms",
        time_threshold_ms: int = 1,
        success_statuses: Optional[Set[int]] = None,
    ):
        """
        :param time_units: time representation fixed in the units (see names in bombard.pretty_ns)
        :param time_threshold_ms: show times bigger than that in red
        :param success_statuses: set of statuses treated as success
        """
        self.DIMENSIONS: Dict[str, Dict[str, Any]] = {
            TIME: {
                "type": ARRAY_UINT64,
                "pretty_func": self.pretty_time,
            },  # time in ns up to 200 000 days.
            SIZE: {"type": ARRAY_UINT32, "pretty_func": pretty_sz},  # sizes up to 4 Gbytes
        }
        self.STAT_DEFAULT: Dict[str, MutableSequence[Any]] = {
            name: array(params["type"]) for name, params in self.DIMENSIONS.items()
        }

        self.start_ns = pretty_ns.time_ns()

        self.time_units = time_units
        self.time_threshold_ns = time_threshold_ms * 10 ** 6
        self.ok = success_statuses or {200}

        self.stat: Dict[
            str, Dict[int, Dict[str, MutableSequence[Any]]]
        ] = {}  # stat[request type][status]['time'|'size']

    def group_name_by_status(self, status: int) -> str:
        """
        All this statuses should be in GROUPS
        """
        if status in self.ok:
            return SUCCESS_GROUP
        return FAIL_GROUP

    def log(
        self, status: Union[int, str], elapsed: int, request_name: str, response_size: int
    ) -> None:
        """
        Add result to the report

        :param status: HTTP response status
        :param elapsed: Request-Response time, ns
        :param request_name: Request name or None
        :param response_size: Response body size
        """
        if isinstance(status, int):  # do not log exceptions
            self.stat.setdefault(request_name, {}).setdefault(status, deepcopy(self.STAT_DEFAULT))
            self.stat[request_name][status][TIME].append(elapsed // TIME_DENOMINATOR)
            self.stat[request_name][status][SIZE].append(response_size)

    @property
    def total_elapsed_ns(self) -> int:
        return pretty_ns.time_ns() - self.start_ns

    def reduce(
        self,
        reduce_func: Callable[
            [Any], Any
        ],  # actually this is Sized (for len) or Iterable[int] (for sub) but I do not see how to express that for mypy
        dimension_name: str,
        status_group_filter: Optional[str] = None,
        request_name_filter: Optional[str] = None,
    ) -> int:
        """
        Reduce the dimension by group and/or request_name with the reduce_func
        Returns dict {'time':, 'size':}
        """
        result = 0
        for request_name, statuses in self.stat.items():
            if request_name == request_name_filter or request_name_filter is None:
                for status in statuses:
                    if (
                        self.group_name_by_status(status) == status_group_filter
                        or status_group_filter is None
                    ):
                        result += reduce_func(statuses[status][dimension_name])
        return result

    def filter(
        self,
        dimension_name: str,
        status_group_filter: Optional[str] = None,
        request_name_filter: Optional[str] = None,
    ) -> MutableSequence[Any]:
        """
        Filter the dimension by group and/or request_name,
        Returns array with values from dimention_name
        """
        dimension_values: MutableSequence[Any] = array(self.DIMENSIONS[dimension_name]["type"])
        for request_name, statuses in self.stat.items():
            if request_name == request_name_filter or request_name_filter is None:
                for status_name, status in statuses.items():
                    if (
                        self.group_name_by_status(status_name) == status_group_filter
                        or status_group_filter is None
                    ):
                        dimension_values += status[dimension_name]
        return dimension_values

    @staticmethod
    def dimension_stat_report(
        dimension_values: MutableSequence[Union[int, float]],
        pretty_func: Callable[[Union[int, float]], str],
    ) -> str:
        if not dimension_values:
            return ""
        return ", ".join(
            [
                f"Mean: {pretty_func(statistics.mean(dimension_values))}",
                f"min: {pretty_func(min(dimension_values))}",
                f"max: {pretty_func(max(dimension_values))}",
            ]
        )

    def filtered_report(
        self, status_group_filter: Optional[str] = None, request_name_filter: Optional[str] = None
    ) -> str:
        """
        Filter by group and/or request_name.
        Returns report str with stats for all dimensions.
        """
        result = []
        for dimension_name, dimention_descr in self.DIMENSIONS.items():
            dimension_values = self.filter(
                dimension_name, status_group_filter, request_name_filter
            )
            if dimension_values:
                result.append(
                    self.dimension_stat_report(dimension_values, dimention_descr["pretty_func"])
                )
        if not result:
            return "No such requests"
        return "\n".join(result)

    def statuses_report(self, request_name_filter: Optional[str] = None) -> str:
        return ", ".join(
            f"{group} {self.reduce(len, TIME, group, request_name_filter)}" for group in GROUPS
        )

    def pretty_time(self, elapsed: int, paint: bool = True) -> str:
        return self.pretty_ns(elapsed * TIME_DENOMINATOR, paint)

    def pretty_ns(self, elapsed_ns: int, paint: bool = True) -> str:
        result = pretty_ns.pretty_ns(elapsed_ns, self.time_units)
        if elapsed_ns > self.time_threshold_ns and paint:
            return red(result)
        return result

    def report(self) -> str:
        size_sum = self.reduce(sum, SIZE)
        total_ns = self.reduce(sum, TIME)
        total_num = self.reduce(len, TIME)
        elapsed_sec = total_ns / (10 ** 9)
        infinity = chr(0x221E)
        total_line = " ".join(
            [
                f"Got `{total_num}` responses",
                f"in `{self.pretty_time(total_ns, paint=False)}`,",
                f"`{round(total_num / elapsed_sec) if elapsed_sec > 0 else infinity} op/sec`,",
                f"{pretty_sz(size_sum)},",
                f"{pretty_sz(size_sum // elapsed_sec) if elapsed_sec > 0 else infinity}/sec",
            ]
        )
        by_group = []
        for status_group in GROUPS:
            by_group.append(
                f"""#### {status_group}: {self.reduce(len, TIME, status_group)}
{self.filtered_report(status_group)}
"""
            )
        by_group_str = "\n".join(by_group)  # we cannot use "\n" inside f-string
        by_request = []
        for request_name in self.stat:
            by_request.append(
                f"""### {request_name}: {self.statuses_report(request_name)}
{self.filtered_report(None, request_name)}
"""
            )
        by_request_str = "\n".join(by_request)  # we cannot use "\n" inside f-string
        return f"""{total_line}

{by_group_str}

{by_request_str}"""
