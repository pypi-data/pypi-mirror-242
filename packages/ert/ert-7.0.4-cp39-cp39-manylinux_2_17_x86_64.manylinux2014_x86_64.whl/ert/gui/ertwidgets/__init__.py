# isort: skip_file
import pkgutil
from os.path import dirname
from typing import cast, TYPE_CHECKING

from qtpy.QtCore import Qt
from qtpy.QtGui import QCursor, QIcon, QMovie, QPixmap
from qtpy.QtWidgets import QApplication

if TYPE_CHECKING:
    from importlib.abc import FileLoader


def _get_ert_gui_dir():
    ert_gui_loader = cast("FileLoader", pkgutil.get_loader("ert.gui"))
    return dirname(ert_gui_loader.get_filename())


def showWaitCursorWhileWaiting(func):
    """A function decorator to show the wait cursor while the function is working."""

    def wrapper(*arg):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            res = func(*arg)
            return res
        finally:
            QApplication.restoreOverrideCursor()

    return wrapper


def resourceIcon(name):
    """Load an image as an icon"""
    return QIcon(f"{_get_ert_gui_dir()}/resources/gui/img/{name}")


def resourceImage(name) -> QPixmap:
    """Load an image as a Pixmap"""
    return QPixmap(f"{_get_ert_gui_dir()}/resources/gui/img/{name}")


def resourceMovie(name) -> QMovie:
    movie = QMovie(f"{_get_ert_gui_dir()}/resources/gui/img/{name}")
    movie.start()
    return movie


# The following imports utilize the functions defined above:
from .legend import Legend  # noqa
from .validationsupport import ValidationSupport  # noqa
from .closabledialog import ClosableDialog  # noqa
from .analysismoduleedit import AnalysisModuleEdit  # noqa
from .activelabel import ActiveLabel  # noqa
from .searchbox import SearchBox  # noqa
from .caseselector import CaseSelector  # noqa
from .caselist import CaseList  # noqa
from .checklist import CheckList  # noqa
from .stringbox import StringBox  # noqa
from .listeditbox import ListEditBox  # noqa
from .customdialog import CustomDialog  # noqa
from .summarypanel import SummaryPanel  # noqa
from .pathchooser import PathChooser  # noqa
from .suggestor_message import SuggestorMessage  # noqa
