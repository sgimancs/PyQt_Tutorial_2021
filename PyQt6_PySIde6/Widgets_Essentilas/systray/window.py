# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog,
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QMenu, QMessageBox, QPushButton,
                               QSpinBox, QStyle, QSystemTrayIcon, QTextEdit,
                               QVBoxLayout)

import rc_systray  # noqa: F401


class Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._icon_group_box = QGroupBox()
        self._icon_label = QLabel()
        self._icon_combo_box = QComboBox()
        self._show_icon_check_box = QCheckBox()

        self._message_group_box = QGroupBox()
        self._type_label = QLabel()
        self._duration_label = QLabel()
        self._duration_warning_label = QLabel()
        self._title_label = QLabel()
        self._body_label = QLabel()

        self._type_combo_box = QComboBox()
        self._duration_spin_box = QSpinBox()
        self._title_edit = QLineEdit()
        self._body_edit = QTextEdit()
        self._show_message_button = QPushButton()

        self._minimize_action = QAction()
        self._maximize_action = QAction()
        self._restore_action = QAction()
        self._quit_action = QAction()

        self._tray_icon = QSystemTrayIcon()
        self._tray_icon_menu = QMenu()

        self.create_icon_group_box()
        self.create_message_group_box()

        self._icon_label.setMinimumWidth(self._duration_label.sizeHint().width())

        self.create_actions()
        self.create_tray_icon()

        self._show_message_button.clicked.connect(self.show_message)
        self._show_icon_check_box.toggled.connect(self._tray_icon.setVisible)
        self._icon_combo_box.currentIndexChanged.connect(self.set_icon)
        self._tray_icon.messageClicked.connect(self.message_clicked)
        self._tray_icon.activated.connect(self.icon_activated)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._icon_group_box)
        self._main_layout.addWidget(self._message_group_box)
        self.setLayout(self._main_layout)

        self._icon_combo_box.setCurrentIndex(1)
        self._tray_icon.show()

        self.setWindowTitle("Systray")
        self.resize(400, 300)

    def setVisible(self, visible):
        self._minimize_action.setEnabled(visible)
        self._maximize_action.setEnabled(not self.isMaximized())
        self._restore_action.setEnabled(self.isMaximized() or not visible)
        super().setVisible(visible)

    def closeEvent(self, event):
        if not event.spontaneous() or not self.isVisible():
            return
        if self._tray_icon.isVisible():
            QMessageBox.information(self, "Systray",
                                    "The program will keep running in the system tray. "
                                    "To terminate the program, choose <b>Quit</b> in the context "
                                    "menu of the system tray entry.")
            self.hide()
            event.ignore()

    @Slot(int)
    def set_icon(self, index):
        icon = self._icon_combo_box.itemIcon(index)
        self._tray_icon.setIcon(icon)
        self.setWindowIcon(icon)
        self._tray_icon.setToolTip(self._icon_combo_box.itemText(index))

    @Slot(str)
    def icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            pass
        if reason == QSystemTrayIcon.DoubleClick:
            self._icon_combo_box.setCurrentIndex(
                (self._icon_combo_box.currentIndex() + 1) % self._icon_combo_box.count()
            )
        if reason == QSystemTrayIcon.MiddleClick:
            self.show_message()

    @Slot()
    def show_message(self):
        self._show_icon_check_box.setChecked(True)
        selected_icon = self._type_combo_box.itemData(self._type_combo_box.currentIndex())
        msg_icon = QSystemTrayIcon.MessageIcon(selected_icon)

        if selected_icon == -1:  # custom icon
            icon = QIcon(self._icon_combo_box.itemIcon(self._icon_combo_box.currentIndex()))
            self._tray_icon.showMessage(
                self._title_edit.text(),
                self._body_edit.toPlainText(),
                icon,
                self._duration_spin_box.value() * 1000,
            )
        else:
            self._tray_icon.showMessage(
                self._title_edit.text(),
                self._body_edit.toPlainText(),
                msg_icon,
                self._duration_spin_box.value() * 1000,
            )

    @Slot()
    def message_clicked(self):
        QMessageBox.information(None, "Systray",
                                "Sorry, I already gave what help I could.\n"
                                "Maybe you should try asking a human?")

    def create_icon_group_box(self):
        self._icon_group_box = QGroupBox("Tray Icon")

        self._icon_label = QLabel("Icon:")

        self._icon_combo_box = QComboBox()
        self._icon_combo_box.addItem(QIcon(":/images/bad.png"), "Bad")
        self._icon_combo_box.addItem(QIcon(":/images/heart.png"), "Heart")
        self._icon_combo_box.addItem(QIcon(":/images/trash.png"), "Trash")

        self._show_icon_check_box = QCheckBox("Show icon")
        self._show_icon_check_box.setChecked(True)

        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self._icon_label)
        icon_layout.addWidget(self._icon_combo_box)
        icon_layout.addStretch()
        icon_layout.addWidget(self._show_icon_check_box)
        self._icon_group_box.setLayout(icon_layout)

    def create_message_group_box(self):
        self._message_group_box = QGroupBox("Balloon Message")

        self._type_label = QLabel("Type:")

        self._type_combo_box = QComboBox()
        self._type_combo_box.addItem("None", QSystemTrayIcon.MessageIcon.NoIcon)
        self._type_combo_box.addItem(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation),
            "Information",
            QSystemTrayIcon.MessageIcon.Information,
        )
        self._type_combo_box.addItem(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning),
            "Warning",
            QSystemTrayIcon.MessageIcon.Warning,
        )
        self._type_combo_box.addItem(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical),
            "Critical",
            QSystemTrayIcon.MessageIcon.Critical,
        )
        self._type_combo_box.addItem(QIcon(), "Custom icon", -1)
        self._type_combo_box.setCurrentIndex(1)

        self._duration_label = QLabel("Duration:")

        self._duration_spin_box = QSpinBox()
        self._duration_spin_box.setRange(5, 60)
        self._duration_spin_box.setSuffix(" s")
        self._duration_spin_box.setValue(15)

        self._duration_warning_label = QLabel("(some systems might ignore this hint)")
        self._duration_warning_label.setIndent(10)

        self._title_label = QLabel("Title:")
        self._title_edit = QLineEdit("Cannot connect to network")
        self._body_label = QLabel("Body:")

        self._body_edit = QTextEdit()
        self._body_edit.setPlainText("Don't believe me. Honestly, I don't have a clue.\n"
                                     "Click this balloon for details.")

        self._show_message_button = QPushButton("Show Message")
        self._show_message_button.setDefault(True)

        message_layout = QGridLayout()
        message_layout.addWidget(self._type_label, 0, 0)
        message_layout.addWidget(self._type_combo_box, 0, 1, 1, 2)
        message_layout.addWidget(self._duration_label, 1, 0)
        message_layout.addWidget(self._duration_spin_box, 1, 1)
        message_layout.addWidget(self._duration_warning_label, 1, 2, 1, 3)
        message_layout.addWidget(self._title_label, 2, 0)
        message_layout.addWidget(self._title_edit, 2, 1, 1, 4)
        message_layout.addWidget(self._body_label, 3, 0)
        message_layout.addWidget(self._body_edit, 3, 1, 2, 4)
        message_layout.addWidget(self._show_message_button, 5, 4)
        message_layout.setColumnStretch(3, 1)
        message_layout.setRowStretch(4, 1)
        self._message_group_box.setLayout(message_layout)

    def create_actions(self):
        self._minimize_action = QAction("Minimize", self)
        self._minimize_action.triggered.connect(self.hide)

        self._maximize_action = QAction("Maximize", self)
        self._maximize_action.triggered.connect(self.showMaximized)

        self._restore_action = QAction("Restore", self)
        self._restore_action.triggered.connect(self.showNormal)

        self._quit_action = QAction("Quit", self)
        self._quit_action.triggered.connect(qApp.quit)  # noqa: F821

    def create_tray_icon(self):
        self._tray_icon_menu = QMenu(self)
        self._tray_icon_menu.addAction(self._minimize_action)
        self._tray_icon_menu.addAction(self._maximize_action)
        self._tray_icon_menu.addAction(self._restore_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._quit_action)

        self._tray_icon = QSystemTrayIcon(self)
        self._tray_icon.setContextMenu(self._tray_icon_menu)
