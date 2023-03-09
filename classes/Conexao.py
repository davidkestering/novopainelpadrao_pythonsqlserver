import pyodbc
import sys
sys.path.append('../')
import constantes as ct

class Conexao:
    def __init__(self, sServidor='BANCO'):
        self.pConexao = None
        self.pConsulta = None
        self.pBanco = None
        self.sErro = None
        self.sSqlError = None
        self.nLastId = None
        self.sServidor = sServidor
        self.setServidor(sServidor)
        if sServidor == 'LOCAL':
            self.conectaBD('WINDOWS_SERVER\MSSQLSERVER01', 'sa', 'fb123', 'dbteste')
        elif sServidor == 'BANCO':
            self.conectaBD('localhost', '', '', '')
        else:
            raise Exception(f'Não foi possível conectar ao servidor: {sServidor}')

    def setServidor(self, sServidor):
        self.sServidor = sServidor

    def getServidor(self):
        return self.sServidor

    def setLastId(self,nLastId):
        self.nLastId = nLastId

    def conectaBD(self, sHost, sUser, sSenha, sBanco):
        self.pConexao = pyodbc.connect(f"Driver={{SQL Server}};Server={sHost};Database={sBanco};uid={sUser};pwd={sSenha}")

    def execute(self, sSql):
        self.pConsulta = self.pConexao.cursor()
        try:
            self.pConsulta.execute(sSql)
            #NAO USAR COMMIT EM SELECT SIMPLES DO SQLSERVER NAO FUNCIONA E DA ERRO
            #self.pConexao.commit()
        except pyodbc.Error as e:
            self.sSqlError = str(e)
            self.sErro = f'Ocorreu o seguinte erro na consulta: {self.sSqlError} <br> Query: {sSql}'
            self.insereErroSql(sSql)
            return self.getErro()

    def executeInsert(self, sSql):
        self.pConsulta = self.pConexao.cursor()
        try:
            self.pConsulta.execute(sSql)
            sSqlLastId = "SELECT @@IDENTITY"
            self.pConsulta.execute(sSqlLastId)
            self.setLastId(self.pConsulta.fetchone()[0])
            self.pConexao.commit()
        except pyodbc.Error as e:
            self.sSqlError = str(e)
            self.sErro = f'Ocorreu o seguinte erro na consulta: {self.sSqlError} <br> Query: {sSql}'
            self.insereErroSql(sSql)
            return self.getErro()

    def insereErroSql(self, sSql):
        try:
            with self.pConexao.cursor() as cursor:
                sSqlErroExecucao = f"INSERT INTO seg_erros_mysql (erro,ip,publicado) VALUES ('{self.escapeString(self.getErro())}','{ct.IP_SERVIDOR}',1)"
                cursor.execute(sSqlErroExecucao)
                self.pConexao.commit()
        except pyodbc.Error as e:
            self.sSqlError = str(e)
            self.sErro = f'Ocorreu o seguinte erro na inserção do erro na tabela seg_erros_mysql: {self.sSqlError} <br> Query: {sSql}'

    #def recordCount(self):
    #    return self.pConsulta.rowcount()

    def fetchObject(self):
        return self.pConsulta.fetchone()

    def close(self):
        self.pConexao.close()

    def getErroSql(self):
        return self.sSqlError

    def setConexao(self,sBanco):
        self.pConexao = Conexao(sServidor=sBanco)

    def getConexao(self):
        return self.pConexao

    def getConsulta(self):
        return self.pConsulta

    def getErro(self):
        return self.sErro

    def escapeString(self, sAtributo):
        if str(sAtributo) != None:
            return str(sAtributo).replace("'", "''")
        return False

    def unescapeString(self, sEscapedString):
        if str(sEscapedString) != None:
            sEscapedString = str(sEscapedString).replace("'", "")
            sEscapedString = str(sEscapedString).replace("\"", "")
            return sEscapedString
        return False

    def getLastId(self):
        return self.nLastId

