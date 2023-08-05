from public import public as _public

from flufl.i18n._application import Application
from flufl.i18n._expand import expand
from flufl.i18n._registry import registry
from flufl.i18n._strategy import PackageStrategy, SimpleStrategy
from flufl.i18n.types import (
    RuntimeTranslator,
    TranslationContextManager,
    TranslationStrategy,
)


__version__ = '3.1.5'


_public(
    Application=Application,
    PackageStrategy=PackageStrategy,
    RuntimeTranslator=RuntimeTranslator,
    SimpleStrategy=SimpleStrategy,
    TranslationContextManager=TranslationContextManager,
    TranslationStrategy=TranslationStrategy,
    expand=expand,
    registry=registry,
)


@_public
def initialize(domain: str) -> RuntimeTranslator:
    """A convenience function for setting up translation.

    :param domain: The application's name.
    :return: The translation function, typically bound to _()
    """
    strategy = SimpleStrategy(domain)
    application = registry.register(strategy)
    return application._


del _public
