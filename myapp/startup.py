# Copyright 2023
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys


class PreStartUp:
    """Necessary steps for environment, Python and Qt"""

    @staticmethod
    def set_qt_application_name():
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.setApplicationName('Siba PCTool')
        QCoreApplication.setOrganizationName('OME')

    @staticmethod
    def set_qt_application_version():
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.setApplicationVersion('0:0:1')

    @staticmethod
    def inject_environment_variables():
        # Qt expects 'qtquickcontrols2.conf' at root level, but the way we handle resources does not allow that.
        # So we need to override the path here
        os.environ['QT_QUICK_CONTROLS_CONF'] = ':/data/qtquickcontrols2.conf'


class StartUp:
    """Necessary steps for myapp"""

    @staticmethod
    def import_resources():
        try:
            import myapp.generated_resources
        except ImportError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def import_bindings():
        try:
            import myapp.pyobjects
            import src.system
        except ImportError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def start_application():
        from myapp.application import MyApplication
        import signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        app = MyApplication(sys.argv)

        app.set_window_icon()
        app.set_up_signals()
        app.set_up_imports()
        app.start_engine()
        app.verify()
        sys.exit(app.exec())
        


def boot_loader():
    we = PreStartUp()
    we.set_qt_application_name()
    we.set_qt_application_version()
    we.inject_environment_variables()

    we = StartUp()
    we.import_resources()
    we.import_bindings()
    we.start_application()
