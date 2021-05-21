import nuke
import sys
module_path = '/home/shrimo/project'
if module_path not in sys.path:
    sys.path.append(module_path)

from amg_system import qt, utils
# from amg.system import qt, utils
import switch_widget
reload(switch_widget)


def nuke_main_window():
    for obj in qt.QApplication.topLevelWidgets():
        if (obj.inherits('QMainWindow') and
                obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
            return obj
    else:
        raise RuntimeError('Could not find DockMainWindow instance')


def shared_menubar():
    if not hasattr(shared_menubar, 'SHARED_MENUBAR'):
        nuke_main = nuke_main_window()
        try:
            main_menu_bar = nuke_main.menuBar()
        except AttributeError:
            # print 'No Nuke Menu'
            return None
        if not main_menu_bar:
            return None
        shared_menubar.SHARED_MENUBAR = SwitchWidgetBar(main_menu_bar)
    return shared_menubar.SHARED_MENUBAR


def on_node_create():
    mb = shared_menubar()
    if mb:
        mb.on_node_create()


def on_node_delete():
    mb = shared_menubar()
    if mb:
        mb.on_node_delete()


def on_node_rename():
    mb = shared_menubar()
    if mb:
        mb.on_node_rename()


class SwichButton(qt.QPushButton):
    def __init__(self, name_menu):
        super(SwichButton, self).__init__(name_menu)
        self.name_menu = name_menu
        self.point = self.pos()
        pb_style = '''
        QPushButton {
            border: 1 solid rgb(30,30,30);
            border-style: solid;         
            border-radius: 3px;
            background-color: rgb(70,70,70);
            width: 80px;
            /* padding: 0 10px; */
            height: 14px;
            font: 8pt;
            margin: 0 0px;
        }

        QPushButton:pressed {
            background-color: rgb(41,41,41);
        }

        QPushButton:flat {
            border: none; /* no border for a flat push button */
        }        
        QPushButton:focus {
            border: none;
            outline: none;
        }
        QPushButton:default {
            border-color: rgb(1,1,1); /* make the default button prominent */
        }'''
        self.setStyleSheet(pb_style)
        self.clicked.connect(self.show_cwidget)

    def show_cwidget(self):
        # print self.pos()
        cw = switch_widget.SwitchWidget(
            self.name_menu, self.mapToGlobal(self.point))
        cw.exec_()


class SwitchWidgetBar(qt.QWidget):
    '''
    Switch QWidget
    '''

    def __init__(self, main_menu_bar):
        super(SwitchWidgetBar, self).__init__()
        self.main_menu_bar = main_menu_bar

        self.create_layout()
        self.main_menu_bar.setCornerWidget(self, qt.Qt.TopRightCorner)
        self.widget_update()

    def create_layout(self):
        self.layout = qt.QHBoxLayout()
        # self.layout.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def clear_layout(self):
        to_remove = []
        for i in range(self.layout.count()):
            to_remove.append(self.layout.itemAt(i))
        for item in to_remove:
            if item.spacerItem():
                self.layout.removeItem(item)
            else:
                item.widget().deleteLater()
        self.layout.addStretch()

    def widget_update(self):
        if not nuke.root():
            return
        # print '>widget update'
        self.main_menu_bar.cornerWidget().close()
        self.main_menu_bar.setCornerWidget(self, qt.Qt.TopRightCorner)
        self.clear_layout()
        switch_list = set(
            node.name() for node in nuke.allNodes('Switch')
            if node.clones())
        switch_list = sorted(switch_list, key=utils.natural_sort_key)
        for switch in switch_list:
            switch_menu = SwichButton(switch)
            # print 'addWidget: ', switch
            self.layout.addWidget(switch_menu)

        self.setVisible(False)
        self.setVisible(True)
        self.update()
        self.layout.update()
        # print '<------------------->'

    def create_deferred(self):
        self.widget_update()

    def on_node_create(self):
        # print '>create'
        # Time delay for modifying a node to a clone
        qt.QTimer.singleShot(50, self.create_deferred)

    def on_node_delete(self):
        self.on_node_create()

    def on_node_rename(self):
        k = nuke.thisKnob()
        if k.name() == 'name':
            # print '>rename ', k.name()
            self.on_node_create()

    def count_switch_inputs(self):
        switch_list = nuke.allNodes('Switch')
        input_max = 0
        for switch in switch_list:
            if switch.clones():
                input_max = max(input_max, switch.inputs())
        return input_max

