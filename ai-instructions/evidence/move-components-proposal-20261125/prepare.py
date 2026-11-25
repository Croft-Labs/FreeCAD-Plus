from pathlib import Path
root = Path(__file__).parent
candidate = Path('C:/Users/dgium/Documents/__Apps/_temp builds/app-render-companion/sessions/f6ed77034205/candidate')
(candidate/'movement.py').write_text((root/'proposed_movement.py').read_text(encoding='utf-8'), encoding='utf-8')
s = (root/'review-source/panel.py').read_text(encoding='utf-8-sig')
s = s.replace('                layout.addWidget(self.assembly_button)', '''                assembly_actions = QtWidgets.QHBoxLayout()
                assembly_actions.addWidget(self.assembly_button, 1)
                move = QtWidgets.QToolButton(); move.setText('Move Components')
                move.setIcon(Gui.getIcon('Std_TransformManip')); move.setToolTip('Move Components')
                move.setAccessibleName('Move Components')
                move.clicked.connect(lambda: self.move_rows(tuple(i.data(0, _ROLE) for i in self.trees[1].selectedItems())))
                assembly_actions.addWidget(move); layout.addLayout(assembly_actions)''')
s = s.replace("                if not row.anchor:\n                    actions[menu.addAction('Move Components')] = lambda unused: self.move_rows(selected)",
              "                actions[menu.addAction('Move Components')] = lambda unused: self.move_rows(selected)")
(candidate/'panel.py').write_text(s, encoding='utf-8')
print('Prepared two UI-only candidate modules')
