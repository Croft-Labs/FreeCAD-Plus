
# Preview-only navigator transition. Acceptance cannot modify the document.
class PreviewPicker(Picker):
    def accept(self):
        return
    def update_enabled(self, *args):
        super().update_enabled(*args)
        self.submit.setText('Next: quantity and pattern…')

def preview_picker(parent):
    picker = PreviewPicker(parent)
    for label in picker.findChildren(QtWidgets.QLabel):
        if label.text() == 'Select parts to add as children at the parent origin.':
            label.setText('Select parts, then choose their quantity and arrangement.')
    return picker
