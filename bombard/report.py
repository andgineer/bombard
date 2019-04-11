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
from typing import Optional
from bombard.terminal_colours import red
from collections import Sequence


class Reporter:
    """
    Report bombard's result
    """
    def __init__(self, time_units: Optional[str] = None, time_threshold_ms: Optional[int] = None):
        """
        :param time_units: fix all time in the units (see names in pretty_ns)
        :param time_threshold_ms: show times bigger than that in red
        """
        self.start_ns = time_ns()

        self.time_units = time_units
        self.time_threshold_ns = time_threshold_ms * 10**6

        self.stat_success_time = array('Q')
        self.stat_fail_time = array('Q')
        self.stat_by_name = {}

        self.stat_success_size = array('Q')
        self.stat_fail_size = array('Q')

    def log(self, success, elapsed, request_name, response_size):
        """
        Add result to the report

        :param success: Successful response
        :param elapsed: Request-Response time, ns
        :param request_name: Request name or None
        :param response_size: Response body size
        """
        if request_name is not None:
            if request_name not in self.stat_by_name:
                self.stat_by_name[request_name] = array('Q')
            self.stat_by_name[request_name].append(elapsed)
        if success:
            self.stat_success_time.append(elapsed)
            self.stat_success_size.append(response_size)
        else:
            self.stat_fail_time.append(elapsed)
            self.stat_fail_size.append(response_size)

    @property
    def total_elapsed_ns(self):
        return time_ns() - self.start_ns

    @property
    def count(self):
        """ How many responses added to the reporter """
        return len(self.stat_success_time) + len(self.stat_fail_time)

    def report_dimension(self, a: array):
        if len(a) == 0:
            return '`...no requests...`'
        return ', '.join([
            f'Mean: {self.pretty_ns(statistics.mean(a))}',
            f'min: {self.pretty_ns(min(a))}',
            f'max: {self.pretty_ns(max(a))}',
        ])

    def pretty_ns(self, elapsed_ns: int):
        result = pretty_ns(elapsed_ns, self.time_units)
        if elapsed_ns > self.time_threshold_ns:
            return red(result)
        else:
            return result

    def report_section(self, success: bool):
        if success:
            stat = self.stat_success_time
            if len(stat) == 0:
                return '`...no success...`'
        else:
            stat = self.stat_fail_time
            if len(stat) == 0:
                return '`...no fails...`'
        return self.report_dimension(stat)

    def parenthesized(self, seq: Sequence):
        return '(' + str(len(seq)) + ')' if seq else ''

    def report(self):
        by_name = []
        for name, stat in self.stat_by_name.items():
            by_name.append(f'### {name} {self.parenthesized(stat)}\n' + self.report_dimension(stat))
        by_name = '\n\n'.join(by_name)
        size_sum = sum(self.stat_success_size) + sum(self.stat_fail_size)
        total_ns = self.total_elapsed_ns
        elapsed_sec = total_ns / (10 ** 9)
        total_line = ' '.join([
            f'Got `{self.count}` responses',
            f'in `{self.pretty_ns(total_ns)}`,',
            f'`{round(self.count / elapsed_sec)} op/sec`,',
            f'{pretty_sz(size_sum)},',
            f'{pretty_sz(size_sum // elapsed_sec) if elapsed_sec > 0 else 0}/sec',
        ])
        return f'''{total_line}
        
## success {self.parenthesized(self.stat_success_time)}
{self.report_section(True)}

## fail {self.parenthesized(self.stat_fail_time)}
{self.report_section(False)}

## by request name:
{by_name}'''



