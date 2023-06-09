from infra.configs.base import  Base
from sqlalchemy import Column, String, Integer , DateTime


class Nota(Base):
    #Nome da tabela a ser criada
    __tablename__ = 'nota'
    #Colunas da tabela que serão criadas na tabela
    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String, nullable=False)
    texto = Column(String, nullable=False)
    prioridade = Column(String, nullable=False)
    data_criacao = Column(DateTime)


    #Função que sobreescreve a maneira de 'printar' a objeto
    def __repr__(self):

        return f'Titulo da nota = {self.titulo}, id = {self.id}'