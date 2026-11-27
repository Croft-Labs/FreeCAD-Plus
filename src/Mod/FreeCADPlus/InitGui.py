# SPDX-License-Identifier: LGPL-2.1-or-later
"""Connect the three presentation choices to the normal application startup."""
from freecad_plus import ui_modes
from freecad_plus import numeric_fields
from freecad_plus import idle_tasks
numeric_fields.install()
idle_tasks.install()
ui_modes.install()

from freecad_plus import thicken_task
thicken_task.install()
from freecad_plus import loft_task
loft_task.install()
from freecad_plus import clone_task
clone_task.install()
from freecad_plus import appearance_command
appearance_command.install()
from freecad_plus import reference_image_task
reference_image_task.install()
