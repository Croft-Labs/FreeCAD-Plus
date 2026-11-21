# SPDX-License-Identifier: LGPL-2.1-or-later
"""Connect the three presentation choices to the normal application startup."""
from freecad_plus import ui_modes
from freecad_plus import numeric_fields
numeric_fields.install()
ui_modes.install()
