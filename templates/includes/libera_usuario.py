from imports_views import *

@app.route('/libera_usuario', methods=['POST'])
def libera_usuario():
    # Itera sobre a propriedade args -GET
    # for key, value in request.args.items():
    #     print(f"{key}: {value}")

    # Itera sobre a propriedade form - POST
    # for key, value in request.form.items():
    #     print(f"{key}: {value}")

    nIdUsuario = None

    if session.get('oLoginAdm'):
        nIdUsuario = session['oLoginAdm']['nId']

    if 'fIdUsuario' in request.form:
        nIdUsuario = request.form['fIdUsuario']

    if(nIdUsuario != None and nIdUsuario != 0):
        oUsuario = oFachadaSeguranca.recuperaUsuario(nIdUsuario,sBanco)
        if(oUsuario != None and isinstance(oUsuario,object)):
            oUsuario.setLogado("0")
            nIdTipoTransacaoLogado = oFachadaSeguranca.recuperaTipoTransacaoPorDescricaoCategoria("Usuario","Alterar",sBanco)
            sObjetoLogado = f"Usuário {oUsuario.getNmUsuario()} liberou a disponibilidade de novo login para o usuário: {oUsuario.getLogin()}"
            oTransacaoLogado = oFachadaSeguranca.inicializaTransacao("",nIdTipoTransacaoLogado,oUsuario.getId(),sObjetoLogado,"","","",IP_USUARIO,ct.DATAHORA,1,1)
            oFachadaSeguranca.alteraUsuario(oUsuario,oTransacaoLogado,sBanco)
            oUsuarioAuxiliar = oFachadaSeguranca.recuperaUsuario(oUsuario.getId(),sBanco)
            if(oUsuarioAuxiliar != None and isinstance(oUsuarioAuxiliar,object)):
                sConteudo = "Usuário liberado com sucesso!"
            else:
                sConteudo = "Não foi possível liberar o usuário!"
        else:
            sConteudo = "Usuário não encontrado!"
    else:
        sConteudo = "Problemas na execução, tente novamente!"

    return sConteudo