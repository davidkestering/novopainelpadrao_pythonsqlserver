from classes.TransacaoParent import TransacaoParent

class Transacao(TransacaoParent):
    def __init__(self, nId,nIdTipoTransacao,nIdUsuario,sObjeto,sCampo,sValorAntigo,sValorNovo,sIp,dDtCadastro,bPublicado,bAtivo):
        self.setId(nId)
        self.setIdTipoTransacao(nIdTipoTransacao)
        self.setIdUsuario(nIdUsuario)
        self.setObjeto(sObjeto)
        self.setCampo(sCampo)
        self.setValorAntigo(sValorAntigo)
        self.setValorNovo(sValorNovo)
        self.setIp(sIp)
        self.setDtCadastro(dDtCadastro)
        self.setPublicado(bPublicado)
        self.setAtivo(bAtivo)
        