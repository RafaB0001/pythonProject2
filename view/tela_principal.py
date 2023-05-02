

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QLabel, QLineEdit, QWidget, QPushButton,
                               QAbstractItemView, QTableWidget, QMessageBox, QSizePolicy, QTableWidgetItem, QTextEdit)

from model.nota import Nota
from controller.nota_dao import DataBase
from datetime import date

from infra.configs.connection import DBConnectionHandler


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()



        conn = DBConnectionHandler()
        conn.create_database()

        self.setMinimumSize(500, 500)
        self.setWindowTitle('Bloco de notas')


        self.lbl_id = QLabel('id')
        self.txt_id = QLineEdit()
        self.txt_id.setReadOnly(True)
        self.lbl_nome_nota = QLabel('Título')
        self.txt_nome_nota =QLineEdit()
        self.lbl_texto_nota = QLabel('Texto')
        self.txt_texto_nota = QTextEdit()
        self.txt_data_nota = QTextEdit()
        self.btn_salvar =QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover =QPushButton('Remover')
        self.tabela_nota = QTableWidget()


        self.tabela_nota.setColumnCount(4)
        self.tabela_nota.setHorizontalHeaderLabels(['id', 'Título', 'data', 'Texto'])

        self.tabela_nota.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_nota.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()

        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_nome_nota)
        layout.addWidget(self.txt_nome_nota)
        layout.addWidget(self.lbl_texto_nota)
        layout.addWidget(self.txt_texto_nota)
        layout.addWidget(self.tabela_nota)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.btn_remover.clicked.connect(self.remover_nota)
        self.btn_limpar.clicked.connect(self.limpar_notas)
        self.tabela_nota.cellDoubleClicked.connect(self.carregar_dados)
        self.popula_tabela_notas()



    def salvar_nota(self):

      db = DataBase()

      nota = Nota(self.txt_id.text(), self.txt_nome_nota.text(), date.today(), self.txt_texto_nota.toPlainText())

      if self.btn_salvar.text() == 'Salvar':

          retorno = db.criar_nota(nota)


          if retorno == 'Ok':

              msg = QMessageBox()
              msg.setWindowTitle('Cadastro realizado ')
              msg.setText('Nota cadastrada com sucesso')
              msg.exec()

          elif retorno == 'UNIQUE constraint failed: NOTA.id':

              msg = QMessageBox()
              msg.setIcon(QMessageBox.Critical)
              msg.setWindowTitle('Nota já cadastrado')
              msg.setText(f'O CPF {self.txt_id.text()} já está cadastrado')
              msg.exec()

          else:
              msg = QMessageBox()
              msg.setIcon(QMessageBox.Critical)
              msg.setWindowTitle('Erro ao cadastrar')
              msg.setText('Erro ao cadastrar a cadastrar nota , verifique os dados inserido')
              msg.exec()

      elif self.btn_salvar.text() == 'Atualizar':

          retorno = db.atualizar_nota(nota)

          if retorno == 'Ok':
              msg = QMessageBox()
              msg.setIcon(QMessageBox.Information)
              msg.setWindowTitle('Cadastro realizado ')
              msg.setText('Cadastro realizado com sucesso')
              msg.exec()
              self.limpar_notas()
          else:
              msg = QMessageBox()
              msg.setIcon(QMessageBox.Critical)
              msg.setWindowTitle('Erro ao cadastrar')
              msg.setText('Erro ao cadastrar o cliente, verifique os dados inserido')
              msg.exec()

      self.popula_tabela_notas()
      self.txt_id.setReadOnly(False)


    def criar_notas(self):


        if self.txt_id.text() != '':

            db = DataBase()

            retorno = db.ler_notas(str(self.txt_id.text()))

            if retorno is not None:

                self.btn_salvar.setText('Atualizar')
                msg = QMessageBox()
                msg.setWindowTitle('Nota já Salva')
                msg.setText(f'A nota {self.txt_id.text()} já esta Salva')
                msg.exec()
                self.txt_nome_nota.setText(retorno[1])
                self.txt_texto_nota.setText(retorno[2])
                self.txt_data_nota.setText(retorno[3])
                self.btn_remover.setVisible(True)



    def remover_nota(self):

        msg = QMessageBox()
        msg.setWindowTitle('Remover Nota')
        msg.setText('Este cliente será removido')
        msg.setInformativeText(f'Você deseja remover a nota {self.txt_id.text()} ?')
        msg.setStandardButtons(QMessageBox.Yes  | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button((QMessageBox.No)).setText('Não')


        resposta = msg.exec()

        if resposta == QMessageBox.Yes:

            db = DataBase()

            if db.delete_notas(self.txt_id.text()) == 'Ok':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover cliente')
                nv_msg.setText('Cliente removida com sucesso')
                nv_msg.exec()
                self.limpar_notas()
            else:

                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover cliente')
                nv_msg.setText('Erro ao remover cliente')
                nv_msg.exec()

        self.txt_id.setReadOnly(False)
        self.popula_tabela_notas()


    def limpar_notas(self):

        for widget in self.container.children():
            if isinstance(widget,QLineEdit):
                widget.clear()
            elif isinstance(widget, QTextEdit):
                widget.clear()
        self.btn_remover.setVisible(False)
        self.btn_salvar.setText('Salvar')
        self.txt_id.setReadOnly(False)

    def popula_tabela_notas(self):

        self.tabela_nota.setRowCount(0)
        db = DataBase()
        lista_notas = db.ler_notas_notas()
        self.tabela_nota.setRowCount(len(lista_notas))

        for linha, nota in enumerate(lista_notas):

            for coluna, valor in enumerate(nota):
              self.tabela_nota.setItem(linha, coluna, QTableWidgetItem(str(valor)))


    def carregar_dados(self,row, column):


        self.txt_id.setText(self.tabela_nota.item(row, 0).text())
        self.txt_nome_nota.setText(self.tabela_nota.item(row, 1).text())
        self.txt_texto_nota.setText(self.tabela_nota.item(row, 3).text())
        self.txt_data_nota.setText(self.tabela_nota.item(row, 2).text())
        self.btn_salvar.setText('Atualizar')
        self.btn_remover.setVisible(True)
