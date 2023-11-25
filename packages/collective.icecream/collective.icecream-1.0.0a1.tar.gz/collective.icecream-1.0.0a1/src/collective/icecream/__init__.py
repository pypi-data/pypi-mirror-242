"""Init and utils."""
from plone import api


def initialize(context):
    """Add icecream to the builtins."""
    if api.env.debug_mode():
        from icecream import install

        install()
        ic("Icecream installed")  # noqa: F821
