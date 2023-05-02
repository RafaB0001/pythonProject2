import sys

from PySide6.QtWidgets import QApplication

import controller.nota_dao
from controller.nota_dao import DataBase
from view.tela_principal import MainWindow


db = controller.nota_dao.DataBase()
db.connect()
db.create_table_nota()
db.close_connection()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()




