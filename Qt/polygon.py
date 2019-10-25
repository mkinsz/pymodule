import sys
import random
from copy import deepcopy
from PySide2.QtWidgets import (QApplication, QPushButton, QWidget)
from PySide2.QtCore import Slot, Qt, QPoint
from PySide2.QtGui import qRgb, QPainter, QPen, QBrush, QPolygon, QPixmap, QColor, QFont


def powlength(p1, p2):
    return pow(p1.x() - p2.x(), 2.0) + pow(p1.y() - p2.y(), 2.0)


def checkpoint(points, testx, testy):
    count = len(points)
    if count < 3:
        return False

    vertx = []
    verty = []
    for pos in points:
        vertx.append(pos.x())
        verty.append(pos.y())

    i = c = 0
    j = count - 1
    while i < count:
        b1 = (verty[i] > testy) != (verty[j] > testy)
        b2 = False
        if verty[j] == verty[i]:
            b2 = (vertx[i] > testx) != (vertx[j] < testx)
        else:
            b2 = (testx < (vertx[j] - vertx[i]) * (testy -
                                                   verty[i]) / (verty[j] - verty[i]) + vertx[i])

        if b1 and b2:
            c = not c
        j = i
        i += 1

    return c


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.pressed = False
        self.selectedIndex = -1
        self.lineColor = qRgb(34, 163, 169)
        self.lineWidth = 2
        self.selectColor = qRgb(0, 120, 200)
        self.polygonColor = qRgb(0, 255, 255)
        self.dotRadius = 4
        self.dotColor = qRgb(34, 163, 169)
        self.setMouseTracking(True)
        self.tempPoints = []
        self.tempPolygons = []
        self.selectedEllipseIndex = -1
        self.selectDotVisible = True
        self.pressedPolygon = {}

        self.button = QPushButton("&Delete All", self)
        # Connecting the signal
        self.button.clicked.connect(self.magic)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            return super().mousePressEvent(event)

        p = event.pos()
        self.pressed = True
        self.lastPoint = self.mapToGlobal(p)

        if 0 == len(self.tempPoints):
            selectedPot = False
            self.selectedEllipseIndex = -1
            if self.selectedIndex != -1:
                i = len(self.tempPolygons[self.selectedIndex]['pos']) - 1
                while i >= 0:
                    if powlength(p, self.tempPolygons[self.selectedIndex]['pos'][i]) < 36:
                        selectedPot = True
                        self.selectedEllipseIndex = i
                        self.ellipsePos = self.tempPolygons[self.selectedIndex]['pos'][i]
                        break
                    i -= 1

            if selectedPot:
                return

            self.selectedIndex = -1
            i = len(self.tempPolygons) - 1
            while i >= 0:
                self.tempPolygons[i]['selected'] = checkpoint(
                    self.tempPolygons[i]['pos'], p.x(), p.y())
                if self.tempPolygons[i]['selected']:
                    if self.selectedIndex == - 1:
                        self.selectedIndex = i
                    else:
                        self.tempPolygons[i]['selected'] = False
                i -= 1

            if self.selectedIndex != -1:
                index = len(self.tempPolygons) - 1
                p = self.tempPolygons.pop(self.selectedIndex)
                self.tempPolygons.append(p)
                self.selectedIndex = index
                self.pressedPolygon = deepcopy(self.tempPolygons[index])

            self.update()

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.tempPoint = event.pos()
        if self.pressed and (self.selectedIndex != -1):
            delta = self.mapToGlobal(self.tempPoint) - self.lastPoint
            points = self.tempPolygons[self.selectedIndex]['pos']
            length = len(points)

            if self.selectedEllipseIndex != -1:
                points[self.selectedEllipseIndex] = self.ellipsePos + delta
            elif self.selectedIndex != -1:
                i = 0
                while i < length:
                    points[i] = self.pressedPolygon['pos'][i] + delta
                    i += 1

        self.update()

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if Qt.RightButton == event.button():
            self.clearTemp()
            return super().mouseReleaseEvent(event)

        self.pressed = False
        if self.selectedIndex != -1:
            return

        point = event.pos()
        if len(self.tempPoints) > 0:
            length = pow(self.tempPoints[0].x(
            ) - point.x(), 2.0) + pow(self.tempPoints[0].y() - point.y(), 2.0)
            if length < 100:
                if len(self.tempPoints) >= 3:
                    pol = {'pos': self.tempPoints.copy(), 'selected': False}
                    self.tempPolygons.append(pol)

                self.tempPoints.clear()
                self.update()
                return

        self.tempPoints.append(point)
        self.update()
        return super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing, True)

        for p in self.tempPolygons:
            self.drawPolygon(painter, p)

        self.drawLines(painter, self.tempPoints)

        return super().paintEvent(event)

    def drawPolygon(self, painter, data):
        painter.save()
        pen = QPen()
        pen.setColor(self.lineColor)
        pen.setWidth(self.lineWidth)
        painter.setPen(pen)
        if data['selected']:
            painter.setBrush(QBrush(self.selectColor))
        else:
            painter.setBrush(QBrush(self.polygonColor))

        polygon = QPolygon(data['pos'])
        painter.drawPolygon(polygon)

        # dot
        if self.selectDotVisible and data['selected']:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self.dotColor))
            for point in data['pos']:
                painter.drawEllipse(point, self.dotRadius, self.dotRadius)

        painter.restore()

    def drawLines(self, painter, points):
        painter.save()

        count = len(points)
        if count > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self.dotColor))
            i = 0
            while i < count:
                painter.drawEllipse(points[i], self.dotRadius, self.dotRadius)
                i += 1

            pen = QPen()
            pen.setColor(self.lineColor)
            pen.setWidth(self.lineWidth)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            for i in range(count - 1):
                painter.drawLine(points[i], points[i+1])

            painter.drawLine(points[count-1], self.tempPoint)

        painter.restore()

    def clearTemp(self):
        self.tempPoints.clear()
        self.selectedIndex = -1
        self.update()

    def clearAll(self):
        self.tempPoints.clear()
        self.tempPolygons.clear()
        self.selectedIndex = -1
        self.update()

    @Slot()
    def magic(self):
        self.clearAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
