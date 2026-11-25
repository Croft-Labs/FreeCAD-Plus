# SPDX-License-Identifier: LGPL-2.1-or-later
"""Render the approved Plus SVG into Windows multi-resolution ICO resources.

Run with the FreeCAD/LibPack Python (PySide6); no image-generation dependency.
The embedded PNG frames retain alpha at every native Windows icon size.
"""
import os
from pathlib import Path
import struct
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6 import QtCore, QtGui, QtSvg

def build(svg, destination):
    app = QtGui.QGuiApplication.instance() or QtGui.QGuiApplication([])
    renderer = QtSvg.QSvgRenderer(str(svg))
    if not renderer.isValid():
        raise ValueError('Invalid source icon')
    sizes = (16, 20, 24, 32, 40, 48, 64, 96, 128, 256)
    frames = []
    for size in sizes:
        image = QtGui.QImage(size, size, QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(image)
        renderer.render(painter)
        painter.end()
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.WriteOnly)
        if not image.save(buffer, 'PNG'):
            raise ValueError('Could not encode icon frame')
        frames.append(bytes(buffer.data()))
    offset = 6 + 16 * len(sizes)
    entries = []
    for size, frame in zip(sizes, frames):
        entries.append(struct.pack('<BBBBHHII', size % 256, size % 256, 0, 0, 1, 32, len(frame), offset))
        offset += len(frame)
    destination.write_bytes(struct.pack('<HHH', 0, 1, len(sizes)) + b''.join(entries) + b''.join(frames))
    print(f'{destination}: {len(sizes)} transparent sizes')

if __name__ == '__main__':
    source = Path(__file__).resolve().parents[1]
    build(source/'Gui/Icons/freecad-plus.svg', source/'Main/icon.ico')
