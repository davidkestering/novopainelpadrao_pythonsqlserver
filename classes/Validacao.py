class Validacao():
    def __init__(self):
        #print("Validando campos")
        print("")

    def verificaObjetoVazio(self,oObjeto, vCampos):
        sMsg = ""
        sMsgFinal = ""
        vObjeto = vars(oObjeto)
        vCampos = vCampos.split(",")
        for atributo, valor in vObjeto.items():
            if atributo not in vCampos:
                if self.verificaCampoVazio(valor):
                    sMsg += f"{atributo},\n"
        sMsg = sMsg[:-2]
        if sMsg:
            sMsgFinal = f"O(s) seguinte(s) campo(s) precisa(m) ser preenchido(s):\n{sMsg}"
        return sMsgFinal

    def verificaCampoVazio(self,sCampo):
        if sCampo == "" or sCampo == None:
            return True
        return False
