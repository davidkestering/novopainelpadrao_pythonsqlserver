import helpers
from classes.FachadaSegurancaBD import FachadaSegurancaBD
from classes.Conexao import Conexao
import sys
sys.path.append('../')
import constantes as ct
from helpers import *

class Login():
    def __init__(self):
        self.oUsuario = None
        self.vPermissao = None

    def setUsuario(self, oUsuario):
        self.oUsuario = oUsuario

    def getUsuario(self):
        return self.oUsuario

    def setvPermissao(self, vPermissao):
        self.vPermissao = vPermissao

    def getvPermissao(self):
        return self.vPermissao

    def getIdUsuario(self):
        return self.oUsuario.getId()

    def criptografaSenhaDentrodoSQLSERVER(self,sSenha,sBanco):
        Conexao.setConexao(self,sBanco=sBanco)
        oConexao = Conexao.getConexao(self)
        sSql = f"""DECLARE @senha NVARCHAR(MAX) = '{sSenha}';
                DECLARE @senhaCriptografada VARBINARY(MAX);
                SET @senhaCriptografada = HASHBYTES('SHA2_256', @senha);
                SELECT @senhaCriptografada;"""
        oConexao.execute(sSql)
        sSenhaCriptografadaNoSQLSERVER = oConexao.fetchObject()[0]
        #print(sSenhaCriptografadaNoSQLSERVER)
        return sSenhaCriptografadaNoSQLSERVER

    def logarUsuarioPainel(self, sLogin, sSenha, sBanco):
        oFachadaSeguranca = FachadaSegurancaBD(sBanco)
        vWhereUsuario = ["login = '{}'".format(sLogin), "publicado = 1", "ativo = 1"]
        voUsuario = oFachadaSeguranca.recuperaTodosUsuario(sBanco, vWhereUsuario)
        #print(voUsuario)

        if voUsuario != None and len(voUsuario) == 1:
            oUsuario = voUsuario[0]
            if(oUsuario != None and isinstance(oUsuario,object)):
                if oUsuario.getSenha() == self.criptografaSenhaDentrodoSQLSERVER(sSenha,ct.BANCO):
                    if oUsuario.getLogado() == 1:
                        nIdTipoTransacaoAcesso = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Acesso","Login",sBanco)
                        sObjetoAcesso = f"VERIFICAR ERRO 1: Tentativa de Login falhou. USUARIO LOGADO NO SISTEMA. Login do usuário: {sLogin} Senha: {sSenha}"
                        oTransacaoAcesso = oFachadaSeguranca.inicializaTransacaoAcesso("",nIdTipoTransacaoAcesso,oUsuario.getId(), sObjetoAcesso, "", "", "",helpers.retornaIpUsuario(), ct.DATAHORA, 1, 1)
                        oFachadaSeguranca.insereTransacaoAcesso(oTransacaoAcesso, sBanco)
                        self.setUsuario(oUsuario)
                        return "2"
                    else:
                        # TRATAMENTO PARA USUARIO NAO LOGADO
                        oUsuario.setLogado("1")
                        if oFachadaSeguranca.alteraUsuario(oUsuario, None, sBanco):
                            nIdTipoTransacaoAcesso = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Acesso", "Login", sBanco)
                            sObjetoAcesso = f"Login efetuado com sucesso. Login do usuário: {sLogin}"
                            oTransacaoAcesso = oFachadaSeguranca.inicializaTransacaoAcesso("",nIdTipoTransacaoAcesso,oUsuario.getId(), sObjetoAcesso, "", "","",helpers.retornaIpUsuario(), ct.DATAHORA, 1, 1)
                            oFachadaSeguranca.insereTransacaoAcesso(oTransacaoAcesso, sBanco)
                            #print(oUsuario.__dict__)
                            self.setUsuario(oUsuario)
                            # vWherePermissaoGrupoUsuario = ["id_grupo_usuario = " + str(oUsuario.getIdGrupoUsuario()),"publicado = 1", "ativo = 1"]
                            # voPermissao = oFachadaSeguranca.recuperaTodosPermissao(sBanco, vWherePermissaoGrupoUsuario)
                            # vPermissao = []
                            # if(voPermissao != None and len(voPermissao) > 0):
                            #     for oPermissao in voPermissao:
                            #         vPermissao.append(oPermissao.__dict__)
                            #     #print(vPermissao)
                            #     self.setvPermissao(vPermissao)
                            return "1"
                else:
                    nIdTipoTransacaoAcesso = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Acesso","Login",sBanco)
                    sObjetoAcesso = f"VERIFICAR  ERRO 4: Tentativa de Login falhou. USUÁRIO EXISTE MAS HOUVE ERRO NA SENHA. Login do usuário: {sLogin} Senha: {sSenha}"
                    oTransacaoAcesso = oFachadaSeguranca.inicializaTransacaoAcesso("",nIdTipoTransacaoAcesso,oUsuario.getId(), sObjetoAcesso,"", "", "", helpers.retornaIpUsuario(), ct.DATAHORA, 1,1)
                    oFachadaSeguranca.insereTransacaoAcesso(oTransacaoAcesso, sBanco)
            else:
                nIdTipoTransacaoAcesso = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Acesso","Login",sBanco)
                sObjetoAcesso = f"VERIFICAR  ERRO 5: Tentativa de Login falhou. USUÁRIO NÃO ENCONTRADO. Login do usuário: {sLogin} Senha: {sSenha}"
                oTransacaoAcesso = oFachadaSeguranca.inicializaTransacaoAcesso("",nIdTipoTransacaoAcesso,app.retornaIdUsuario(), sObjetoAcesso,"", "", "", helpers.retornaIpUsuario(), ct.DATAHORA,1,1)
                oFachadaSeguranca.insereTransacaoAcesso(oTransacaoAcesso, sBanco)
        else:
            nIdTipoTransacaoAcesso = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Acesso","Login",sBanco)
            sObjetoAcesso = f"VERIFICAR  ERRO 6: Tentativa de Login falhou. USUÁRIO NÃO ENCONTRADO. Login do usuário: {sLogin} Senha: {sSenha}"
            oTransacaoAcesso = oFachadaSeguranca.inicializaTransacaoAcesso("",nIdTipoTransacaoAcesso,app.retornaIdUsuario(),sObjetoAcesso,"", "", "", helpers.retornaIpUsuario(), ct.DATAHORA,1,1)
            oFachadaSeguranca.insereTransacaoAcesso(oTransacaoAcesso, sBanco)

        return "0"

    def recuperaPermissoes(self,oUsuario,sBanco):
        oFachadaSeguranca = FachadaSegurancaBD(sBanco)
        vWherePermissaoGrupoUsuario = ["id_grupo_usuario = " + str(oUsuario.getIdGrupoUsuario()), "publicado = 1",
                                       "ativo = 1"]
        voPermissao = oFachadaSeguranca.recuperaTodosPermissao(sBanco, vWherePermissaoGrupoUsuario)
        if (voPermissao != None and len(voPermissao) > 0):
            self.setvPermissao(voPermissao)

    def verificaPermissao(self,sTipo, sOp, sBanco):
        oFachadaSeguranca = FachadaSegurancaBD(sBanco)
        nIdTipoTransacao = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria(sTipo, sOp, sBanco)
        voPermissao = self.getvPermissao()
        if len(voPermissao) > 0:
            for oPermissao in voPermissao:
                if oPermissao.getIdTipoTransacao() == nIdTipoTransacao:
                    return True
        return False

    def recuperaTipoTransacaoPorDescricaoCategoria(self,sTipo, sOp, sBanco):
        oFachadaSeguranca = FachadaSegurancaBD()
        return oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria(sTipo, sOp, sBanco)
