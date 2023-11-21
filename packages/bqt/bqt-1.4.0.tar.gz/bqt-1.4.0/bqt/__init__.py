"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import bqt
import bqt.focus
import bqt.manager
import os
import sys
import bpy
from bqt.qt_core import QtCore, QApplication
import logging
import blender_stylesheet


bl_info = {
        "name": "PySide Qt wrapper (bqt)",
        "description": "Enable PySide QtWidgets in Blender",
        "author": "tech-artists.org",
        "version": (1, 3, 0),
        "blender": (2, 80, 0),
        # "location": "",
        # "warning": "", # used for warning icon and text in add-ons panel
        "wiki_url": "https://github.com/techartorg/bqt/wiki",
        "tracker_url": "https://github.com/techartorg/bqt/issues",
        "support": "COMMUNITY",
        "category": "UI"
        }

add = bqt.manager.register

# CORE FUNCTIONS #

def _instantiate_QApplication() -> "bqt.blender_applications.BlenderApplication":
    # enable dpi scale, run before creating QApplication
    QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = _load_os_module()
    blender_stylesheet.setup()
    return app


def _load_os_module() -> "bqt.blender_applications.BlenderApplication":
    """Loads the correct OS platform Application Class"""
    operating_system = sys.platform
    if operating_system == "darwin":
        from .blender_applications.darwin_blender_application import DarwinBlenderApplication

        return DarwinBlenderApplication(sys.argv)

    if operating_system in ["linux", "linux2"]:
        # TODO: LINUX module
        pass

    elif operating_system == "win32":
        from .blender_applications.win32_blender_application import Win32BlenderApplication

        return Win32BlenderApplication(sys.argv + ['-platform', 'windows:darkmode=2'])


@bpy.app.handlers.persistent
def _create_global_app():
    """
    Create a global QApplication instance, that's maintained between Blender sessions.
    Runs after Blender finished startup.
    """
    qapp = _instantiate_QApplication()
    # save a reference to the C++ window in a global var, to prevent the parent being garbage collected
    # for some reason this works here, but not in the blender_applications init as a class attribute (self),
    # and saving it in a global in blender_applications.py causes blender to crash on startup
    global parent_window
    parent_window = qapp._blender_window.parent()


def register():
    """
    Runs on enabling the add-on.
    setup bqt, wrap blender in qt, register operators
    """
    # hacky way to check if we already are waiting on bqt setup, or bqt is already setup
    if QApplication.instance():
        logging.warning("bqt: QApplication already exists, skipping bqt registration")
        return

    if os.getenv("BQT_DISABLE_STARTUP", 0) == "1":
        logging.warning("bqt: BQT_DISABLE_STARTUP is set, skipping bqt registration")
        return

    _create_global_app()


def unregister():
    """
    Runs on disabling the add-on.
    """
    # todo, as long as blender is wrapped in qt, unregistering operator & callback will cause issues,
    #  for now we just return since unregister should not be called partially
    return

    # if not os.getenv("BQT_DISABLE_WRAP", 0) == "1":
    #     bpy.utils.unregister_class(bqt.focus.QFocusOperator)


