import argparse
import configparser
import fnmatch
import os
import re
import sys
from configparser import SectionProxy
from glob import glob
from typing import Any, Dict, Iterator, List, Optional, Pattern, Sequence, Set, Tuple, Union  # noqa: WPS235

from modularhistory.utils import linting

CONFIG_FILE = 'setup.cfg'

ConfigFileSection = Dict[str, object]
ErrorCodeSet = Set[str]
MultiOptions = Union[Sequence[str], str]
OptionsUpdate = Tuple[Optional[str], ConfigFileSection]
PathPatternList = List[Pattern]
PatternList = List[Pattern]
PerFileIgnore = Tuple[str, Set[str]]

ALL = None

# choose an exit that does not conflict with mypy's
PARSING_FAIL = 100

GLOBAL_ONLY_OPTIONS = [
    'color',
    'show_ignored',
    'daemon',
    'exclude',
]

PER_MODULE_OPTIONS = [
    'select',
    'ignore',
    'warn',
    'include',
    'error_filters',
    'warning_filters',
]


class LinterOptions:
    """Options for linters."""

    # error codes:
    select: Optional[ErrorCodeSet] = None
    ignore: Optional[ErrorCodeSet] = None
    warn: Optional[ErrorCodeSet] = None

    # paths:
    include: Optional[PathPatternList] = None
    exclude: Optional[PathPatternList] = None

    # per-file ignores:
    per_file_ignores: Optional[List[PerFileIgnore]] = None

    # messages:
    error_filters: Optional[PatternList] = None
    warning_filters: Optional[PatternList] = None

    def __init__(self):
        """Constructs linter options."""
        self.select = ALL
        self.ignore = set()
        self.warn = set()
        self.include = []
        self.exclude = []
        self.per_file_ignores = []
        self.error_filters = []
        self.warning_filters = []

    def __str__(self):
        """TODO: write docstring."""
        return f'{self.__dict__}'

    def is_excluded_path(self, path: str) -> bool:
        """TODO: write docstring."""
        return linting.match(self.exclude, path)

    def is_included_path(self, path: str) -> bool:
        """TODO: write docstring."""
        return linting.match(self.include, path)

    def error_is_ignored_in_file(self, filename: str, error_code: str):
        """Return True if an error is specifically ignored for the given filename."""
        for pattern, error_codes in self.per_file_ignores:
            if filename in glob(pattern) and error_code in error_codes:
                return True
        return False

    def get_message_level(self, message, error_code, filename) -> Optional[str]:
        """Returns a modified message level based on specified options."""
        error_is_ignored = any([
            linting.match(self.error_filters, message),
            self.ignore is ALL,
            error_code in self.ignore,
            self.error_is_ignored_in_file(filename=filename, error_code=error_code)
        ])
        # If error is to be ignored
        if error_is_ignored:
            return None
        # If we have specified something to check for
        elif self.select and error_code in self.select:
            return 'error'
        # If we have specified something to warn (ignore overrides this)
        elif self.warn is ALL or error_code in self.warn:
            return 'warning'
        # If checking everything
        elif self.select is ALL:
            return 'error'
        return None


PerModuleOptions = List[Tuple[str, LinterOptions]]


def _parse_multi_options(options: MultiOptions, split_token: str = ',') -> List[str]:  # noqa: S107
    """Split and strip and discard empties."""
    if isinstance(options, str):
        options = options.strip()
        # Split the options by the specified split token, or by newlines
        if split_token in options:
            parsed_options = options.split(split_token)
        else:
            parsed_options = options.split('\n')
    else:
        parsed_options = options
    return [option.strip() for option in parsed_options if option.strip()]


def _glob_to_regex(file_glob):
    """."""
    return re.compile(fnmatch.translate(file_glob))


def _glob_list(globs: MultiOptions) -> PathPatternList:
    """."""
    return [_glob_to_regex(file_glob) for file_glob in _parse_multi_options(globs)]


def _per_file_ignores_list(per_file_ignores: MultiOptions) -> List[PerFileIgnore]:
    per_file_ignores_list = []
    entries = _parse_multi_options(per_file_ignores, split_token='\n')  # noqa: S106
    for entry in entries:
        pattern, codes = entry.split(':')
        error_codes = {code.strip() for code in codes.split(',')}
        per_file_ignores_list.append((pattern.strip(), error_codes))
    return per_file_ignores_list


