from os.path import basename
from random import randint
from yaml import full_load
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QMessageBox

from .cell import Cell
from .tools import EraserTool, SelectorTool, ConnectionAdditionTool, FilterTool, PrintSequencesTool
from .triangle import Triangle, TriangleLeft, TriangleRight
from .staple import StapleTypeID, Staple, ConnectionElement, Protector
from ..util.plate_aggregator import PlateAggregator
from ..util.sequence_generator import SequencePool


class Grid(QGraphicsView):
    selection_tool = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.seq_pool = SequencePool()

        self.setRenderHint(QPainter.Antialiasing)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        scene = QGraphicsScene()
        self.setScene(scene)

        self.rows = 20
        self.colls = 20
        self.cells = [[None for i in range(self.colls)] for j in range(self.rows)]

        self.selection_tool = SelectorTool(self)
        self.eraser_tool = EraserTool(self)
        self.connection_addition_tool = ConnectionAdditionTool(self)
        self.filter_tool = FilterTool(self)
        self.print_sequence_tool = PrintSequencesTool(self)
        self.tool = self.selection_tool

        # dummy cell
        b_rect = (Cell(-1, -1)).boundingRect()
        dx = b_rect.width() - Triangle.a / 2 + Triangle.p_w * 2
        dy = b_rect.height() + Triangle.p_w
        x, y = 0, 0
        xs, ys = 0, 0

        for j in range(self.rows):
            x = xs - j * dx / 2
            for i in range(self.colls):
                cell = Cell(j, i)
                self.cells[j][i] = cell
                cell.setPos(x, y)
                scene.addItem(cell)
                x += dx
            y += dy

            # self.load_design()

    def triangle_by_pos(self, pos):
        row, col, t = pos
        cell = self.cells[row][col]
        if t is "L":
            return cell.Left
        if t is "R":
            return cell.Right

    def load_design(self, path):
        # path = "./designs/oligo_pool_32_plate_62129.yaml"
        # path = "./designs/oligo_pool_34_plate_64076.yaml"
        # path = "./designs/3R2C_2T.yaml"
        with open(path[0], "r") as file:
            # designs = load(file)["Plate_62129"]
            data = full_load(file)  # ["Plate_64076"]

        for plate_name, plate in data.items():
            print(plate_name)
            if not "Connectors" in plate_name:
                # loop on staples\protectors
                for name, row in plate["rows"].items():
                    for item in row:
                        pos = item["pos"]
                        triangle = self.triangle_by_pos(pos)
                        oligo = triangle.load_oligo(item, plate_name)
                        if oligo:
                            #print(oligo)
                            self.seq_pool.add_staple(oligo)
                        else:
                            print("load broken:")
                            print("plate:", plate_name)
                            print(item)
                        triangle.update()
            else:
                # loop on connectors
                # pass
                for name, row in plate["rows"].items():
                    for item in row:
                        pos = item["pos"]
                        triangle = self.triangle_by_pos(pos)
                        staple = triangle.load_oligo(item, plate_name)

                        print(item["seq"])

                        to_pos = item["to_element_pos"]
                        to_triangle = self.triangle_by_pos(to_pos)

                        to_staple = None
                        if item["to_element_stype"] == "A":
                            to_staple = to_triangle.get_staple_by_type(StapleTypeID.A)
                        if item["to_element_stype"] == "B":
                            to_staple = to_triangle.get_staple_by_type(StapleTypeID.B)
                        if item["to_element_stype"] == "C":
                            to_staple = to_triangle.get_staple_by_type(StapleTypeID.C)

                        triangle.set_staple_by_type(staple.type_id, staple)
                        if to_staple:
                            c = ConnectionElement(staple)
                            c.connect_triangles(to_staple)
                            triangle.set_staple_by_type(staple.type_id, c)
                            c.fill_by(staple)
                            c.to_element.fill_by(to_staple)

                            # c.to_element.info["plate_name"] = plate_name
                            # c.info["plate_name"] = plate_name

    def save_design(self, fname="./designs/des1.yaml"):
        from yaml import dump
        plates = {}
        fname = fname[0] #TODO: Figure out the new way to communicate with the file dialogs in QT
        base_filename = basename(fname)
        design_name = base_filename.split(".")[0]
        p = PlateAggregator("Ord_" + "".join(str(randint(0, 9)) for i in range(5)), design_name)
        for row in self.cells:
            for cell in row:
                for triangle in (cell.Left, cell.Right):
                    for staple in map(triangle.get_staple_by_type, StapleTypeID):
                        if staple and staple.info \
                                and type(
                                    staple) is not ConnectionElement:  # and not staple.info.get("connection", False):
                            # if "Protectors" in staple.info["plate_name"]:
                            print("%s %s %s %s " %
                                  (type(staple), staple.info.get("connection", None), staple.plate_name,
                                   staple.info["name"]))
                            # print("%s %s %s" % (staple.plate_name, staple.info["protector"],staple.info["name"]))

                            # check wherever plate name is already defined
                            if not staple.plate_name in plates:
                                plates[staple.plate_name] = {"rows": {}}
                            # chech the same for the row
                            if not staple.plate_row() in plates[staple.plate_name]["rows"]:
                                plates[staple.plate_name]["rows"][staple.plate_row()] = []
                            # check for updating the design index
                            if not design_name in staple.info["design"]:
                                staple.info["design"].append(design_name)
                            # assign staple
                            plates[staple.plate_name]["rows"][staple.plate_row()].append(staple.info)
                        else:
                            # use plate aggregator to create an order
                            p.add_oligo(staple)
        # append order list
        p.update_order(plates)

        with open(fname, "w") as file:
            file.write(dump(plates))
            print("Dump completed.")

    def clean_cells(self):
        for row in self.cells:
            for cell in row:
                for triangle in (cell.Left, cell.Right):
                    triangle.bg_color = QColor(230, 230, 230, 255)
                    for stype in StapleTypeID:
                        triangle.set_staple_by_type(stype, None)

    def calculate_price(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Price is ")
        msg.setStandardButtons(QMessageBox.Ok)
        s = []
        a = s.append
        a("The price of the ")
        N = 0
        p = 0.0
        quote = 0.12
        for row in self.cells:
            for cell in row:
                for triangle in (cell.Left, cell.Right):
                    for staple in map(triangle.get_staple_by_type, StapleTypeID):
                        if staple and not staple.info and type(staple) is not ConnectionElement:
                            # check if has info - if does - ordered already
                            n_bases = sum(staple.seq_map)
                            p += n_bases * quote
                            N += 1
        a(str(N))
        a(" oligos is ")
        a(str(round(p)))
        a(" euros")

        msg.setText("".join(s))
        msg.exec()

    def mousePressEvent(self, qMouseEvent):
        triangle = self.itemAt(qMouseEvent.pos())
        if type(triangle) is TriangleLeft or type(triangle) is TriangleRight:
            self.tool.action(triangle)

    def mouseDoubleClickEvent(self, qMouseEvent):
        self.mousePressEvent(qMouseEvent)

    def invoke_generate_sequences(self):
        for row in self.cells:
            for cell in row:
                cell.Left.bg_color = QColor(230, 230, 230, 255)
                cell.Right.bg_color = QColor(230, 230, 230, 255)
        # init
        self.generate_sequences()
        self.filter_tool.action()

    def output_design(self, file_path):
        for rows in self.cells:
            for cell in rows:
                for triangle in (cell.Left, cell.Right):
                    for stype in StapleTypeID:
                        staple = triangle.get_staple_by_type(stype)
                        if staple:
                            print(type(triangle), staple)

    def find_triangle_with_property(self, pred):
        # search for first triangle, containing staple items (not connectors or protectors)
        for rows in self.cells:
            for cell in rows:
                for triangle in (cell.Left, cell.Right):
                    if pred(triangle):
                        return triangle
        return None

    def get_neighbors_by_type(self, triangle, processed, staple_class_type):
        # highlite neighbors
        neighbors = map(self.triangle_by_pos, triangle.get_neighbor_cords())
        filtered = []
        # sort the neighbors into bins
        for n in neighbors:
            if n in processed:
                continue
            if n.has_staple_class_type(staple_class_type):
                filtered.append(n)

        return filtered

    def generate_sequences(self):
        print("Generate sequences was pressed.")
        # search for first triangle, containing staple items (not connectors or protectors)
        triangle = self.find_triangle_with_property(lambda tr:
                                                    tr.has_staple_class_type(Staple))
        # nothing added to the grid
        if triangle is None:
            return
        else:
            # add it to process list
            to_process = [triangle]
        # list of done items
        searched = []
        staple_triangles = [triangle]
        protector_triangles = []
        connection_triangles = []
        while to_process:
            # get current triangle
            cur_triangle = to_process.pop()
            # and add it to the list of consumed ones
            searched.append(cur_triangle)

            # needed to run the cycle.
            n_staple_triangles = self.get_neighbors_by_type(cur_triangle, searched, Staple)
            n_protector_triangles = self.get_neighbors_by_type(cur_triangle, searched, Protector)
            n_connection_triangles = self.get_neighbors_by_type(cur_triangle, searched, ConnectionElement)

            staple_triangles.extend(n_staple_triangles)
            protector_triangles.extend(n_protector_triangles)
            connection_triangles.extend(n_connection_triangles)

            neighbors = []
            neighbors.extend(n_protector_triangles)
            neighbors.extend(n_staple_triangles)
            neighbors.extend(n_connection_triangles)
            # and highlite them
            for neighbor in neighbors:
                # neighbor.bg_color = QColor("cyan")
                if neighbor not in to_process and neighbor not in searched:
                    to_process.append(neighbor)

        for t in connection_triangles:
            t.fill_by(map(self.triangle_by_pos, t.get_neighbor_cords()),
                      self.seq_pool)
            t.bg_color = QColor("white")

        for t in staple_triangles:
            t.fill_by(map(self.triangle_by_pos, t.get_neighbor_cords()),
                      self.seq_pool)
            t.random_fill(self.seq_pool)
            t.bg_color = QColor("white")
            # t.bg_color = QColor(0,255,255,50)

        for t in protector_triangles:
            t.fill_by(map(self.triangle_by_pos, t.get_neighbor_cords()),
                      self.seq_pool)
            t.bg_color = QColor("white")
            # t.bg_color = QColor("yellow")
