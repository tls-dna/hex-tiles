from PyQt5.QtWidgets import QAction, QMainWindow, QFileDialog
from .grid import Grid


class RouterAppMain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        def menu_action(name, shortcut, tip, slt):
            action = QAction(name, self)
            action.setShortcut(shortcut)
            action.setStatusTip(tip)
            action.triggered.connect(slt)
            return action

        self.tileGrid = Grid()
        self.setCentralWidget(self.tileGrid)
        self.setWindowTitle('TileRouter')
        self.statusBar()

        openFile = menu_action('Open', 'Ctrl+O',
                               'Open new File', self.showFileDialog)
        newFile = menu_action('New', 'Ctrl+N',
                              'Clean triangle grid', self.tileGrid.clean_cells)

        saveFile = menu_action('Save As', "Ctrl+S", 'Save design', self.showSaveDialog)

        select_tool = menu_action('Select', 'S',
                                  'Select triangles', self.selectSelectionTool)
        print_sequence_tool = menu_action('Print Triangle', 'Ctrl+P',
                                          'Prints triangle sequence to cmd', self.selectPrintSeqTool)

        eraser_tool = menu_action('Delete Triangles',
                                  'Ctrl+D', 'Does what it says.', self.selectEraserTool)
        connection_tool = menu_action('Add connection',
                                      'Ctrl+C', 'Makes staples complementary.', self.selectConnectionAdditionTool)
        filter_tool = menu_action('Filter', 'Ctrl+F',
                                  'Hide all triangles where no sequence is assigned.', self.filterTool)

        generate_tool = menu_action('Generate Seq', 'Ctrl+G',
                                    'Generate the staple sequences', self.tileGrid.invoke_generate_sequences)

        get_price_tool = menu_action('Price ?', 'Shift+4', 'Calculates the price of the oligos to order.',
                                     self.tileGrid.calculate_price)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(openFile)
        file_menu.addAction(newFile)
        file_menu.addAction(saveFile)

        tools_menu = menu_bar.addMenu('&Tools')
        tools_menu.addAction(select_tool)
        tools_menu.addAction(print_sequence_tool)
        tools_menu.addAction(eraser_tool)
        tools_menu.addAction(connection_tool)
        tools_menu.addAction(filter_tool)
        tools_menu.addAction(generate_tool)
        tools_menu.addAction(get_price_tool)

        self.show()

    def selectSelectionTool(self):
        self.tileGrid.connection_addition_tool.terminate_connection()
        self.tileGrid.tool = self.tileGrid.selection_tool

    def selectPrintSeqTool(self):
        self.tileGrid.connection_addition_tool.terminate_connection()
        self.tileGrid.tool = self.tileGrid.print_sequence_tool

    def selectEraserTool(self):
        self.tileGrid.connection_addition_tool.terminate_connection()
        self.tileGrid.tool = self.tileGrid.eraser_tool

    def selectConnectionAdditionTool(self):
        self.tileGrid.connection_addition_tool.terminate_connection()
        self.tileGrid.tool = self.tileGrid.connection_addition_tool

    def filterTool(self):
        self.tileGrid.connection_addition_tool.terminate_connection()
        self.tileGrid.filter_tool.action()

    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './designs', "*.yaml")
        self.tileGrid.clean_cells()
        if fname:
            self.tileGrid.load_design(fname)

    def showSaveDialog(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file as', './designs', "*.yaml")
        if fname:
            self.tileGrid.save_design(fname)
