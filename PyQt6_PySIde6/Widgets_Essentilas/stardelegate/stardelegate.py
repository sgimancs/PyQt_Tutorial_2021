# Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>
# Copyright (C) 2011 Arun Srinivasan <rulfzid@gmail.com>
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

from PySide6.QtWidgets import QStyledItemDelegate, QStyle

from starrating import StarRating
from stareditor import StarEditor


class StarDelegate(QStyledItemDelegate):
    """ A subclass of QStyledItemDelegate that allows us to render our
        pretty star ratings.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        """ Paint the items in the table.

            If the item referred to by <index> is a StarRating, we handle the
            painting ourselves. For the other items, we let the base class
            handle the painting as usual.

            In a polished application, we'd use a better check than the
            column number to find out if we needed to paint the stars, but
            it works for the purposes of this example.
        """
        if index.column() == 3:
            star_rating = StarRating(index.data())

            # If the row is currently selected, we need to make sure we
            # paint the background accordingly.
            if option.state & QStyle.StateFlag.State_Selected:
                # The original C++ example used option.palette.foreground() to
                # get the brush for painting, but there are a couple of
                # problems with that:
                #   - foreground() is obsolete now, use windowText() instead
                #   - more importantly, windowText() just returns a brush
                #     containing a flat color, where sometimes the style
                #     would have a nice subtle gradient or something.
                # Here we just use the brush of the painter object that's
                # passed in to us, which keeps the row highlighting nice
                # and consistent.
                painter.fillRect(option.rect, painter.brush())

            # Now that we've painted the background, call starRating.paint()
            # to paint the stars.
            star_rating.paint(painter, option.rect, option.palette)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        """ Returns the size needed to display the item in a QSize object. """
        if index.column() == 3:
            star_rating = StarRating(index.data())
            return star_rating.sizeHint()
        else:
            return QStyledItemDelegate.sizeHint(self, option, index)

    # The next 4 methods handle the custom editing that we need to do.
    # If this were just a display delegate, paint() and sizeHint() would
    # be all we needed.

    def createEditor(self, parent, option, index):
        """ Creates and returns the custom StarEditor object we'll use to edit
            the StarRating.
        """
        if index.column() == 3:
            editor = StarEditor(parent)
            editor.editing_finished.connect(self.commit_and_close_editor)
            return editor
        else:
            return QStyledItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        """ Sets the data to be displayed and edited by our custom editor. """
        if index.column() == 3:
            editor.star_rating = StarRating(index.data())
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        """ Get the data from our custom editor and stuffs it into the model.
        """
        if index.column() == 3:
            model.setData(index, editor.star_rating.star_count)
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

    def commit_and_close_editor(self):
        """ Erm... commits the data and closes the editor. :) """
        editor = self.sender()

        # The commitData signal must be emitted when we've finished editing
        # and need to write our changed back to the model.
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QStyledItemDelegate.NoHint)


if __name__ == "__main__":
    """ Run the application. """
    from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem,
                                   QAbstractItemView)
    import sys

    app = QApplication(sys.argv)

    # Create and populate the tableWidget
    table_widget = QTableWidget(4, 4)
    table_widget.setItemDelegate(StarDelegate())
    table_widget.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked
                                 | QAbstractItemView.EditTrigger.SelectedClicked)
    table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    table_widget.setHorizontalHeaderLabels(["Title", "Genre", "Artist", "Rating"])

    data = [["Mass in B-Minor", "Baroque", "J.S. Bach", 5],
            ["Three More Foxes", "Jazz", "Maynard Ferguson", 4],
            ["Sex Bomb", "Pop", "Tom Jones", 3],
            ["Barbie Girl", "Pop", "Aqua", 5]]

    for r in range(len(data)):
        table_widget.setItem(r, 0, QTableWidgetItem(data[r][0]))
        table_widget.setItem(r, 1, QTableWidgetItem(data[r][1]))
        table_widget.setItem(r, 2, QTableWidgetItem(data[r][2]))
        item = QTableWidgetItem()
        item.setData(0, StarRating(data[r][3]).star_count)
        table_widget.setItem(r, 3, item)

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    sys.exit(app.exec())