def _regex_list(patterns: MultiOptions) -> List[Pattern]:
    """."""
    return [re.compile(pattern) for pattern in _parse_multi_options(patterns)]


def _error_code_set(error_codes: MultiOptions) -> Optional[Set[str]]:
    """."""
    error_code_set = set()
    for res in _parse_multi_options(error_codes):
        if res == '*':
            return None
        else:
            error_code_set.add(res)
    return error_code_set


option_types = {
    'select': _error_code_set,
    'ignore': _error_code_set,
    'warn': _error_code_set,
    'args': _parse_multi_options,
    'include': _glob_list,
    'exclude': _glob_list,
    'per_file_ignores': _per_file_ignores_list,
    'error_filters': _regex_list,
    'warning_filters': _regex_list,
}


class ConfigFileOptionsParser:
    """TODO: add docstring."""

    report_unrecognized_options: bool = True

    def __init__(self, script_name: str):
        """
        Constructs the config file options parser.

        Sets script_name, which is used to determine which section of the config file to read.
        """
        self.script_name = script_name

    def apply(
        self,
        options: LinterOptions,
        module_options: List[Tuple[str, LinterOptions]]
    ) -> None:
        """TODO: add docstring."""
        options_cls = options.__class__
        for config_section_key, updates in self.extract_updates(options):
            if updates:
                if config_section_key is None:
                    opt = options
                else:
                    opt = options_cls()
                    module_options.append((config_section_key, opt))
                for option_key, option_value in updates.items():
                    setattr(opt, option_key.replace('-', '_'), option_value)

    def _parse_option(
        self,
        option_key: str,
        option_value: str,
        template: LinterOptions,
        section: SectionProxy
    ) -> Any:
        template_key = option_key.replace('-', '_')
        option_type: Any = option_types.get(template_key)
        processed_value: Any
        if not option_type:
            dv = getattr(template, template_key, None)
            if dv is None:
                if self.report_unrecognized_options:
                    print(f'Unrecognized option: {option_key} = {option_value}', file=sys.stderr)
                return None
            option_type = type(dv)
        try:
            if option_type is bool:
                processed_value = section.getboolean(template_key)
            elif callable(option_type):
                processed_value = option_type(section.get(option_key))
            else:
                print(f'Cannot determine what type {option_key} should have', file=sys.stderr)
                return None
        except (ValueError, argparse.ArgumentTypeError) as error:
            print(f'{option_key}: {error}', file=sys.stderr)
            return None
        return processed_value

    def _parse_section(
        self,
        template: LinterOptions,
        section: SectionProxy
    ) -> ConfigFileSection:
        parsed_section: ConfigFileSection = {}
        for option_key, option_value in section.items():
            processed_value = self._parse_option(option_key, option_value, template, section)
            if processed_value:
                parsed_section[option_key] = processed_value
        return parsed_section

    def extract_updates(self, options: LinterOptions) -> Iterator[OptionsUpdate]:
        """TODO: add docstring."""
        config_file = os.path.expanduser(CONFIG_FILE)
        parser = configparser.RawConfigParser()
        if not os.path.exists(config_file):
            raise EnvironmentError(f'No config file named {CONFIG_FILE} exists.')
        try:
            parser.read(config_file)
        except configparser.Error as error:
            print(f'{config_file}: {error}', file=sys.stderr)

        script_name = self.script_name
        if script_name in parser:
            section = parser[script_name]  # noqa: WPS529
            yield None, self._parse_section(options, section)
        else:
            print(f'No [{self.script_name}] section in config file', file=sys.stderr)

        for name, section in parser.items():
            if name.startswith('mypyrun-'):
                prefix = f'{CONFIG_FILE}: [{name}]'
                updates = self._parse_section(options, section)
                if set(updates).intersection(GLOBAL_ONLY_OPTIONS):
                    print(
                        f'{prefix}: Per-module sections should only specify per-module flags '
                        f'({", ".join(sorted(set(updates).intersection(GLOBAL_ONLY_OPTIONS)))})',
                        file=sys.stderr
                    )
                    updates = {
                        option_key: option_value for option_key, option_value in updates.items()
                        if option_key in PER_MODULE_OPTIONS
                    }
                globs = name[8:]
                for file_glob in globs.split(','):
                    yield file_glob, updates
