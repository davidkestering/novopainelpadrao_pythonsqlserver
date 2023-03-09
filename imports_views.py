import helpers
from app import app
from flask import render_template, request, redirect, session, url_for
from datetime import datetime
from classes.FachadaSegurancaBD import FachadaSegurancaBD
import json
import constantes as ct

ID_USUARIO = 0
IP_USUARIO = None
sBanco = ct.BANCO

oFachadaSeguranca = FachadaSegurancaBD(sBanco=sBanco)