# SPDX-License-Identifier: LGPL-2.1-or-later
from .document import open_document


def open(filename):
    return open_document(filename)


def insert(filename, document_name):
    raise ValueError("Component insertion requires the later import/placement stage")
