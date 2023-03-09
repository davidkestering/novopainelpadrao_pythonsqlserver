from classes.Transacao import Transacao
from classes.Conexao import Conexao
from datetime import datetime

class TransacaoBDParent(Conexao):
    def __init__(self, sBanco):
        self.pConexao = Conexao(sServidor=sBanco)

    def getConexao(self):
        return Conexao.getConexao(self.pConexao)

    def recupera(self, nId):
        oConexao = self.getConexao()
        sSql = f"select * from seg_transacao where id = '{nId}'"
        oConexao.execute(sSql)
        oReg = oConexao.fetchObject()
        if oReg:
            oTransacao = Transacao(oReg.id,oReg.id_tipo_transacao,oReg.id_usuario,oConexao.unescapeString(oReg.objeto),oConexao.unescapeString(oReg.campo),oConexao.unescapeString(oReg.valor_antigo),oConexao.unescapeString(oReg.valor_novo),oConexao.unescapeString(oReg.ip),oReg.dt_cadastro,oReg.publicado,oReg.ativo)
            vData = str(oTransacao.getDtCadastro()).split(".")
            data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
            dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
            oTransacao.setDtCadastro(dDataCadastro)
            return oTransacao
        return False

    def presente(self, nId):
        oConexao = self.getConexao()
        sSql = f"select id from seg_transacao where id = '{nId}'"
        oConexao.execute(sSql)
        oReg = oConexao.fetchObject()
        if oReg:
            return len(oReg) > 0
        return 0

    def insere(self, oTransacao):
        oConexao = self.getConexao()
        vData = str(oTransacao.getDtCadastro()).split(".")
        data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
        dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
        oTransacao.setDtCadastro(dDataCadastro)
        sSql = f"insert into seg_transacao (id_tipo_transacao,id_usuario,objeto,campo,valor_antigo,valor_novo,ip,dt_cadastro,publicado,ativo) values ('{oTransacao.getIdTipoTransacao()}','{oTransacao.getIdUsuario()}','{oConexao.escapeString(oTransacao.getObjeto())}','{oConexao.escapeString(oTransacao.getCampo())}','{oConexao.escapeString(oTransacao.getValorAntigo())}','{oConexao.escapeString(oTransacao.getValorNovo())}','{oConexao.escapeString(oTransacao.getIp())}','{oTransacao.getDtCadastro()}','{oTransacao.getPublicado()}','{oTransacao.getAtivo()}')"
        oConexao.execute(sSql)
        nId = oConexao.getLastId()
        if nId:
            return nId
        return oConexao.getConsulta()

    def altera(self, oTransacao):
        oConexao = self.getConexao()
        vData = str(oTransacao.getDtCadastro()).split(".")
        data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
        dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
        oTransacao.setDtCadastro(dDataCadastro)
        sSql = f"update seg_transacao set id_tipo_transacao = '{oTransacao.getIdTipoTransacao()}', id_usuario = '{oTransacao.getIdUsuario()}', objeto = '{oConexao.escapeString(oTransacao.getObjeto())}', campo = '{oConexao.escapeString(oTransacao.getCampo())}', valor_antigo = '{oConexao.escapeString(oTransacao.getValorAntigo())}', valor_novo = '{oConexao.escapeString(oTransacao.getValorNovo())}', ip = '{oConexao.escapeString(oTransacao.getIp())}', dt_cadastro = '{oTransacao.getDtCadastro()}', publicado = '{oTransacao.getPublicado()}', ativo = '{oTransacao.getAtivo()}' where id = '{oTransacao.getId()}'"
        oConexao.execute(sSql)
        return oConexao.getConsulta()

    def recuperaTodos(self, vWhere, sOrder):
        oConexao = self.getConexao()
        if isinstance(vWhere, list) and len(vWhere) > 0:
            sSql2 = ""
            for sWhere in vWhere:
                if sWhere != "":
                    sSql2 += sWhere + " AND "
            if sSql2 != "":
                sSql = "SELECT * FROM seg_transacao WHERE "
                sSql = (sSql + sSql2)[:-5]
            else:
                sSql = "SELECT * FROM seg_transacao "
        else:
            sSql = "SELECT * FROM seg_transacao "

        if sOrder:
            sSql += " ORDER BY " + sOrder

        oConexao.execute(sSql)
        voObjeto = []
        while True:
            oReg = oConexao.fetchObject()
            if oReg != None:
                oTransacao = Transacao(oReg.id,oReg.id_tipo_transacao,oReg.id_usuario,oConexao.unescapeString(oReg.objeto),oConexao.unescapeString(oReg.campo),oConexao.unescapeString(oReg.valor_antigo),oConexao.unescapeString(oReg.valor_novo),oConexao.unescapeString(oReg.ip),oReg.dt_cadastro,oReg.publicado,oReg.ativo)
                vData = str(oTransacao.getDtCadastro()).split(".")
                data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
                dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
                oTransacao.setDtCadastro(dDataCadastro)
                voObjeto.append(oTransacao)
                del oTransacao
            else:
                break
        return voObjeto

    def exclui(self, nId):
        oConexao = self.getConexao()
        sSql = f"delete from seg_transacao where id = '{nId}'"
        oConexao.execute(sSql)
        return oConexao.getConsulta()

    def desativa(self, nId):
        oConexao = self.getConexao()
        sSql = f"update seg_transacao set ativo = '0' where id = '{nId}'"
        oConexao.execute(sSql)
        return oConexao.getConsulta()