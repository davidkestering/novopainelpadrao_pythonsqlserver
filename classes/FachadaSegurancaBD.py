from classes.FachadaSegurancaBDParent import FachadaSegurancaBDParent

class FachadaSegurancaBD(FachadaSegurancaBDParent):
    def __init__(self, sBanco):
        self.pConexao = FachadaSegurancaBDParent(sBanco=sBanco)

    def alteraSenhaUsuario(self, oUsuario, sSenha, voTransacao, sBanco):
        oUsuarioBD = self.inicializaUsuarioBD(sBanco)
        bResultado = oUsuarioBD.alteraSenha(oUsuario,sSenha)
        if bResultado and voTransacao != None and hasattr(voTransacao,'__iter__'):
            for oTransacao in voTransacao:
                 if oTransacao != None and isinstance(oTransacao, object):
                     if not self.insereTransacao(oTransacao, sBanco):
                         return False
        if bResultado and voTransacao != None and not hasattr(voTransacao,'__iter__'):
            if not self.insereTransacao(voTransacao, sBanco):
                return False
        return bResultado

    def recuperaTipoTransacaoPorDescricaoCategoria(self, sDescricao, sTransacao, sBanco):
        oTipoTransacaoBD = self.inicializaTipoTransacaoBD(sBanco)
        oCategoriaTipoTransacaoBD = self.inicializaCategoriaTipoTransacaoBD(sBanco)
        oFachadaSeguranca = FachadaSegurancaBD(sBanco)
        vWhereCategoriaTipoTransacao = ["descricao = '{}'".format(sDescricao)]
        voCategoriaTipoTransacao = oFachadaSeguranca.recuperaTodosCategoriaTipoTransacao(sBanco,vWhereCategoriaTipoTransacao)
        if voCategoriaTipoTransacao != None and len(voCategoriaTipoTransacao) == 1:
            oCategoriaTipoTransacao = voCategoriaTipoTransacao[0]
            if isinstance(oCategoriaTipoTransacao, object):
                vWhereTipoTransacao = ["id_categoria_tipo_transacao = {}".format(oCategoriaTipoTransacao.getId()),
                                       "transacao = '{}'".format(sTransacao)]
                sOrderTipoTransacao = ""
                voTipoTransacao = oTipoTransacaoBD.recuperaTodos(vWhereTipoTransacao, sOrderTipoTransacao)
                if len(voTipoTransacao) == 1:
                    oTipoTransacao = voTipoTransacao[0]
                    return oTipoTransacao.getId()
        return False

    def desativaPermissaoPorGrupoUsuario(self,nIdGrupoUsuario, sBanco):
        oPermissaoBD = self.inicializaPermissaoBD(sBanco)
        bResultado = oPermissaoBD.desativaPorGrupoUsuario(nIdGrupoUsuario)
        return bResultado

    def desativaPermissaoPorTipoTransacao(self,nIdTipoTransacao, sBanco):
        oPermissaoBD = self.inicializaPermissaoBD(sBanco)
        bResultado = oPermissaoBD.desativaPorTipoTransacao(nIdTipoTransacao)
        return bResultado

    def verificaPermissao(self,nIdTipoTransacao, vPermissao, sBanco):
        oPermissaoBD = self.inicializaPermissaoBD(sBanco)
        bResultado = False
        if len(vPermissao) > 0:
            for oPermissao in vPermissao:
                if oPermissao.getIdTipoTransacao() == nIdTipoTransacao:
                    bResultado = True
            return bResultado
        return False

    def desativaTipoTransacaoPorCategoria(self,nIdCategoria,sBanco):
        oTipoTransacaoBD = self.inicializaTipoTransacaoBD(sBanco)
        bResultado = oTipoTransacaoBD.desativaPorCategoria(nIdCategoria)
        return bResultado