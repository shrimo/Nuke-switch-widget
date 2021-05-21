import nuke
import sys
module_path = '/home/shrimo/project'
if module_path not in sys.path:
    sys.path.append(module_path)
from amg_system import qt


class SwitchWidget(qt.QDialog):
    '''
    Switch widget for clones switch node
    '''

    def __init__(self, switch_name, coordinates):
        super(SwitchWidget, self).__init__()
        self.switch_name = switch_name
        self.coordinates = coordinates
        self.move(coordinates.x()-48, coordinates.y()+26)
        self.setWindowFlags(qt.Qt.Popup) 
        
        self.setStyleSheet("""
        QMenu {
            background-color: rgb(49,49,49);      
            color: rgb(0,255,255);
            border: 1px solid;
            }""")

        self.layout_v = qt.QVBoxLayout()
        self.layout_h = qt.QHBoxLayout()
        self.setLayout(self.layout_v)
        self.setFixedWidth(130)        
        # self.aboutToShow.connect(self.update_info_widget)
        self.slider = qt.QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.count_switch_inputs())
        self.slider.setSliderPosition(self.current_switch_input())
        self.slider.setOrientation(qt.Qt.Horizontal)
        self.slider.setStyleSheet("""
        QSlider::groove:horizontal {            
            height: 10px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
            margin: 2px 0;}

        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
            border: 1px solid #5c5c5c;
            width: 18px;
            margin: -2px 0;
            border-radius: 3px;}""")
        self.slider.valueChanged[int].connect(self.slider_changed)
        self.label1 = qt.QLabel()
        self.label2 = qt.QLabel()
        label_css = """
        QLabel{
            color: rgb(150, 150, 150);
            font: 11px;  
        }"""
        self.label1.setStyleSheet(label_css)
        self.label2.setStyleSheet(label_css)

        self.line_edit = qt.QLineEdit(self)
        self.line_edit.setText(str(self.current_switch_input()))
        self.line_edit.textChanged[str].connect(self.line_edit_changed)
        self.label_which = qt.QLabel('which')

        self.layout_h.addWidget(self.label_which)
        self.layout_h.addWidget(self.line_edit)
        self.layout_v.addWidget(self.label1)
        self.layout_v.addWidget(self.label2)
        self.layout_v.addWidget(self.slider)
        self.layout_v.addLayout(self.layout_h)        
        self.update_info_widget()
        
        
    def update_info_widget(self):        
        # self.title_text = "{name} : {sv}".format(
        #     name=self.switch_name, sv=self.current_switch_input())
        # self.title_text = self.switch_name
        self.clones_count = "Clones: {csn}".format(
            csn=self.count_switch_node())
        self.nodes_count = "Inputs: {csi}".format(
            csi=self.count_switch_inputs() + 1)
        # self.setTitle(self.title_text)
        self.label1.setText(self.clones_count)
        self.label2.setText(self.nodes_count)
        self.slider.setMaximum(self.count_switch_inputs())        

    def count_switch_node(self):
        switch = nuke.toNode(self.switch_name)
        if switch:
            if switch.clones():
                return switch.clones() + 1
        return 0

    def current_switch_input(self):
        switch = nuke.toNode(self.switch_name)
        if switch:
            if switch.clones():
                return int(switch.knob('which').getValue())


    def count_switch_inputs(self):        
        switch = nuke.toNode(self.switch_name)
        if switch:            
            if switch.clones() and switch.inputs() > 1:
                return switch.inputs() - 1
            else:
                return switch.inputs()
        return 0

    def selector(self, toggle):
        if toggle:
            switch = nuke.toNode(self.switch_name)            
            if switch.clones():
                switch['which'].setValue(float(toggle))                

    def slider_changed(self, val):
        self.update_info_widget()
        self.line_edit.setText(str(self.slider.value()))
        self.selector(str(val))

    def line_edit_changed(self, val):
        if val:
            self.update_info_widget()
            self.slider.setValue(int(val))
            self.selector(val)
