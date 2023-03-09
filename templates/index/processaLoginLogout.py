from imports_views import *

@app.route('/login/processa', methods=['POST'])
def processaLogin():
    IP_USUARIO = request.remote_addr
    # Itera sobre a propriedade args -GET
    # for key, value in request.args.items():
    #     print(f"{key}: {value}")

    #Itera sobre a propriedade form - POST
    #for key, value in request.form.items():
    #    print(f"{key}: {value}")
    sOP = request.form['sOP']
    match sOP:
        case "Logar":
            sLogin = request.form['fLogin']
            sSenha = request.form['fSenha']

            if sOP == "Logar" and (not sLogin or not sSenha):
                session['sMsgPermissao'] = "Informe o login e a senha para ter acesso ao Painel Administrativo!"
                return "0_" + session['sMsgPermissao']
            else:
                from classes.Login import Login
                from classes.Usuario import Usuario
                oLogin = Login()
                sRetorno = oLogin.logarUsuarioPainel(sLogin, sSenha, ct.BANCO)

                #print(sRetorno)
                match sRetorno:
                    case "0":
                        session['sMsgPermissao'] = "Problemas na identificação. Verifique se os seus dados estão corretos."
                        session['sTipoAlertaMensagem'] = "danger"
                        session['sTipoAlertaLogo'] = "fa-ban"
                        return "2_"+session['sMsgPermissao']
                    case "1":
                        session['oLoginAdm'] = oLogin.oUsuario.to_dict()
                        session['sMsgPermissao'] = ""
                        session['sTipoAlertaMensagem'] = "success"
                        session['sTipoAlertaLogo'] = "fa-check"
                        session['dUltimoAcesso'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        return "1_"
                    case "2":
                        #print(oLogin.oUsuario.to_dict())
                        # print(json.dumps(oLogin.oUsuario))
                        # usuario_json = json.dumps(oLogin.oUsuario)
                        # usuario_objeto = json.loads(usuario_json, object_hook=lambda d: Usuario(**d))
                        # print(usuario_objeto)
                        #exit()

                        session['oLoginUsuarioJaLogado'] = oLogin.oUsuario.to_dict()
                        nIdUsuario = session['oLoginUsuarioJaLogado']['nId']
                        session['sMsgPermissao'] = f'Usuário já logado no sistema!<br /> <a href="Javascript: void(0)" onclick="liberaUsuario({nIdUsuario})">Clique aqui para liberar o acesso!</a>'
                        session['sTipoAlertaMensagem'] = "danger"
                        session['sTipoAlertaLogo'] = "fa-ban"
                        return "2_" + session['sMsgPermissao']
        case "Logoff":
            from templates.includes import libera_usuario
            libera_usuario.libera_usuario()
            session['oLoginUsuarioJaLogado'] = ""
            session.pop('oLoginUsuarioJaLogado', None)
            session['oLoginAdm'] = ""
            session.pop('oLoginAdm', None)
            session['oLoginPermissao'] = ""
            session.pop('oLoginPermissao', None)
            # RESET DAS MENSAGENS
            session['sMsgPermissao'] = ""
            session['sTipoAlertaMensagem'] = ""
            session['sTipoAlertaLogo'] = ""
            session.clear()
            return "1"