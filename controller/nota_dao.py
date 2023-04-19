import sqlite3



from model.nota import Nota

class DataBase:

   def __init__(self, nome = 'system.db'):

       self.connection = None
       self.name = nome


   def connect(self):

       self.connection = sqlite3.connect(self.name)

   def close_connection(self):

       try:
           self.connection.close()

       except Exception as e:

           print(e)


   def create_table_nota(self):

       self.connect()
       cursor = self.connection.cursor()
       cursor.execute(
           """
           CREATE TABLE IF NOT EXISTS NOTA( 
           ID INTEGER PRIMARY KEY AUTOINCREMENT, 
           NOME_NOTA TEXT, 
           DATA_NOTA DATE, 
           TEXTO_NOTA TEXT 
            );
           """)

       self.close_connection()

   def criar_nota(self, nota=Nota):

        self.connect()

        cursor = self.connection.cursor()

        campos_nota = ('NOME_NOTA', 'DATA_NOTA', 'TEXTO_NOTA')

        valores = f"'{nota.nome_nota}','{nota.data_nota}','{nota.texto_nota}'"

        try:

            cursor.execute(f"""INSERT INTO NOTA {campos_nota} VALUES ({valores})""")
            self.connection.commit()

            return 'Ok'

        except sqlite3.Error as e:
            return str(e)

        finally:

            self.close_connection()

   def ler_notas(self, id):

         self.connect()

         try:

            cursor = self.connection.cursor()
            cursor.execute(f""" SELECT * FROM NOTA  WHERE ID = {id}""")
            return  cursor.fetchone()
         except sqlite3.Error as e:
             return None
         finally:
             self.close_connection()

   def ler_notas_notas(self):

        self.connect()

        try:

            cursor = self.connection.cursor()
            cursor.execute("SELECT *  FROM NOTA")
            notas= cursor.fetchall()

            return notas

        except sqlite3.Error as e:

            print(f'Erro {e} ')

            return
        finally:

            self.close_connection()


   def delete_notas(self, id):
        self.connect()
        try:

            cursor = self.connection.cursor()
            cursor.execute(f"""DELETE FROM NOTA WHERE ID = {id}""")
            self.connection.commit()
            return 'Ok'

        except sqlite3.Error as e:
            print(e)

        finally:
            self.close_connection()




   def atualizar_nota(self, nota=Nota):

        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""UPDATE NOTA SET
                   NOME_NOTA = '{nota.nome_nota}',
                   TEXTO_NOTA = '{nota.texto_nota}'
                   WHERE ID = {nota.id}""")

            self.connection.commit()

            return 'Ok'
        except sqlite3.Error as e:
             return e
        finally:
            self.close_connection()