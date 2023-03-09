from classes.UsuarioBDParent import UsuarioBDParent

class UsuarioBD(UsuarioBDParent):
    def __init__(self, sBanco):
        self.pConexao = UsuarioBDParent(sBanco=sBanco)

    def alteraSenha(self, oUsuario, sSenha):
        oConexao = self.getConexao()
        sSql = f"""DECLARE @senha NVARCHAR(MAX) = '{sSenha}';
                    DECLARE @senhaCriptografada VARBINARY(MAX);
                    SET @senhaCriptografada = HASHBYTES('SHA2_256', @senha);
                    UPDATE SEG_USUARIO SET senha = @senhaCriptografada WHERE id = {oUsuario.getId()};"""
        oConexao.executeInsert(sSql)
        return oConexao.getErro() is None