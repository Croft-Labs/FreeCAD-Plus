# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native scroll/focus/lifetime coverage for shared task error feedback."""
import os
import sys
import unittest
from PySide6 import QtCore,QtWidgets,QtTest
from freecad_plus.task_status import TaskStatus


class TestTaskStatus(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:self.skipTest('Requires an isolated native profile')
        self.window=QtWidgets.QWidget()
        layout=QtWidgets.QVBoxLayout(self.window)
        self.scroll=QtWidgets.QScrollArea();self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.scroll)
        self.form=QtWidgets.QWidget();form_layout=QtWidgets.QVBoxLayout(self.form)
        self.field=QtWidgets.QLineEdit('Existing input');form_layout.addWidget(self.field)
        spacer=QtWidgets.QWidget();spacer.setFixedHeight(450);form_layout.addWidget(spacer)
        self.status=TaskStatus('Choose geometry.');form_layout.addWidget(self.status)
        self.scroll.setWidget(self.form);self.window.resize(300,260);self.window.show()
        self.window.activateWindow();self.field.setFocus();QtTest.QTest.qWait(80)

    def tearDown(self):
        self.window.close();self.window.deleteLater();QtTest.QTest.qWait(150)

    def rect(self):
        return QtCore.QRect(self.status.mapTo(self.scroll.viewport(),QtCore.QPoint()),self.status.size())

    def test_error_reveal_preserves_focus_and_repeat_does_not_scroll(self):
        focus=QtWidgets.QApplication.focusWidget()
        text='The selected plane must precede this sketch. Reorder History, then try again.'
        self.status.setError(text);QtTest.QTest.qWait(180)
        self.assertTrue(self.status.error)
        self.assertTrue(self.scroll.viewport().rect().contains(self.rect()))
        self.assertEqual(QtWidgets.QApplication.focusWidget(),focus)
        self.scroll.verticalScrollBar().setValue(0);QtTest.QTest.qWait(40)
        self.status.setError(text);QtTest.QTest.qWait(180)
        self.assertEqual(self.scroll.verticalScrollBar().value(),0)
        self.status.setText('Using the selected plane.');QtTest.QTest.qWait(80)
        self.assertFalse(self.status.error);self.assertFalse(self.status.styleSheet())
        self.assertEqual(self.field.text(),'Existing input')
        self.assertEqual(QtWidgets.QApplication.focusWidget(),focus)

    def test_long_wrapped_error_reveals_beginning_and_renders_literal_labels(self):
        text='<b>Plane & Sketch</b>: ' + 'Choose an earlier input and retry. '*35
        self.status.setError(text);QtTest.QTest.qWait(180)
        self.assertEqual(self.status.textFormat(),QtCore.Qt.PlainText)
        self.assertEqual(self.status.text(),text)
        self.assertTrue(self.status.wordWrap())
        self.assertGreater(self.status.height(),self.scroll.viewport().height())
        self.assertGreaterEqual(self.rect().top(),0)
        self.assertLessEqual(self.rect().top(),12)

    def test_recovery_and_destruction_cancel_pending_reveal(self):
        self.status.setError('Invalid input.');self.status.setText('Ready.')
        QtTest.QTest.qWait(180)
        self.assertEqual(self.scroll.verticalScrollBar().value(),0)
        errors=[];previous=sys.excepthook
        sys.excepthook=lambda *args:errors.append(args)
        try:
            self.status.setError('Another invalid input.')
            self.status.deleteLater();QtTest.QTest.qWait(180)
            self.assertFalse(errors,errors)
        finally:sys.excepthook=previous
