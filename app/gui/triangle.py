from math import sqrt
from PyQt5.QtCore import QRectF, QPointF, Qt, QLineF
from PyQt5.QtGui import QPolygonF, QColor, QPen, QPainterPath, QBrush
from PyQt5.QtWidgets import QGraphicsItem

from app import settings
from .staple import StapleTypeID, Staple, Protector, StapleDomains, ConnectionElement


class Triangle(QGraphicsItem):
    """
        Abstract class knowing how to draw the polygon
    """
    a = 60.0
    h = a * sqrt(3) / 2.0
    p_w = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.pen = QPen(QColor("blue"), self.p_w, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.bg_color = QColor(230, 230, 230, 255)

        self.staple_a = None
        self.staple_b = None
        self.staple_c = None

    def set_staple_by_type(self, type, staple):
        if type is StapleTypeID.A:
            self.staple_a = staple
        if type is StapleTypeID.B:
            self.staple_b = staple
        if type is StapleTypeID.C:
            self.staple_c = staple

    def get_staple_by_type(self, type):
        if type is StapleTypeID.A:
            return self.staple_a
        if type is StapleTypeID.B:
            return self.staple_b
        if type is StapleTypeID.C:
            return self.staple_c

    def has_staple_class_type(self, staple_class_type):
        if type(self.staple_a) is staple_class_type:
            return True
        if type(self.staple_b) is staple_class_type:
            return True
        if type(self.staple_c) is staple_class_type:
            return True
        return False

    def shape(self):
        path = QPainterPath()
        path.addPolygon(self.polygon)
        return path

    def boundingRect(self):
        pen_w = self.pen.width()
        return QRectF(0 - pen_w, 0 - pen_w, self.a + pen_w, self.h + pen_w)

    def load_oligo(self, item, plate_name):
        seq = item["seq"]

        fabric = Staple
        if item["protector"]:
            fabric = Protector

        if item["stype"] == "A":
            self.staple_a = fabric(self, seq=seq, type_id=StapleTypeID.A, plate_name=plate_name, info=item)
            return self.staple_a

        if item["stype"] is "B":
            self.staple_b = fabric(self, seq=seq, type_id=StapleTypeID.B, plate_name=plate_name, info=item)
            return self.staple_b

        if item["stype"] is "C":
            self.staple_c = fabric(self, seq=seq, type_id=StapleTypeID.C, plate_name=plate_name, info=item)
            return self.staple_c

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        if not self.isEnabled():
            return
        QPainter.setPen(QPen(QColor("white")))
        QPainter.setBrush(QBrush(self.bg_color))
        QPainter.drawPolygon(self.polygon)

        AB = QLineF(self.vertex_A, self.vertex_B)
        BC = QLineF(self.vertex_B, self.vertex_C)
        CA = QLineF(self.vertex_C, self.vertex_A)

        vertices = [self.vertex_A, self.vertex_B, self.vertex_C]

        if self.staple_a:
            self.staple_a.draw(QPainter, vertices)
        if self.staple_b:
            self.staple_b.draw(QPainter, vertices)
        if self.staple_c:
            self.staple_c.draw(QPainter, vertices)

    def __str__(self):
        return "\n".join(map(str, [
            "-" * 80,
            ("L_" if type(self) is TriangleLeft else "R_") + str(self.parent.row) + "_" + str(self.parent.col),
            self.staple_a,
            self.staple_b,
            self.staple_c,
            "-" * 80
        ]))

    def random_fill(self, pool):
        for staple in (self.staple_a, self.staple_b, self.staple_c):
            # only works only if no seq assigned
            staple.random_fill(pool)

    def fill_by(self, neighbors, pool):
        mp = {
            StapleTypeID.A: [StapleTypeID.A, StapleTypeID.B],
            StapleTypeID.B: [StapleTypeID.B, StapleTypeID.C],
            StapleTypeID.C: [StapleTypeID.C, StapleTypeID.A],
        }
        nxt = {
            StapleTypeID.A: StapleTypeID.B,
            StapleTypeID.B: StapleTypeID.C,
            StapleTypeID.C: StapleTypeID.A
        }

        for stype, neighbor in zip(StapleTypeID, neighbors):
            strand = self.get_staple_by_type(stype)
            if strand : #makes sure we do have a strand
                strand_type_1, strand_type_2 = mp[stype]
                neighbor_stand1, neighbor_strand2 = neighbor.get_staple_by_type(strand_type_1), \
                                                    neighbor.get_staple_by_type(strand_type_2)

                self.__strand_staple_neighbor_staple(neighbor_stand1, neighbor_strand2, nxt, strand)
                self.__strand_protector_neighbor_staple(neighbor_stand1, neighbor_strand2, strand)
                self.__strand_connection_neighbor_staple(neighbor_stand1, neighbor_strand2, strand, pool)

    def _get_triangle_pos(self):
        lst = []
        a = lst.append
        row, col = self.parent.pos
        a(row)
        a(col)
        if type(self) is TriangleLeft:
            a("L")
        else:
            a("R")
        return lst

    def __strand_protector_neighbor_staple(self, neighbor_stand1, neighbor_strand2, strand):
        if type(strand) is Protector and type(neighbor_stand1) is Staple:
            strand.short = neighbor_strand2.get_rev_c_or_none(StapleDomains.short)
            strand.long1 = neighbor_stand1.get_rev_c_or_none(StapleDomains.long2)
            strand.long2 = neighbor_stand1.get_rev_c_or_none(StapleDomains.long1)

    def __strand_staple_neighbor_staple(self, neighbor_stand1, neighbor_strand2, nxt, strand):
        if type(strand) is Staple and type(neighbor_stand1) is Staple:
            if not strand.long1:
                strand.long1 = neighbor_strand2.get_rev_c_or_none(StapleDomains.short)
            if not strand.long2:
                strand.long2 = neighbor_stand1.get_rev_c_or_none(StapleDomains.long2)
            # we can fill out also the next fragment of the next strand
            nxt_strand = self.get_staple_by_type(nxt[strand.type_id])
            if not nxt_strand.short:
                nxt_strand.short = neighbor_stand1.get_rev_c_or_none(StapleDomains.long1)

    def __strand_connection_neighbor_staple(self, neighbor_strand1, neighbor_strand2, strand, pool=None):
        if type(strand) is ConnectionElement and type(neighbor_strand1) is Staple:
            # if it has an assigned sequence we need to assign the rev_c to the neighbors
            # for Connection elements all domains have to be filled out so we can check only 1 domain

            if neighbor_strand1.long1 and not strand.short:  # rely only on first neighbor
            #if neighbor_strand1.long1:  # rely only on first neighbor
                # the sequence based on the neighborhood (if they have a seq )
                strand.info = None
                strand.short = neighbor_strand2.get_rev_c_or_none(StapleDomains.short)
                strand.long1 = neighbor_strand1.get_rev_c_or_none(StapleDomains.long2)
                strand.long2 = neighbor_strand1.get_rev_c_or_none(StapleDomains.long1)
            elif strand.info:
                return #do nothing if we have already generated the sequences
            # TODO:check this section, as inner are now generated first
            # if not strand.short: #makes sure that we do have a seq
            #    # otherwise we assign a random seq and forward it to the neighbors
            #    strand.random_fill(pool)
            else:
                neighbor_strand2.info = None
                neighbor_strand1.info = None

                neighbor_strand2.short = strand.get_rev_c_or_none(StapleDomains.short)
                neighbor_strand1.long2 = strand.get_rev_c_or_none(StapleDomains.long1)
                neighbor_strand1.long1 = strand.get_rev_c_or_none(StapleDomains.long2)

                neighbor_strand1.triangle.set_staple_by_type(neighbor_strand1.type_id,
                                                             neighbor_strand1)
                neighbor_strand2.triangle.set_staple_by_type(neighbor_strand2.type_id,
                                                             neighbor_strand2)

            # print("Connection strand looks like ")
            # print(strand)
            # print(strand.short is not None)

            # now we just need to change the seq for the to_protector if it does not have a seq (see #1)
            to_strand = strand.to_element
            print("*" * 80)
            print("to_strand", type(to_strand))
            if not to_strand.short:
                to_strand.info = None
                to_strand.short = neighbor_strand1.long1
                to_strand.long1 = neighbor_strand1.long2
                to_strand.long2 = neighbor_strand2.short
                # update the triangle
                to_strand.triangle.set_staple_by_type(to_strand.type_id, to_strand)


class TriangleLeft(Triangle):
    def __init__(self, parent=None):
        super().__init__(parent)
        pen_w = self.pen.width()
        xs, ys = pen_w, pen_w
        a = self.a
        h = self.h

        self.vertex_A = QPointF(xs, ys + h)
        self.vertex_B = QPointF(xs + a, ys + h)
        self.vertex_C = QPointF(xs + a / 2, ys)

        self.polygon = QPolygonF()
        self.polygon.append(self.vertex_A)
        self.polygon.append(self.vertex_B)
        self.polygon.append(self.vertex_C)

    def get_neighbor_cords(self):
        row, col = self.parent.pos
        return [
            [row + 1, col + 0, "R"],  # bottom staple A
            [row + 0, col + 0, "R"],  # right staple B
            [row + 0, col - 1, "R"]  # left staple C
        ]


class TriangleRight(Triangle):
    def __init__(self, parent=None):
        super().__init__(parent)
        a = self.a
        h = self.h
        pen_w = self.pen.width()
        xs, ys = pen_w, pen_w

        self.vertex_B = QPointF(xs, ys)
        self.vertex_A = QPointF(xs + a, ys)
        self.vertex_C = QPointF(xs + a / 2, ys + h)

        self.polygon = QPolygonF()
        self.polygon.append(self.vertex_A)
        self.polygon.append(self.vertex_B)
        self.polygon.append(self.vertex_C)

    def get_neighbor_cords(self):
        row, col = self.parent.pos
        return [
            [row - 1, col + 0, "L"],  # top staple A
            [row + 0, col + 0, "L"],  # right staple B
            [row + 0, col + 1, "L"]  # left staple C
        ]
