from classes.TipoTransacao import TipoTransacao
from classes.Conexao import Conexao
from datetime import datetime

class TipoTransacaoBDParent(Conexao):
    def __init__(self, sBanco):
        self.pConexao = Conexao(sServidor=sBanco)

    def getConexao(self):
        return Conexao.getConexao(self.pConexao)

    def recupera(self, nId):
        oConexao = self.getConexao()
        sSql = f"select * from seg_tipo_transacao where id = '{nId}'"
        oConexao.execute(sSql)
        oReg = oConexao.fetchObject()
        if oReg:
            oTipoTransacao = TipoTransacao(oReg.id,oReg.id_categoria_tipo_transacao,oConexao.unescapeString(oReg.transacao),oReg.dt_cadastro,oReg.publicado,oReg.ativo)
            vData = str(oTipoTransacao.getDtCadastro()).split(".")
            data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
            dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
            oTipoTransacao.setDtCadastro(dDataCadastro)
            return oTipoTransacao
        return False

    def presente(self, nId):
        oConexao = self.getConexao()
        sSql = f"select id from seg_tipo_transacao where id = '{nId}'"
        oConexao.execute(sSql)
        oReg = oConexao.fetchObject()
        if oReg:
            return len(oReg) > 0
        return 0

    def insere(self, oTipoTransacao):
        oConexao = self.getConexao()
        vData = str(oTipoTransacao.getDtCadastro()).split(".")
        data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
        dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
        oTipoTransacao.setDtCadastro(dDataCadastro)
        sSql = f"insert into seg_tipo_transacao (id_categoria_tipo_transacao,transacao,dt_cadastro,publicado,ativo) values ('{oTipoTransacao.getIdCategoriaTipoTransacao()}','{oConexao.escapeString(oTipoTransacao.getTransacao())}','{oTipoTransacao.getDtCadastro()}','{oTipoTransacao.getPublicado()}','{oTipoTransacao.getAtivo()}')"
        oConexao.execute(sSql)
        nId = oConexao.getLastId()
        if nId:
            return nId
        return oConexao.getConsulta()

    def altera(self, oTipoTransacao):
        oConexao = self.getConexao()
        vData = str(oTipoTransacao.getDtCadastro()).split(".")
        data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
        dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
        oTipoTransacao.setDtCadastro(dDataCadastro)
        sSql = f"update seg_tipo_transacao set id_categoria_tipo_transacao = '{oTipoTransacao.getIdCategoriaTipoTransacao()}', transacao = '{oConexao.escapeString(oTipoTransacao.getTransacao())}', dt_cadastro = '{oTipoTransacao.getDtCadastro()}', publicado = '{oTipoTransacao.getPublicado()}', ativo = '{oTipoTransacao.getAtivo()}' where id = '{oTipoTransacao.getId()}'"
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
                sSql = "SELECT * FROM seg_tipo_transacao WHERE "
                sSql = (sSql + sSql2)[:-5]
            else:
                sSql = "SELECT * FROM seg_tipo_transacao "
        else:
            sSql = "SELECT * FROM seg_tipo_transacao "

        if sOrder:
            sSql += " ORDER BY " + sOrder

        oConexao.execute(sSql)
        voObjeto = []
        while True:
            oReg = oConexao.fetchObject()
            if oReg != None:
                oTipoTransacao = TipoTransacao(oReg.id,oReg.id_categoria_tipo_transacao,oConexao.unescapeString(oReg.transacao),oReg.dt_cadastro,oReg.publicado,oReg.ativo)
                vData = str(oTipoTransacao.getDtCadastro()).split(".")
                data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
                dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
                oTipoTransacao.setDtCadastro(dDataCadastro)
                voObjeto.append(oTipoTransacao)
                del oTipoTransacao
            else:
                break
        return voObjeto

    def exclui(self, nId):
        oConexao = self.getConexao()
        sSql = f"delete from seg_tipo_transacao where id = '{nId}'"
        oConexao.execute(sSql)
        return oConexao.getConsulta()

    def desativa(self, nId):
        oConexao = self.getConexao()
        sSql = f"update seg_tipo_transacao set ativo = '0' where id = '{nId}'"
        oConexao.execute(sSql)
        return oConexao.getConsulta()