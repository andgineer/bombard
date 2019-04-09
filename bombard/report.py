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


class Reporter:
    """
    Report bombard's result
    """
    def __init__(self):
        self.start_ns = time_ns()

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

    @staticmethod
    def report_dimension(a: array):
        if len(a) == 0:
            return '`...no requests...`'
        return ', '.join([
            f'Mean: {pretty_ns(statistics.mean(a))}',
            f'min: {pretty_ns(min(a))}',
            f'max: {pretty_ns(max(a))}',
        ])

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

    def report(self):
        by_name = []
        for name, stat in self.stat_by_name.items():
            by_name.append(f'### {name}\n' + self.report_dimension(stat))
        by_name = '\n\n'.join(by_name)
        size_sum = sum(self.stat_success_size) + sum(self.stat_fail_size)
        elapsed_sec = self.total_elapsed_ns / (10 ** 9)
        total_line = ' '.join([
            f'Got `{self.count}` responses',
            f'in `{pretty_ns(self.total_elapsed_ns)}`,',
            f'`{round(self.count / elapsed_sec)} op/sec`,',
            f'{pretty_sz(size_sum)},',
            f'{pretty_sz(size_sum // elapsed_sec) if elapsed_sec > 0 else 0}/sec',
        ])
        return f'''{total_line}
        
## success:
{self.report_section(True)}

## fail:
{self.report_section(False)}

## by request name:
{by_name}'''



