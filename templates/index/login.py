from imports_views import *

@app.route('/login', methods=['GET'])
def login():
    vMsg = helpers.carregaMensagens()

    if 'oLoginAdm' in session:
        return redirect('/')
    else:
        # RESET DAS MENSAGENS
        session['sMsgPermissao'] = ""
        session['sTipoAlertaMensagem'] = ""
        session['sTipoAlertaLogo'] = ""
        return render_template('index/login.html', ANORODAPE=2023, vMsg=vMsg)