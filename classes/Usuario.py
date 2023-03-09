from classes.UsuarioParent import UsuarioParent

class Usuario(UsuarioParent):
    def __init__(self, nId, nIdGrupoUsuario, sNmUsuario, sLogin, sSenha, sEmail, bLogado, dDtCadastro, bPublicado, bAtivo):
        self.setId(nId)
        self.setIdGrupoUsuario(nIdGrupoUsuario)
        self.setNmUsuario(sNmUsuario)
        self.setLogin(sLogin)
        self.setSenha(sSenha)
        self.setEmail(sEmail)
        self.setLogado(bLogado)
        self.setDtCadastro(dDtCadastro)
        self.setPublicado(bPublicado)
        self.setAtivo(bAtivo)

    def to_dict(self):
        return {
            "nId": self.nId,
            "nIdGrupoUsuario": self.nIdGrupoUsuario,
            "sNmUsuario": self.sNmUsuario,
            "sLogin": self.sLogin,
            "sSenha": "",
            "sEmail": self.sEmail,
            "bLogado": self.bLogado,
            "dDtCadastro": str(self.dDtCadastro),
            "bPublicado": self.bPublicado,
            "bAtivo": self.bAtivo
        }