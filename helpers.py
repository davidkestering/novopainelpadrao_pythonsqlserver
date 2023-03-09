from flask import request, session
from markupsafe import Markup
import constantes as ct

def retornaIpServidor():
    return ct.IP_SERVIDOR

def retornaIpUsuario():
    return request.remote_addr or None

def retornaIdUsuario():
    return session['oLoginAdm']['nId']

def carregaMensagens():
    # CONTROLE DE MENSAGEM
    sClasseMensagem = "esconder"
    sTipoAlertaMensagem = ""
    sTipoAlertaLogo = ""
    sMensagem = ""
    if session.get('sMsgPermissao') and session.get('sTipoAlertaMensagem') and session.get('sTipoAlertaLogo'):
        sClasseMensagem = "mostrar"
        sMensagem = session['sMsgPermissao']
        sTipoAlertaMensagem = session['sTipoAlertaMensagem']
        sTipoAlertaLogo = session['sTipoAlertaLogo']

    vMsg = {"CLASSEMENSAGEM": sClasseMensagem, "MENSAGEM": Markup(sMensagem), "TIPOALERTAMENSAGEM": sTipoAlertaMensagem,
            "TIPOALERTALOGO": sTipoAlertaLogo}

    return vMsg