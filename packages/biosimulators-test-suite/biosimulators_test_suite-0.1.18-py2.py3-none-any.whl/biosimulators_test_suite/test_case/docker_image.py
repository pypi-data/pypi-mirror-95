""" Methods for test cases involving checking Docker images

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2020-12-21
:Copyright: 2020, Center for Reproducible Biomedical Modeling
:License: MIT
"""

from ..data_model import TestCase
from ..warnings import TestCaseWarning
from biosimulators_utils.simulator.environ import ENVIRONMENT_VARIABLES
import warnings

__all__ = [
    'DefaultUserIsRoot',
    'DeclaresSupportedEnvironmentVariables',
    'HasOciLabels',
    'HasBioContainersLabels',
]


class DefaultUserIsRoot(TestCase):
    """ Test that the default user of a Docker image is root """

    def eval(self, specifications, expected_user=(None, '', '0')):
        """ Evaluate a simulator's performance on a test case

        Args:
            specifications (:obj:`dict`): specifications of the simulator to validate
            expected_user (:obj:`tuple`, optional): expected user

        Raises:
            :obj:`Exception`: if the simulator did not pass the test case
        """
        image = self.get_simulator_docker_image(specifications)
        user = image.attrs['Config']['User']
        if user not in expected_user:
            msg = ("The default user for the Docker image is `{}`. For compatability with Singularity, "
                   "Docker images for simulators should not declare default users (`USER`) other than root. "
                   "Compatability with Singularity is important for using the image on HPC systems, including "
                   "the infrastructure used by runBioSimulations and BioSimulations.\n\n"
                   "More information:\n"
                   "  https://biosimulators.org/standards/simulator-images\n"
                   "  https://sylabs.io/guides/3.7/user-guide/singularity_and_docker.html#best-practices"
                   ).format(user)
            warnings.warn(msg, TestCaseWarning)


class DeclaresSupportedEnvironmentVariables(TestCase):
    """ Test if a Docker image declares the environment variables that is supports """

    def eval(self, specifications):
        """ Evaluate a simulator's performance on a test case

        Args:
            specifications (:obj:`dict`): specifications of the simulator to validate

        Raises:
            :obj:`Exception`: if the simulator did not pass the test case
        """
        image = self.get_simulator_docker_image(specifications)
        expected_env_vars = set(var.name for var in ENVIRONMENT_VARIABLES.values())
        env_vars = set(key_val.partition('=')[0] for key_val in image.attrs['Config']['Env'])
        potentially_missing_env_vars = sorted(expected_env_vars.difference(env_vars))
        if potentially_missing_env_vars:
            msg = ('Docker images for simulation tools should declare the environment variables that they support.\n\n'
                   'The Docker image does not declare the following standard environment '
                   'variables recognized by BioSimulators:\n  - {}\n\n'
                   'If the simulation tool implements these variables, they should be declared in the Dockerfile for '
                   'the Docker image for the simulator.\n\n'
                   'Note, support for these environment variables is optional. Simulation tools are not required to support '
                   'these variables.'
                   ).format('\n  - '.join("'" + var + "'" for var in potentially_missing_env_vars))
            warnings.warn(msg, TestCaseWarning)


class HasOciLabels(TestCase):
    """ Test that a Docker image has Open Container Initiative (OCI) labels
    with metadata about the image
    """
    EXPECTED_LABELS = [
        'org.opencontainers.image.authors',
        'org.opencontainers.image.description',
        'org.opencontainers.image.documentation',
        'org.opencontainers.image.licenses',
        'org.opencontainers.image.revision',
        'org.opencontainers.image.source',
        'org.opencontainers.image.title',
        'org.opencontainers.image.url',
        'org.opencontainers.image.vendor',
        'org.opencontainers.image.version',
        'org.opencontainers.image.created',
    ]

    def eval(self, specifications):
        """ Evaluate a simulator's performance on a test case

        Args:
            specifications (:obj:`dict`): specifications of the simulator to validate

        Raises:
            :obj:`Exception`: if the simulator did not pass the test case
        """
        image = self.get_simulator_docker_image(specifications)
        missing_labels = set(self.EXPECTED_LABELS).difference(set(image.labels.keys()))
        if missing_labels:
            warnings.warn('The Docker image should have the following Open Container Initiative (OCI) labels:\n  {}'.format(
                '\n  '.join(sorted(missing_labels))), TestCaseWarning)


class HasBioContainersLabels(TestCase):
    """ Test that a Docker image has BioContainers labels with metadata
    about the image
    """
    EXPECTED_LABELS = [
        "about.documentation",
        "about.home",
        "about.license",
        "about.license_file",
        "about.summary",
        "about.tags",
        "base_image",
        "extra.identifiers.biotools",
        "maintainer",
        "software",
        "software.version",
        "version",
    ]

    def eval(self, specifications):
        """ Evaluate a simulator's performance on a test case

        Args:
            specifications (:obj:`dict`): specifications of the simulator to validate

        Raises:
            :obj:`Exception`: if the simulator did not pass the test case
        """
        image = self.get_simulator_docker_image(specifications)
        missing_labels = set(self.EXPECTED_LABELS).difference(set(image.labels.keys()))
        if missing_labels:
            warnings.warn('The Docker image should have the following BioContainers labels:\n  {}'.format(
                '\n  '.join(sorted(missing_labels))), TestCaseWarning)
