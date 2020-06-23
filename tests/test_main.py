import collections
import logging

from cvescan import __main__ as main
from cvescan.output_formatters import (
    cli_output_formatter,
    cve_output_formatter,
    nagios_output_formatter,
)

Args = collections.namedtuple("Args", "silent, verbose")


class MockOpt:
    def __init__(self):
        self.download_uct_db_file = False
        self.db_file = "tests/assets/cache_uct.json"
        self.cve = False
        self.nagios_mode = False


class MockDownloadCache:
    def get_from_url(self, url):
        return {"metadata": {}, "data": {"CVE-2019-1000": "0"}}


def test_set_output_verbosity_info():
    args = Args(silent=False, verbose=False)
    logger = main.set_output_verbosity(args)

    assert logger.level == logging.INFO


def test_set_output_verbosity_silent():
    args = Args(silent=True, verbose=False)
    logger = main.set_output_verbosity(args)
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.NullHandler)


def test_set_output_verbosity_debug():
    args = Args(silent=False, verbose=True)
    logger = main.set_output_verbosity(args)

    assert logger.level == logging.DEBUG


def test_load_uct_data_file():
    opt = MockOpt()
    opt.download_uct_db_file = False

    download_cache = MockDownloadCache()

    data = main.load_uct_data(opt, download_cache)

    assert len(data.keys()) == 3
    assert "CVE-2020-1000" in data
    assert "CVE-2020-1001" in data
    assert "CVE-2020-1002" in data


def test_load_uct_data_cache():
    opt = MockOpt()
    opt.download_uct_db_file = True

    download_cache = MockDownloadCache()

    data = main.load_uct_data(opt, download_cache)

    assert len(data.keys()) == 1
    assert "CVE-2019-1000" in data


def test_cve_output_formatter():
    opt = MockOpt()
    opt.cve = True

    output_formatter = main.load_output_formatter(opt)

    assert isinstance(output_formatter, cve_output_formatter.CVEOutputFormatter)


def test_nagios_output_formatter():
    opt = MockOpt()
    opt.nagios_mode = True

    output_formatter = main.load_output_formatter(opt)

    assert isinstance(output_formatter, nagios_output_formatter.NagiosOutputFormatter)


def test_cli_output_formatter():
    opt = MockOpt()
    opt.cve = False
    opt.nagios_mode = False

    output_formatter = main.load_output_formatter(opt)

    assert isinstance(output_formatter, cli_output_formatter.CLIOutputFormatter)
