from PyQt5.QtWidgets import QGraphicsView
from yaml import load

from app.gui.cell import Cell
from app.gui.staple import StapleTypeID, ConnectionElement, Staple
from app.util.sequence_generator import SequencePool

path = r"D:\PycharmProjects\HexTiles\app\designs\Structures\4R4C_2T.yaml"
out = r"D:\PycharmProjects\HexTiles\app\designs\Structures\4R4C_2T_asym_mod.yaml"


def push_base(st1, st2):
    last_base = st1.short[-1]
    st1.short = st1.short[:-1]
    st2.long1 = last_base + st2.long1


def pull_base(st1):
    first_base = st1.short[0]
    st1.short = st1.short[1:]
    st1.long2 = st1.long2 + first_base


def update_info(st1):
    st1.info["seq"] = [st1.long1, st1.space, st1.long2, st1.short]


class Grid(QGraphicsView):
    def __init__(self):
        # do not call init of super class as this script is not graphical
        self.seq_pool = SequencePool()

        self.rows = 8
        self.colls = 8
        self.cells = [[None for i in range(self.colls)] for j in range(self.rows)]

        for j in range(self.rows):
            for i in range(self.colls):
                cell = Cell(j, i)
                self.cells[j][i] = cell

    def triangle_by_pos(self, pos):
        row, col, t = pos
        cell = self.cells[row][col]
        if t is "L":
            return cell.Left
        if t is "R":
            return cell.Right

    def load_design(self, path):
        with open(path, "r") as file:
            data = load(file)

        for plate_name, plate in data.items():
            if not "Connectors" in plate_name:
                # loop on staples\protectors
                for name, row in plate["rows"].items():
                    for item in row:
                        pos = item["pos"]
                        triangle = self.triangle_by_pos(pos)
                        oligo = triangle.load_oligo(item, plate_name)
                        if oligo:
                            self.seq_pool.add_staple(oligo)

            else:
                # loop on connectors
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

    def save_design(self, fname="./designs/des1.yaml"):
        from yaml import dump
        plates = {}
        for row in self.cells:
            for cell in row:
                for triangle in (cell.Left, cell.Right):
                    for staple in map(triangle.get_staple_by_type, StapleTypeID):
                        if staple:
                            # check wherever plate name is already defined
                            if not staple.plate_name in plates:
                                plates[staple.plate_name] = {"rows": {}}
                            # chech the same for the row
                            if not staple.plate_row() in plates[staple.plate_name]["rows"]:
                                plates[staple.plate_name]["rows"][staple.plate_row()] = []
                            # assign staple
                            plates[staple.plate_name]["rows"][staple.plate_row()].append(staple.info)

        with open(fname, "w") as file:
            file.write(dump(plates))
            print("Dump completed.")


g = Grid()
g.load_design(path)

triangles_to_process = []
a = triangles_to_process.append

for rows in g.cells:
    for cell in rows:
        for triangle in [cell.Left, cell.Right]:
            if triangle.has_staple_class_type(Staple):
                a(triangle)

inc = 0

staples = []
a = staples.append

for triangle in triangles_to_process:
    # alias
    stap_a = triangle.staple_a
    stap_b = triangle.staple_b
    stap_c = triangle.staple_c

    # reformat
    push_base(stap_a, stap_b)
    push_base(stap_b, stap_c)
    push_base(stap_c, stap_a)

    push_base(stap_a, stap_b)
    push_base(stap_b, stap_c)
    push_base(stap_c, stap_a)

    pull_base(stap_a)
    pull_base(stap_b)
    pull_base(stap_c)

    pull_base(stap_a)
    pull_base(stap_b)
    pull_base(stap_c)

    update_info(stap_a)
    update_info(stap_b)
    update_info(stap_c)

    a(stap_a)
    a(stap_b)
    a(stap_c)

    inc += 3
    # print("reformated: ~~~")
    #
    # print(triangle.staple_b)
    # print(triangle.staple_c)
    # print(triangle.staple_a)
    #
    # print("~~~" * 20)

# save modified file
# g.save_design(out)
# pprint (short_domains)


from pprint import pprint

hist = {}
for s in staples:
    for d in [s.long1, s.long2, s.short]:
        if not d in hist:
            hist[d] = [s]
        else:
            hist[d].append(s)

repeating_overhangs = [[(vi.info["seq"], vi.info["stype"], vi.info["pos"]) for vi in v]
                           for k, v in hist.items()
                           if len(v) > 1]

pprint(repeating_overhangs)
