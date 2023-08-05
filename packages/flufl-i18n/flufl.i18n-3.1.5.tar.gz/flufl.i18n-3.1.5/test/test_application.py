from .data import messages

from flufl.i18n import Application, PackageStrategy


def test_application_name():
    strategy = PackageStrategy('flufl', messages)
    application = Application(strategy)
    assert application.name == 'flufl'
