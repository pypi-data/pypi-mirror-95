""" Methods for test cases involving checking command-line interfaces

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2020-12-21
:Copyright: 2020, Center for Reproducible Biomedical Modeling
:License: MIT
"""

from ..data_model import TestCase
from ..warnings import TestCaseWarning
from biosimulators_utils.simulator.environ import ENVIRONMENT_VARIABLES
import re
import subprocess
import warnings

__all__ = [
    'CliDisplaysHelpInline',
    'CliDescribesSupportedEnvironmentVariablesInline',
    'CliDisplaysVersionInformationInline',
]


class CliDisplaysHelpInline(TestCase):
    """ Test that a command-line interface provides inline help. """

    def eval(self, specifications):
        """ Evaluate a simulator's performance on a test case

        Args:
            specifications (:obj:`dict`): specifications of the simulator to validate

        Raises:
            :obj:`Exception`: if the simulator did not pass the test case
        """
        self.get_simulator_docker_image(specifications)
        image_url = specifications['image']['url']

        result = subprocess.run(['docker', 'run', '--tty', '--rm', image_url],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = result.stdout.decode() if result.stdout else ''
        supported = (
            '-i' in log
            and '-o' in log
        )
        if not supported:
            warnings.warn(('Command-line interfaces should display basic help when no arguments are provided.\n\n'
                           'The command-line interface displayed the following when no argument was provided:\n\n  {}'
                           ).format(log.replace('\n', '\n  ')),
                          TestCaseWarning)

        result = subprocess.run(['docker', 'run', '--tty', '--rm', image_url, '-h'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = result.stdout.decode() if result.stdout else ''
        supported = (
            'arguments' in log
            and '-i' in log
            and '--archive' in log
            and '-o' in log
            and '--out-dir' in log
        )
        if not supported:
            warnings.warn(('Command-line interface should support the `-h` option for displaying help inline.\n\n'
                           'The command-line interface displayed the following when executed with `-h`:\n\n  {}'
                           ).format(log.replace('\n', '\n  ')),
                          TestCaseWarning)

        result = subprocess.run(['docker', 'run', '--tty', '--rm', image_url, '--help'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = result.stdout.decode() if result.stdout else ''
        supported = (
            'arguments' in log
            and '-i' in log
            and '--archive' in log
            and '-o' in log
            and '--out-dir' in log
        )
        if not supported:
            warnings.warn(('Command-line interface should support the `--help` option for displaying help inline.\n\n'
                           'The command-line interface displayed the following when executed with `--help`:\n\n  {}'
                           ).format(log.replace('\n', '\n  ')),
                          TestCaseWarning)


class CliDescribesSupportedEnvironmentVariablesInline(TestCase):
    """ Test that the inline help for a command-line interface describes the environment variables that the
    simulator supports.
    """

    def eval(self, specifications):
        """ Evaluate a simulator's performance on a test case

        Args:
            specifications (:obj:`dict`): specifications of the simulator to validate

        Raises:
            :obj:`Exception`: if the simulator did not pass the test case
        """
        self.get_simulator_docker_image(specifications)
        image_url = specifications['image']['url']

        result = subprocess.run(['docker', 'run', '--tty', '--rm', image_url, '-h'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = result.stdout.decode() if result.stdout else ''

        potentially_missing_env_vars = []
        for var in ENVIRONMENT_VARIABLES.values():
            if var.name not in log:
                potentially_missing_env_vars.append(var.name)

        if potentially_missing_env_vars:
            msg = ('The inline help for a command-line interface for a simulation tool should describe the '
                   'environment variables that the simulation tool supports.\n\n'
                   'The command-line interface does not describe the following standard environment '
                   'variables recognized by BioSimulators:\n  - {}\n\n'
                   'If the simulation tool implements these variables, they should be described in the inline help for '
                   'its command-line interface.\n\n'
                   'Note, support for these environment variables is optional. Simulation tools are not required to support '
                   'these variables.'
                   ).format('\n  - '.join("'" + var + "'" for var in sorted(potentially_missing_env_vars)))
            warnings.warn(msg, TestCaseWarning)


class CliDisplaysVersionInformationInline(TestCase):
    """ Test that a command-line interface provides version information inline. """

    def eval(self, specifications):
        """ Evaluate a simulator's performance on a test case

        Args:
            specifications (:obj:`dict`): specifications of the simulator to validate

        Raises:
            :obj:`Exception`: if the simulator did not pass the test case
        """
        self.get_simulator_docker_image(specifications)
        image_url = specifications['image']['url']

        result = subprocess.run(['docker', 'run', '--tty', '--rm', image_url, '-v'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = result.stdout.decode() if result.stdout else ''
        supported = re.search(r'\d+\.\d+', log)
        if not supported:
            warnings.warn(('Command-line interface should support the `-v` option for displaying version information inline.\n\n'
                           'The command-line interface displayed the following when executed with `-v`:\n\n  {}'
                           ).format(log.replace('\n', '\n  ')),
                          TestCaseWarning)

        result = subprocess.run(['docker', 'run', '--tty', '--rm', image_url, '--version'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = result.stdout.decode() if result.stdout else ''
        supported = re.search(r'\d+\.\d+', log)
        if not supported:
            warnings.warn(('Command-line interface should support the `--version` option for displaying version information inline.\n\n'
                           'The command-line interface displayed the following when executed with `--version`:\n\n  {}'
                           ).format(log.replace('\n', '\n  ')),
                          TestCaseWarning)
