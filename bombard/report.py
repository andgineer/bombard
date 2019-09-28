"""
Bombard reporter.

Use:
* `log` to add each request result.
* `report` to generate report.
"""
from bombard.pretty_ns import time_ns, pretty_ns
from array import array
import statistics
from bombard.pretty_sz import pretty_sz
from bombard.terminal_colours import red
from copy import deepcopy


ARRAY_UINT64 = 'Q'
SUCCESS_GROUP = 'success'
FAIL_GROUP = 'fail'
GROUPS = [SUCCESS_GROUP, FAIL_GROUP]
DIMENSIONS = ['time', 'size']
STAT_DEFAULT = {
    name: array(ARRAY_UINT64) for name in DIMENSIONS
}


class Reporter:
    """
    Report bombard's result
    """
    def __init__(
            self,
            time_units: str,
            time_threshold_ms: int,
            success_statuses: dict
    ):
        """
        :param time_units: fix all time in the units (see names in pretty_ns)
        :param time_threshold_ms: show times bigger than that in red
        :param success_statuses: dict of statuses treated as success
        """
        self.start_ns = time_ns()

        self.time_units = time_units
        self.time_threshold_ns = time_threshold_ms * 10**6
        self.ok = success_statuses

        self.stat = {}  # stat[request type][status]

    def group_name_by_status(self, status):
        """
        All this statuses should be in GROUPS
        """
        if status in self.ok:
            return SUCCESS_GROUP
        else:
            return FAIL_GROUP

    def log(self, status, elapsed, request_name, response_size):
        """
        Add result to the report

        :param status: HTTP response status
        :param elapsed: Request-Response time, ns
        :param request_name: Request name or None
        :param response_size: Response body size
        """
        self.stat.setdefault(request_name, {}).setdefault(status, deepcopy(STAT_DEFAULT))
        self.stat[request_name][status]['time'].append(elapsed)
        self.stat[request_name][status]['size'].append(response_size)

    @property
    def total_elapsed_ns(self):
        return time_ns() - self.start_ns

    def reduce(
            self,
            reduce_func,
            status_group_filter: str = None,
            request_name_filter: str = None
    ) -> dict:
        """
        Reduce by group and/or request_name with the reduce_func
        Returns dict {'time':, 'size':}
        """
        result = {
            name: 0 for name in DIMENSIONS
        }
        for request_name in self.stat:
            if request_name == request_name_filter or request_name_filter is None:
                for status in self.stat[request_name]:
                    if self.group_name_by_status(status) == status_group_filter or status_group_filter is None:
                        for dimension in DIMENSIONS:
                            result[dimension] += reduce_func(self.stat[request_name][status][dimension])
        return result

    def filter_dimension(
            self,
            dimension_name: str,
            status_group_filter: str = None,
            request_name_filter: str = None
    ) -> array:
        """
        Filter by group and/or request_name,
        Returns array with values from dimention_name
        """
        dimension = array(ARRAY_UINT64)
        for request_name in self.stat:
            if request_name == request_name_filter or request_name_filter is None:
                for status in self.stat[request_name]:
                    if self.group_name_by_status(status) == status_group_filter or status_group_filter is None:
                        dimension += self.stat[request_name][status][dimension_name]
        return dimension

    @staticmethod
    def dimension_stat_report(dimension_values: array, pretty_func) -> str:
        if not dimension_values:
            return ''
        return ', '.join([
            f'Mean: {pretty_func(statistics.mean(dimension_values))}',
            f'min: {pretty_func(min(dimension_values))}',
            f'max: {pretty_func(max(dimension_values))}',
        ])

    def filtered_report(
            self,
            status_group_filter: str = None,
            request_name_filter: str = None
    ) -> str:
        """
        Filter by group and/or request_name.
        Returns report str with stats for all dimensions.
        """
        result = []
        for dimension_name in DIMENSIONS:
            dimension = self.filter_dimension(dimension_name, status_group_filter, request_name_filter)
            if dimension:
                result.append(
                    self.dimension_stat_report(
                        dimension,
                        self.pretty_ns if 'time' in dimension_name else pretty_sz
                    )
                )
        if not result:
            return 'No such requests'
        return '\n'.join(result)

    def statuses_report(self, request_name_filter: str = None) -> str:
        return ', '.join([f'{group} {self.reduce(len, group, request_name_filter)["time"]}'
                          for group in GROUPS])

    def pretty_ns(self, elapsed_ns: int):
        result = pretty_ns(elapsed_ns, self.time_units)
        if elapsed_ns > self.time_threshold_ns:
            return red(result)
        else:
            return result

    def report(self):
        total_sum = self.reduce(sum)
        size_sum = total_sum['size']
        total_ns = total_sum['time']
        total_num = self.reduce(len)['time']
        elapsed_sec = total_ns / (10 ** 9)
        total_line = ' '.join([
            f'Got `{total_num}` responses',
            f'in `{pretty_ns(total_ns)}`,',
            f'`{round(total_num / elapsed_sec)} op/sec`,',
            f'{pretty_sz(size_sum)},',
            f'{pretty_sz(size_sum // elapsed_sec) if elapsed_sec > 0 else 0}/sec',
        ])
        by_group = []
        for status_group in GROUPS:
            by_group.append(f'''#### {status_group}: {self.reduce(len, status_group)['time']} 
{self.filtered_report(status_group)}
''')
        by_group = '\n'.join(by_group)
        by_request = []
        for request_name in self.stat:
            by_request.append(f'''### {request_name}: {self.statuses_report(request_name)}
{self.filtered_report(None, request_name)}
''')
        by_request = '\n'.join(by_request)
        return f'''{total_line}
        
{by_group}

{by_request}'''
