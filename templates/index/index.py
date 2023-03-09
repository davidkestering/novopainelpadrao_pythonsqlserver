from imports_views import *

@app.route('/', methods=['GET'])
def index():
    vMsg = helpers.carregaMensagens()

    sNomeUsuarioLogado = ""
    bVisualizaMenuAdministrativo = False
    bVisualizarMenuAlterarDados = False
    bVisualizarMenuUsuario = False
    bVisualizarMenuGrupoUsuario = False
    bVisualizarMenuTransacao = False
    bVisualizarMenuLogTransacao = False
    bVisualizarMenuLogAcesso = False
    bVisualizarMenuLogErrosSQL = False
    if session.get('oLoginAdm'):
        from classes.Login import Login
        oLogin = Login()
        sNomeUsuarioLogado = session['oLoginAdm']['sNmUsuario']
        oUsuario = oFachadaSeguranca.recuperaUsuario(session['oLoginAdm']['nId'],sBanco)
        if (oUsuario != None and isinstance(oUsuario,object)):
            oLogin.setUsuario(oUsuario)
            oLogin.recuperaPermissoes(oUsuario,sBanco)
            # ALTERAR SENHA
            bPermissaoAlterarSenha = oLogin.verificaPermissao("Usuario", "AlterarSenha", sBanco)
            #print(bPermissaoAlterarSenha)

            #VERIFICA AS PERMISSÕES
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

    vPermissoes = {"BLOCK_MENU_ADMINISTRATIVO":bVisualizaMenuAdministrativo,"BLOCK_MENU_ALTERA_SENHA":bVisualizarMenuAlterarDados,"BLOCK_MENU_USUARIOS":bVisualizarMenuUsuario,"BLOCK_MENU_GRUPO_USUARIOS":bVisualizarMenuGrupoUsuario,"BLOCK_MENU_TRANSACOES":bVisualizarMenuTransacao,"BLOCK_MENU_LOG":bVisualizarMenuLogTransacao,"BLOCK_MENU_ERROS_ACESSO":bVisualizarMenuLogAcesso,"BLOCK_MENU_ERROS_SQL":bVisualizarMenuLogErrosSQL}

    vTextos = {"PAGINAATUAL":"Painel Administrativo","USUARIOLOGADO":sNomeUsuarioLogado}

    #print(oLogin.vPermissao)

    if 'oLoginAdm' in session:
        # RESET DAS MENSAGENS
        session['sMsgPermissao'] = ""
        session['sTipoAlertaMensagem'] = ""
        session['sTipoAlertaLogo'] = ""
        return render_template('index/index.html',ANORODAPE=2023, vMsg=vMsg, vTextos=vTextos, vPermissoes=vPermissoes)
    else:
        return redirect('/login')