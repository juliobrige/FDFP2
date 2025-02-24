from sqlmodel import Field, SQLModel, create_engine, Relationship
from enum import Enum
from datetime import date


class Bancos(Enum):
    MILLENIUBIM = 'milleniumnim'
    STANDARBANK = 'standarbank'
    BCI = 'bci'


class Status(Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo' 

class Tipos(Enum):
   ENTRADA = 'entrada'
   SAIDA = 'saida'     



class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    valor: float
    banco: Bancos = Field(default=Bancos.MILLENIUBIM)
    status: Status = Field(default=Status.ATIVO)

class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship()
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data : date

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

 
if __name__ == "__main__":
    SQLModel.metadata.create_all(engine) 
