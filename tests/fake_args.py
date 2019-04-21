"""
Fake args that we can pass to bombard to test it.
This is AttrDict so you can use something like that
>>> args = FakeArgs(init=True)
>>> args.init
True
"""
from bombard.attr_dict import AttrDict
from bombard.args import CAMPAIGN_FILE_NAME, THRESHOLD, TIMEOUT, THREADS_NUM


class FakeArgs(AttrDict):
    threads = THREADS_NUM
    timeout = TIMEOUT
    ms = False
    threshold = THRESHOLD
    quiet = False
    dry = False
    verbose = False
    quiet = False
    log = None
    example = None
    init = False
    examples = False
    file_name = CAMPAIGN_FILE_NAME
    version = False
    supply={}
    repeat=1
