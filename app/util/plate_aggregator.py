from ..gui.triangle import TriangleLeft
from ..gui.staple import Staple, Protector, \
                           StapleTypeID, ConnectionElement


class Plate:
    n_to_r = {
        0 : "A", 1 : "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"
    }
    def __init__(self, plate_name="FlatTruss", design_name=""):
        self.cells =[[None for
                      i in range(12)] for j in range(8)]

        self.design_name = design_name
        self.pointer_pos = self._get_pointer_pos()
        self.pointer = None
        self.plate_name = plate_name


    def _get_pointer_pos(self):
        for i in range(9):
            for j in range(12):
                yield i,j
    def add_oligo(self, oligo):
        self.pointer = next(self.pointer_pos,None)
        if not self.pointer:
            raise Exception("Plate full")
        row, col = self.pointer
        self.cells[row][col] = self.convert_to_dict_item(oligo,row,col)
    def _name_from(self,oligo):
        s = []
        a = s.append
        a("MM")
        a(oligo.triangle.parent.row)
        a(oligo.triangle.parent.col)
        if type(oligo.triangle) is TriangleLeft:
            a(1)
        else:
            a(2)

        for stype, letter in zip(StapleTypeID,"ABC"):
            if oligo.type_id is stype:
                a(letter)
                break
        return "_".join(map(str,s))
    def _get_triangle_pos(self, triangle):
        lst = []
        a = lst.append
        row, col = triangle.parent.pos
        a(row)
        a(col)
        if type(triangle) is TriangleLeft:
            a("L")
        else:
            a("R")
        return lst
    def _check_is_protector(self, oligo):
        return type(oligo) == Protector or self._check_is_connection(oligo)

    def _check_is_connection(self, oligo):
        return type(oligo) == ConnectionElement
    def convert_to_dict_item(self, oligo,row,col):
        item = {}
        item["design"] = [self.design_name]
        item["name"] = self._name_from(oligo)
        item["plate_id"] = self.n_to_r[row] + str(col+1)
        item["pos"] = self._get_triangle_pos(oligo.triangle)
        item["seq"] = [oligo.short, oligo.space, oligo.long1, oligo.long2]
        item["stype"] = item["name"][-1]
        item["connection"] = self._check_is_connection(oligo)
        if item["connection"]:
            item["to_element_name"] = self._name_from(oligo.to_element)
            item["to_element_pos"] = self._get_triangle_pos(oligo.to_element.triangle)
            item["to_element_stype"] = item["name"][-1]
        item["protector"] = self._check_is_protector(oligo)

        return item

    def to_dict(self):
        plate = {"rows":{}}
        for nr, row in enumerate(self.cells):
            r = []
            for nc, cell in enumerate(row):
                if cell is not None:
                    r.append(cell)
            if r:
                plate["rows"][self.n_to_r[nr]] = r
        return {self.plate_name : plate}

class PlateAggregator:
    def __init__(self, plate_name_prefix, design_name):
        self.design_name = design_name

        self.plate_name_prefix = plate_name_prefix
        self.staple_plates = []
        self.staple_plate = self.get_plate(self.stpl_plate_indx())

        self.protector_plates = []
        self.protector_plate = self.get_plate(self.prt_plate_indx())

        self.connection_plates = []
        self.connection_plate = self.get_plate(self.cnt_plate_indx())



    def get_plate(self, postfix_name):
        return Plate(self.plate_name_prefix + postfix_name, self.design_name)

    def stpl_plate_indx(self):
        return "_Staples_" + str(len(self.staple_plates))

    def prt_plate_indx(self):
        return "_Protectors_"+ str(len(self.protector_plates))
    def cnt_plate_indx(self):
        return "_Connectors_"+ str(len(self.connection_plates))

    def add_oligo(self, oligo):
        if type(oligo) is Staple:
            try:
                self.staple_plate.add_oligo(oligo)
            except:
                self.staple_plates.append(self.staple_plate)
                self.staple_plate = self.get_plate(self.stpl_plate_indx())
                self.staple_plate.add_oligo(oligo)
        if type(oligo) is Protector:
            try:
                self.protector_plate.add_oligo(oligo)
            except:
                self.protector_plates.append(self.protector_plate)
                self.protector_plate = self.get_plate(self.prt_plate_indx())
                self.protector_plate.add_oligo(oligo)

        if type(oligo) is ConnectionElement:
            try:
                self.connection_plate.add_oligo(oligo)
            except:
                self.connection_plates.append(self.connection_plate)
                self.connection_plate = self.get_plate(self.cnt_plate_indx())
                self.connection_plate.add_oligo(oligo)



    def get_staple_plates(self):
        return self.staple_plates + [self.staple_plate]

    def get_protector_plates(self):
        return self.protector_plates + [self.protector_plate]

    def get_connection_plates(self):
        return self.connection_plates + [self.connection_plate]


    def update_order(self, plates):
        for plate in (self.get_staple_plates()+self.get_protector_plates()
                          +self.get_connection_plates()):
            plates.update(plate.to_dict())


