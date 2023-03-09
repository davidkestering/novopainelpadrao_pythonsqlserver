from imports_views import *

@app.route('/usuario/alterar_senha', methods=['GET','POST'])
def alterar_dados():
    if 'oLoginAdm' not in session:
        session['sMsgPermissao'] = ct.ACESSO_NEGADO
        session['sTipoAlertaMensagem'] = "danger"
        session['sTipoAlertaLogo'] = "fa-ban"
        return redirect(url_for('login',bErro=1))

    from classes.Login import Login
    oLogin = Login()
    oUsuario = oFachadaSeguranca.recuperaUsuario(session['oLoginAdm']['nId'], sBanco)
    if not oUsuario or oUsuario == None:
        session['sMsgPermissao'] = "Usuário não encontrado no sistema!"
        session['sTipoAlertaMensagem'] = "danger"
        session['sTipoAlertaLogo'] = "fa-ban"
        return redirect(url_for('index', bErro=1))
    else:
        oLogin.setUsuario(oUsuario)
        oLogin.recuperaPermissoes(oUsuario, sBanco)

        if request.method == 'POST':
            sOP = request.form['sOP']
            fIdUsuario = request.form['fIdUsuario']
            sSenhaEnviada = request.form['fSenha']
            sSenhaEnviadaConfirmacao = request.form['fSenhaConfirmacao']
            nIdTipoTransacaoSessao = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Usuario",sOP, sBanco)
            bPermissao = oLogin.verificaPermissao("Usuario",sOP,sBanco)

            if not bPermissao:
                nIdTipoTransacaoAcesso = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Usuario",sOP, sBanco)
                sObjetoAcesso = ct.ACESSO_NEGADO_TRANSACAO
                oTransacaoAcesso = oFachadaSeguranca.inicializaTransacaoAcesso(nIdTipoTransacaoAcesso, session['oLoginAdm']['nId'], fIdUsuario, sObjetoAcesso, "", "", "", IP_USUARIO, ct.DATAHORA, 1, 1)
                oFachadaSeguranca.insereTransacaoAcesso(oTransacaoAcesso, sBanco)
                session['sMsgPermissao'] = ct.ACESSO_NEGADO
                session['sTipoAlertaMensagem'] = "danger"
                session['sTipoAlertaLogo'] = "fa-ban"
                return redirect(url_for('index',bErro=1))

            # NAO PERMITE QUE O USUARIO DA SESSAO ALTERE A SENHA DE OUTRO USUARIO CASO ALTERE O HIDDEN DO IDUSUARIO
            if (str(session['oLoginAdm']['nId']) != str(fIdUsuario)):
                nIdTipoTransacaoAcesso = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Usuario",sOP, sBanco)
                sObjetoAcesso = f"VERIFICAR ERRO: Tentativa de alteracao de senha, mas o ID_USUARIO da sessao eh diferente do ID_USUARIO do POST. ID do Usuario da Sessao {session['oLoginAdm']['nId']}, POST: {fIdUsuario}"
                oTransacaoAcesso = oFachadaSeguranca.inicializaTransacaoAcesso(nIdTipoTransacaoAcesso,session['oLoginAdm']['nId'], fIdUsuario,sObjetoAcesso, "", "", "", IP_USUARIO,ct.DATAHORA, 1, 1)
                oFachadaSeguranca.insereTransacaoAcesso(oTransacaoAcesso, sBanco)
                session['sMsgPermissao'] = ct.ACESSO_NEGADO
                session['sTipoAlertaMensagem'] = "danger"
                session['sTipoAlertaLogo'] = "fa-ban"
                return redirect(url_for('index', bErro=2))

            sMsg = None
            if str(sSenhaEnviada) and str(sSenhaEnviadaConfirmacao) and (str(sSenhaEnviada) != str(sSenhaEnviadaConfirmacao)):
                sMsg = "A senha precisa ser igual a confirmação. Tente novamente!"
                if sMsg != None:
                    session['sMsgPermissao'] = sMsg
                    session['sTipoAlertaMensagem'] = "danger"
                    session['sTipoAlertaLogo'] = "fa-ban"
                    return redirect(url_for('alterar_dados', bErro=3))

            from classes.Validacao import Validacao
            oValidacao = Validacao()
            sAtributosQuePodemEstarVazios = "nId,bLogado,sEmail,sSenha,bPublicado,bAtivo"
            sMsg = oValidacao.verificaObjetoVazio(oUsuario,sAtributosQuePodemEstarVazios)
            if sMsg.strip() != "" and sMsg != None:
                session['sMsgPermissao'] = sMsg
                session['sTipoAlertaMensagem'] = "danger"
                session['sTipoAlertaLogo'] = "fa-ban"
                return redirect(url_for('alterar_dados', bErro=4))

            oUsuarioAuxiliar = oFachadaSeguranca.recuperaUsuario(session['oLoginAdm']['nId'], sBanco)

            if(sSenhaEnviada.strip() == "" or sSenhaEnviada == None):
                oUsuario.setSenha(oUsuarioAuxiliar.getSenha())
                session['sMsgPermissao'] = "Não houve alteração de senha!"
                session['sTipoAlertaMensagem'] = "success"
                session['sTipoAlertaLogo'] = "fa-check"
                return redirect(url_for('alterar_dados'))

            # TRANSACAO
            vObjetoModificado = {}
            voUsuario = oUsuario.__dict__
            voUsuarioAuxiliar = oUsuarioAuxiliar.__dict__
            for key in voUsuario:
                if voUsuario[key] != voUsuarioAuxiliar[key]:
                    vObjetoModificado[key] = voUsuario[key]
            vObjetoAntigo = voUsuarioAuxiliar
            voTransacao = []
            for sCampo, sValor in vObjetoModificado.items():
                sValorAntigo = vObjetoAntigo[sCampo]
                oTransacao = oFachadaSeguranca.inicializaTransacao("",nIdTipoTransacaoSessao,helpers.retornaIdUsuario(),fIdUsuario,sCampo,sValorAntigo,sValor,helpers.retornaIpUsuario(),ct.DATAHORA,1,1)
                if sValor is not None and sValor != "":
                    voTransacao.append(oTransacao)

            if not oFachadaSeguranca.alteraSenhaUsuario(oUsuario,sSenhaEnviada,voTransacao,sBanco):
                sObjetoAcesso = ct.ACESSO_TENTATIVA
                voTransacaoAcesso = []
                for sCampo, sValor in vObjetoModificado.items():
                    sValorAntigo = vObjetoAntigo[sCampo]
                    oTransacaoAcesso = oFachadaSeguranca.inicializaTransacaoAcesso("", nIdTipoTransacaoSessao, helpers.retornaIdUsuario(),fIdUsuario, sObjetoAcesso, sValorAntigo, sValor,helpers.retornaIpUsuario(), ct.DATAHORA, 1, 1)
                    if sValor is not None and sValor != "":
                        voTransacaoAcesso.append(oTransacaoAcesso)

                for oTransacaoAcesso in voTransacaoAcesso:
                    if oTransacaoAcesso != None and isinstance(oTransacaoAcesso,object):
                        oFachadaSeguranca.insereTransacaoAcesso(oTransacaoAcesso,sBanco)

                session['sMsgPermissao'] = "Não foi possível alterar as informações!"
                session['sTipoAlertaMensagem'] = "danger"
                session['sTipoAlertaLogo'] = "fa-ban"
                return redirect(url_for('alterar_dados', bErro=5))
            else:
                session['sMsgPermissao'] = "Informações alteradas com sucesso!"
                session['sTipoAlertaMensagem'] = "success"
                session['sTipoAlertaLogo'] = "fa-check"
                return redirect(url_for('alterar_dados'))
        else:
            vMsg = helpers.carregaMensagens()

            bVisualizaMenuAdministrativo = False
            bVisualizarMenuAlterarDados = False
            bVisualizarMenuUsuario = False
            bVisualizarMenuGrupoUsuario = False
            bVisualizarMenuTransacao = False
            bVisualizarMenuLogTransacao = False
            bVisualizarMenuLogAcesso = False
            bVisualizarMenuLogErrosSQL = False
            sNomeUsuarioLogado = ""
            nIdUsuario = ""
            sNomeUsuario = ""
            sEmailUsuario = ""
            sGrupoUsuario = ""
            sLoginUsuario = ""
            if session.get('oLoginAdm'):
                oLogin = Login()
                sNomeUsuarioLogado = session['oLoginAdm']['sNmUsuario']
                oUsuario = oFachadaSeguranca.recuperaUsuario(session['oLoginAdm']['nId'], sBanco)
                if (oUsuario != None and isinstance(oUsuario, object)):
                    nIdUsuario = oUsuario.getId()
                    sNomeUsuario = oUsuario.getNmUsuario()
                    sEmailUsuario = oUsuario.getEmail()
                    oGrupoUsuario = oFachadaSeguranca.recuperaGrupoUsuario(oUsuario.getIdGrupoUsuario(),sBanco)
                    if (oGrupoUsuario != None and isinstance(oGrupoUsuario,object)):
                        sGrupoUsuario = oGrupoUsuario.getNmGrupoUsuario()
                    sLoginUsuario = oUsuario.getLogin()

                    oLogin.setUsuario(oUsuario)
                    oLogin.recuperaPermissoes(oUsuario, sBanco)

                    # ALTERAR SENHA
                    bPermissaoAlterarSenha = oLogin.verificaPermissao("Usuario", "AlterarSenha", sBanco)
                    # print(bPermissaoAlterarSenha)

                    # VERIFICA AS PERMISSÕES
                    bPermissaoAlterarDados = oLogin.verificaPermissao("Permissao", "Alterar", sBanco)
                    bPermissaoVisualizarUsuario = oLogin.verificaPermissao("Usuario", "Visualizar", sBanco)
                    bPermissaoVisualizarGrupoUsuario = oLogin.verificaPermissao("Grupos", "Visualizar", sBanco)
                    bPermissaoVisualizarTransacao = oLogin.verificaPermissao("Transacao", "Visualizar", sBanco)
                    bPermissaoVerLogTransacao = oLogin.verificaPermissao("Transacao", "VerLog", sBanco)
                    bPermissaoVerErroTransacao = oLogin.verificaPermissao("Transacao", "VerErro", sBanco)
                    bPermissaoVerErrosSQLTransacao = oLogin.verificaPermissao("Transacao", "VerErrosMySQL", sBanco)


                    if (bPermissaoVisualizarUsuario or bPermissaoAlterarSenha or bPermissaoAlterarDados or bPermissaoVisualizarGrupoUsuario or bPermissaoVisualizarTransacao or bPermissaoVerLogTransacao or bPermissaoVerErroTransacao or bPermissaoVerErrosSQLTransacao):
                        bVisualizaMenuAdministrativo = True

                        if bPermissaoAlterarDados and bPermissaoAlterarSenha:
                            bVisualizarMenuAlterarDados = True

                        if bPermissaoVisualizarUsuario:
                            bVisualizarMenuUsuario = True

                        if bPermissaoVisualizarGrupoUsuario:
                            bVisualizarMenuGrupoUsuario = True

                        if bPermissaoVisualizarTransacao:
                            bVisualizarMenuTransacao = True

                        if bPermissaoVerLogTransacao:
                            bVisualizarMenuLogTransacao = True

                        if bPermissaoVerErroTransacao:
                            bVisualizarMenuLogAcesso = True

                        if bPermissaoVerErrosSQLTransacao:
                            bVisualizarMenuLogErrosSQL = True

            vPermissoes = {"BLOCK_MENU_ADMINISTRATIVO": bVisualizaMenuAdministrativo,
                           "BLOCK_MENU_ALTERA_SENHA": bVisualizarMenuAlterarDados,
                           "BLOCK_MENU_USUARIOS": bVisualizarMenuUsuario,
                           "BLOCK_MENU_GRUPO_USUARIOS": bVisualizarMenuGrupoUsuario,
                           "BLOCK_MENU_TRANSACOES": bVisualizarMenuTransacao, "BLOCK_MENU_LOG": bVisualizarMenuLogTransacao,
                           "BLOCK_MENU_ERROS_ACESSO": bVisualizarMenuLogAcesso,
                           "BLOCK_MENU_ERROS_SQL": bVisualizarMenuLogErrosSQL}

            vTextos = {"PAGINAATUAL": "Alterar Senha", "USUARIOLOGADO": sNomeUsuarioLogado,"MENUADMATIVO":"active","SUBMENUALTERASENHAATIVO":"active"}

            vDadosPagina = {"ACAO":"AlterarSenha","IDUSUARIO":nIdUsuario,"NOME":sNomeUsuario,"EMAIL":sEmailUsuario,"GRUPOUSUARIO":sGrupoUsuario,"LOGIN":sLoginUsuario}

        # RESET DAS MENSAGENS
        session['sMsgPermissao'] = ""
        session['sTipoAlertaMensagem'] = ""
        session['sTipoAlertaLogo'] = ""
        return render_template('painel/administrativo/alterar_senha/index.html', ANORODAPE=2023, vMsg=vMsg, vTextos=vTextos, vPermissoes=vPermissoes, vDadosPagina=vDadosPagina)