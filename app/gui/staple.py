from enum import Enum
from math import sqrt
from random import randint
from PyQt5.QtCore import QLineF, Qt
from PyQt5.QtGui import QPen, QColor

from app import settings


class StapleTypeID(Enum):
    A = 0
    B = 1
    C = 2


class StapleDomains(Enum):
    short = 0
    space = 1
    long1 = 2
    long2 = 3


class Staple:
    compl = {"A": "T", "C": "G", "T": "A", "G": "C", "N": "N"}
    p_w = 5
    a = 60.0
    h = a * sqrt(3) / 2.0

    # (3,0,2,3)
    def __init__(self, triangle=None, seq=None, type_id=None, seq_map=(11, 2, 11, 10), plate_name="To order",
                 info=None):
        self.triangle = triangle
        self.type_id = type_id
        # self.protector = protector
        self.seq_map = seq_map

        self.plate_name = plate_name
        self.info = info

        if seq and not "None" in seq:
            self.short = seq[0]  # seq[0                : sum(seq_map[:1])]
            self.space = seq[1]  # seq[sum(seq_map[:1]) : sum(seq_map[:2])]
            self.long1 = seq[2]  # seq[sum(seq_map[:2]) : sum(seq_map[:3])]
            self.long2 = seq[3]  # seq[sum(seq_map[:3]) :]

        else:
            self.short = None
            l = self.seq_map[StapleDomains.space.value]
            self.space = "T" * l
            self.long1 = None
            self.long2 = None

        if self.type_id is StapleTypeID.A:
            self.pen = QPen(QColor("orange"), self.p_w, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        if self.type_id is StapleTypeID.B:
            self.pen = QPen(QColor("green"), self.p_w, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        if self.type_id is StapleTypeID.C:
            self.pen = QPen(QColor("blue"), self.p_w, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)


    def plate_row(self):
        return self.info["plate_id"][0]

    def get_rev_c_or_none(self, domain_type):
        seq = None
        if domain_type is StapleDomains.short:
            seq = self.short
        if domain_type is StapleDomains.space:
            seq = self.space
        if domain_type is StapleDomains.long1:
            seq = self.long1
        if domain_type is StapleDomains.long2:
            seq = self.long2
        if seq:
            return "".join(self.compl[c] for c in seq[::-1])
        else:
            return None

    def random_fill(self, pool):
        # def rand_str(ln):
        #    return "".join(choice("ATCG") for i in range(ln))
        s = pool.get_next()
        if not self.short:
            self.short = s.short
            # l = self.seq_map[StapleDomains.short.value]
            # self.short =  rand_str(l)
        if not self.long1:
            self.long1 = s.long1
            # l = self.seq_map[StapleDomains.long1.value]
            # self.long1 =  rand_str(l)
        if not self.long2:
            self.long2 = s.long2
        pool.add_staple(self)
        # l = self.seq_map[StapleDomains.long2.value]
        # self.long2 =  rand_str(l)

    def draw(self, QPainter, vertices):
        def short_domain(side, f=0.3):
            r = side.unitVector()
            r = -r.p1() + r.p2()
            p1 = side.p1() + r * (self.a - self.a * f)
            p2 = side.p2()  # - r * self.a * f
            return QLineF(p1, p2)

        def long_domain(side, f=0.6):
            r = side.unitVector()
            r = -r.p1() + r.p2()
            p1 = side.p1()
            p2 = side.p2() - r * self.a * 0.4
            return QLineF(p1, p2)

        def draw_staple(side1, side2):
            QPainter.setPen(self.pen)
            QPainter.drawLine(short_domain(side1))
            QPainter.drawLine(long_domain(side2))

        vertex_A, vertex_B, vertex_C = vertices
        AB = QLineF(vertex_A, vertex_B)
        BC = QLineF(vertex_B, vertex_C)
        CA = QLineF(vertex_C, vertex_A)

        if self.type_id is StapleTypeID.A:
            draw_staple(CA, AB)

        if self.type_id is StapleTypeID.B:
            draw_staple(AB, BC)

        if self.type_id is StapleTypeID.C:
            draw_staple(BC, CA)

    def __str__(self):
        if self.info:
            plate_pos = self.info["plate_id"]
        return "\n".join(map(str,
                             [
                                 str(self.type_id) + " " + str(type(self)),
                                 #"plate name:" + self.plate_name + " " + plate_pos,
                                 " ".join(map(str, [self.short,
                                                    self.space,
                                                    self.long1,
                                                    self.long2]
                                              ))
                             ]))

    def seq(self):
        s = []
        a = s.append
        a(self.short)
        a(self.space)
        a(self.long1)
        a(self.long2)
        return "".join(map(str, s))


class Protector(Staple):
    def __init__(self, triangle=None, seq=None, type_id=None, seq_map=(11, 0, 10, 11), plate_name="To order",
                 info=None):
        super().__init__(triangle, seq, type_id, seq_map, plate_name=plate_name, info=info)

    def draw(self, QPainter, vertices):
        def draw_protector(side):
            r = side.unitVector()
            r = -r.p1() + r.p2()
            p1 = side.p1() + r * self.p_w
            p2 = side.p2() - r * self.p_w

            QPainter.setPen(self.pen)
            QPainter.drawLine(QLineF(p1, p2))

        vertex_A, vertex_B, vertex_C = vertices
        AB = QLineF(vertex_A, vertex_B)
        BC = QLineF(vertex_B, vertex_C)
        CA = QLineF(vertex_C, vertex_A)
        if self.type_id is StapleTypeID.A:
            draw_protector(AB)
        if self.type_id is StapleTypeID.B:
            draw_protector(BC)
        if self.type_id is StapleTypeID.C:
            draw_protector(CA)


class ConnectionElement(Protector):
    def __init__(self, protector, protector2=None, color=None):
        super().__init__(protector.triangle, [protector.short, protector.space,protector.long1,protector.long2],
                         protector.type_id, protector.seq_map,
                         info=protector.info, plate_name=None)#protector.plate_name)
        self.short, self.space, self.long1, self.long2 = None, None,None,None
        self.info = {}

        self.pen.setStyle(Qt.DotLine)
        if not color:
            self.pen.setColor(QColor(randint(0, 200), randint(0, 200), randint(0, 200), 255))
        else:
            self.pen.setColor(color)

        self.prev_protector = protector
        self.to_element = protector2

    def fill_by(self, protector):
        self.short = protector.short
        self.space = protector.space
        self.long1 = protector.long1
        self.long2 = protector.long2
        self.info = protector.info

        print(self.info)

    def connect_triangles(self, protector2):
        protector2 = ConnectionElement(protector2, self, self.pen.color())
        protector2.short, protector2.space, protector2.long1, protector2.long2 = None, None,None,None
        protector2.triangle.set_staple_by_type(protector2.type_id, protector2)
        self.to_element = protector2
