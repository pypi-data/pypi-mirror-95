from typing import List
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QVBoxLayout, QWidget
from bergen.schema import Port
from functools import partial

class AssignationUI(QDialog):


    def __init__(self, inputs: List[Port], default_values = {}, forced_values={}, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.inputs = inputs

        self.editable_ports = [port for port in self.inputs if port.key not in forced_values.keys()]

        self.keyDependencyMap = {port.key: port.widget.dependencies for port in self.inputs}

        self.keyWidgetMap = {
            port.key: port.buildWidget(on_changed=partial(self.onDependencyChanged, port.key)) for port in self.editable_ports
        }
        self.keyLabelMap = {
            port.key: port.label for port in self.editable_ports
        }

        self.defaultValuesMap = {
            port.key: port.default for port in self.inputs
        }

        self.keyValuesMap = {**self.defaultValuesMap, **default_values, **forced_values}


        #UI

        self.parametersWidget = QGroupBox("Parameters")
        self.parametersLayout = QFormLayout()

        self.port_widgets = [widget for widget in self.keyWidgetMap.values()]
        self.port_labels = [label for label in self.keyLabelMap.values()]

        for row in zip(self.port_labels, self.port_widgets):
            self.parametersLayout.addRow(*row)

        self.parametersWidget.setLayout(self.parametersLayout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.on_set)
        buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.parametersWidget)
        self.layout.addWidget(buttonBox)
        self.setLayout(self.layout)

    
        self.initialRender()


    def on_set(self):
        self.parameters = self.keyValuesMap
        self.accept()
        self.close()


    def initialRender(self):

        no_dependency_keys = [key for key, dependencies in self.keyDependencyMap.items() if len(dependencies) == 0]

        for key in no_dependency_keys:
            if key in self.keyWidgetMap:
                self.keyWidgetMap[key].render(self.keyValuesMap)
    

    def onDependencyChanged(self, updatedkey, value):
        print(updatedkey, value)
        if self.keyValuesMap[updatedkey] == value:
            # No change in dependency, omit
            print("Ommitting")
            return
        else:
            self.keyValuesMap[updatedkey] = value
            dependent_keys = [key for key, dependencies in self.keyDependencyMap.items() if updatedkey in dependencies]
            print(dependent_keys)
            
            for key in dependent_keys:
                self.keyWidgetMap[key].render(self.keyValuesMap)


class AssignationUIMixin:

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._ui = None


    def askInputs(self, **kwargs) -> dict:
        widget = self.getWidget(**kwargs) # We have established a ui
        if widget.exec_():
            return widget.parameters
        else:
            return None


    def getWidget(self, **kwargs):
        if not self._ui:
            self._ui = AssignationUI(self.inputs, **kwargs)
        return self._ui