from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QPolygonF
from PyQt5.QtWidgets import QGraphicsItem
from .triangle import Triangle, TriangleLeft, TriangleRight


class Cell(QGraphicsItem):
    def __init__(self, row, col,  parent=None):
        super().__init__(parent)
        self.row, self.col = row, col
        self.pos = (row, col)
        self.Left = TriangleLeft(self)
        self.Left.setPos(0, 0)
        self.Right = TriangleRight(self)
        self.Right.setPos(self.Left.a / 2 + 5 * 2, 0)

    def boundingRect(self):
       #TODO: MB, get the bounding rect of the respective polygon.
       rect = QRectF(0, 0, Triangle.a + Triangle.a / 2 + Triangle.p_w * 2, Triangle.h + Triangle.p_w)
       return rect

    def shape(self):
        #TODO: add proper path corresponding to bounding rect
        #has to be implemented, otherwise bounding rect is the assumed shape
        path = QPainterPath()
        polygon = QPolygonF()
        polygon.append(QPointF(Triangle.a/2, 0))
        polygon.append(QPointF(0, Triangle.h))
        polygon.append(QPointF(Triangle.a, Triangle.h))
        polygon.append(QPointF(Triangle.a+Triangle.a/2, 0))
        path.addPolygon(polygon)
        return path

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        if self.Left.isEnabled():
            self.Left.update()
        if self.Right.isEnabled():
            self.Right.update()