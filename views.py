from imports_views import *

@app.before_request
def registraConstantesGlobais():
    global IP_USUARIO
    IP_USUARIO = request.remote_addr

#TELA INICIAL
from templates.index import index

#TELA LOGIN
from templates.index import login

#PROCESSAMENTO DE LOGIN E LOGOUT
from templates.index import processaLoginLogout

#OPCAO DE LIBERAR USUARIO JA LOGADO
from templates.includes import libera_usuario

#TELA ALTERAR SENHA
from templates.painel.administrativo.alterar_senha import alterar_senha

#OUTROS METODOS E FUNCOES AUXILIARES
from helpers import *