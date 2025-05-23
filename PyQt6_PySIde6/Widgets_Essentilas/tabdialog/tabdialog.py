# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 port of the widgets/dialogs/tabdialog example from Qt v6.x"""

import sys

from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QApplication,
    QDialog,
    QTabWidget,
    QLineEdit,
    QDialogButtonBox,
    QFrame,
    QListWidget,
    QGroupBox,
)


class TabDialog(QDialog):
    def __init__(self, file_name: str, parent: QWidget = None):
        super().__init__(parent)

        file_info = QFileInfo(file_name)

        tab_widget = QTabWidget()
        tab_widget.addTab(GeneralTab(file_info, self), "General")
        tab_widget.addTab(PermissionsTab(file_info, self), "Permissions")
        tab_widget.addTab(ApplicationsTab(file_info, self), "Applications")

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.setWindowTitle("Tab Dialog")


class GeneralTab(QWidget):
    def __init__(self, file_info: QFileInfo, parent: QWidget):
        super().__init__(parent)

        file_name_label = QLabel("File Name:")
        file_name_edit = QLineEdit(file_info.fileName())

        path_label = QLabel("Path:")
        path_value_label = QLabel(file_info.absoluteFilePath())
        path_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        size_label = QLabel("Size:")
        size = file_info.size() / 1024
        size_value_label = QLabel(f"{size} K")
        size_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        last_read_label = QLabel("Last Read:")
        last_read_value_label = QLabel(file_info.lastRead().toString())
        last_read_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        last_mod_label = QLabel("Last Modified:")
        last_mod_value_label = QLabel(file_info.lastModified().toString())
        last_mod_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        main_layout = QVBoxLayout()
        main_layout.addWidget(file_name_label)
        main_layout.addWidget(file_name_edit)
        main_layout.addWidget(path_label)
        main_layout.addWidget(path_value_label)
        main_layout.addWidget(size_label)
        main_layout.addWidget(size_value_label)
        main_layout.addWidget(last_read_label)
        main_layout.addWidget(last_read_value_label)
        main_layout.addWidget(last_mod_label)
        main_layout.addWidget(last_mod_value_label)
        main_layout.addStretch(1)
        self.setLayout(main_layout)


class PermissionsTab(QWidget):
    def __init__(self, file_info: QFileInfo, parent: QWidget):
        super().__init__(parent)

        permissions_group = QGroupBox("Permissions")

        readable = QCheckBox("Readable")
        if file_info.isReadable():
            readable.setChecked(True)

        writable = QCheckBox("Writable")
        if file_info.isWritable():
            writable.setChecked(True)

        executable = QCheckBox("Executable")
        if file_info.isExecutable():
            executable.setChecked(True)

        owner_group = QGroupBox("Ownership")

        owner_label = QLabel("Owner")
        owner_value_label = QLabel(file_info.owner())
        owner_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        group_label = QLabel("Group")
        group_value_label = QLabel(file_info.group())
        group_value_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        permissions_layout = QVBoxLayout()
        permissions_layout.addWidget(readable)
        permissions_layout.addWidget(writable)
        permissions_layout.addWidget(executable)
        permissions_group.setLayout(permissions_layout)

        owner_layout = QVBoxLayout()
        owner_layout.addWidget(owner_label)
        owner_layout.addWidget(owner_value_label)
        owner_layout.addWidget(group_label)
        owner_layout.addWidget(group_value_label)
        owner_group.setLayout(owner_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(permissions_group)
        main_layout.addWidget(owner_group)
        main_layout.addStretch(1)
        self.setLayout(main_layout)


class ApplicationsTab(QWidget):
    def __init__(self, file_info: QFileInfo, parent: QWidget):
        super().__init__(parent)

        top_label = QLabel("Open with:")

        applications_list_box = QListWidget()
        applications = []

        for i in range(1, 31):
            applications.append(f"Application {i}")
        applications_list_box.insertItems(0, applications)

        if not file_info.suffix():
            always_check_box = QCheckBox(
                "Always use this application to open this type of file"
            )
        else:
            always_check_box = QCheckBox(
                f"Always use this application to open files "
                f"with the extension {file_info.suffix()}"
            )

        layout = QVBoxLayout()
        layout.addWidget(top_label)
        layout.addWidget(applications_list_box)
        layout.addWidget(always_check_box)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
    else:
        file_name = "."

    tab_dialog = TabDialog(file_name)
    tab_dialog.show()

    sys.exit(app.exec())
