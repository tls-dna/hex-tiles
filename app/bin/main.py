import sys
sys.path.append('../../')
from PyQt5.QtWidgets import QApplication
from app.gui.tile_router_app import RouterAppMain
from app import settings


print(settings)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = RouterAppMain()
    app.exec_()
