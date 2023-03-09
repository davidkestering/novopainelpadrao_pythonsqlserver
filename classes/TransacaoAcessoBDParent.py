from classes.TransacaoAcesso import TransacaoAcesso
from classes.Conexao import Conexao
from datetime import datetime

class TransacaoAcessoBDParent(Conexao):
    def __init__(self, sBanco):
        self.pConexao = Conexao(sServidor=sBanco)

    def getConexao(self):
        return Conexao.getConexao(self.pConexao)

    def recupera(self, nId):
        oConexao = self.getConexao()
        sSql = f"select * from seg_transacao_acesso where id = '{nId}'"
        oConexao.execute(sSql)
        oReg = oConexao.fetchObject()
        if oReg:
            oTransacaoAcesso = TransacaoAcesso(oReg.id,oReg.id_tipo_transacao,oReg.id_usuario,oConexao.unescapeString(oReg.objeto),oConexao.unescapeString(oReg.campo),oConexao.unescapeString(oReg.valor_antigo),oConexao.unescapeString(oReg.valor_novo),oConexao.unescapeString(oReg.ip),oReg.dt_cadastro,oReg.publicado,oReg.ativo)
            vData = str(oTransacaoAcesso.getDtCadastro()).split(".")
            data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
            dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
            oTransacaoAcesso.setDtCadastro(dDataCadastro)
            return oTransacaoAcesso
        return False

    def presente(self, nId):
        oConexao = self.getConexao()
        sSql = f"select id from seg_transacao_acesso where id = '{nId}'"
        oConexao.execute(sSql)
        oReg = oConexao.fetchObject()
        if oReg:
            return len(oReg) > 0
        return 0

    def insere(self, oTransacaoAcesso):
        oConexao = self.getConexao()
        vData = str(oTransacaoAcesso.getDtCadastro()).split(".")
        data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
        dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
        oTransacaoAcesso.setDtCadastro(dDataCadastro)
        sSql = f"insert into seg_transacao_acesso (id_tipo_transacao,id_usuario,objeto,campo,valor_antigo,valor_novo,ip,dt_cadastro,publicado,ativo) values ('{oTransacaoAcesso.getIdTipoTransacao()}','{oTransacaoAcesso.getIdUsuario()}','{oConexao.escapeString(oTransacaoAcesso.getObjeto())}','{oConexao.escapeString(oTransacaoAcesso.getCampo())}','{oConexao.escapeString(oTransacaoAcesso.getValorAntigo())}','{oConexao.escapeString(oTransacaoAcesso.getValorNovo())}','{oConexao.escapeString(oTransacaoAcesso.getIp())}','{oTransacaoAcesso.getDtCadastro()}','{oTransacaoAcesso.getPublicado()}','{oTransacaoAcesso.getAtivo()}')"
        oConexao.execute(sSql)
        nId = oConexao.getLastId()
        if nId:
            return nId
        return oConexao.getConsulta()

    def altera(self, oTransacaoAcesso):
        oConexao = self.getConexao()
        vData = str(oTransacaoAcesso.getDtCadastro()).split(".")
        data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
        dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
        oTransacaoAcesso.setDtCadastro(dDataCadastro)
        sSql = f"update seg_transacao_acesso set id_tipo_transacao = '{oTransacaoAcesso.getIdTipoTransacao()}', id_usuario = '{oTransacaoAcesso.getIdUsuario()}', objeto = '{oConexao.escapeString(oTransacaoAcesso.getObjeto())}', campo = '{oConexao.escapeString(oTransacaoAcesso.getCampo())}', valor_antigo = '{oConexao.escapeString(oTransacaoAcesso.getValorAntigo())}', valor_novo = '{oConexao.escapeString(oTransacaoAcesso.getValorNovo())}', ip = '{oConexao.escapeString(oTransacaoAcesso.getIp())}', dt_cadastro = '{oTransacaoAcesso.getDtCadastro()}', publicado = '{oTransacaoAcesso.getPublicado()}', ativo = '{oTransacaoAcesso.getAtivo()}' where id = '{oTransacaoAcesso.getId()}'"
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
                sSql = "SELECT * FROM seg_transacao_acesso WHERE "
                sSql = (sSql + sSql2)[:-5]
            else:
                sSql = "SELECT * FROM seg_transacao_acesso "
        else:
            sSql = "SELECT * FROM seg_transacao_acesso "

        if sOrder:
            sSql += " ORDER BY " + sOrder

        oConexao.execute(sSql)
        voObjeto = []
        while True:
            oReg = oConexao.fetchObject()
            if oReg != None:
                oTransacaoAcesso = TransacaoAcesso(oReg.id,oReg.id_tipo_transacao,oReg.id_usuario,oConexao.unescapeString(oReg.objeto),oConexao.unescapeString(oReg.campo),oConexao.unescapeString(oReg.valor_antigo),oConexao.unescapeString(oReg.valor_novo),oConexao.unescapeString(oReg.ip),oReg.dt_cadastro,oReg.publicado,oReg.ativo)
                vData = str(oTransacaoAcesso.getDtCadastro()).split(".")
                data = datetime.strptime(vData[0] + '.000000', '%Y-%m-%d %H:%M:%S.%f')
                dDataCadastro = data.strftime('%Y-%m-%d %H:%M:%S')
                oTransacaoAcesso.setDtCadastro(dDataCadastro)
                voObjeto.append(oTransacaoAcesso)
                del oTransacaoAcesso
            else:
                break
        return voObjeto

    def exclui(self, nId):
        oConexao = self.getConexao()
        sSql = f"delete from seg_transacao_acesso where id = '{nId}'"
        oConexao.execute(sSql)
        return oConexao.getConsulta()

    def desativa(self, nId):
        oConexao = self.getConexao()
        sSql = f"update seg_transacao_acesso set ativo = '0' where id = '{nId}'"
        oConexao.execute(sSql)
        return oConexao.getConsulta()