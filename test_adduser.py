import os
from main import UserApp
import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from database import Database

db_path = os.path.join(os.path.dirname(__file__), 'users.db')

def test_add(qtbot: QtBot):
    nom_user = "sofia"
    pass_user = "sofia"
    role_user = "user"

    widget = UserApp()
    qtbot.addWidget(widget)
    
    ### Ací comprobem que el widget s'afegeix als qLine de l a finestra
    widget.finestra.lineEdit.setText(nom_user)
    widget.finestra.lineEdit_2.setText(pass_user)
    widget.finestra.lineEdit_3.setText(role_user)
    
    # No sé com comprovar que s'ha afegit a la taula del widget
    # Aixina que contaré les fines que hi havia abans i les que hi ha despres al inserir el nou usuari
    
    files_abans = widget.table.rowCount()
    
    widget.add_user()
    
    files_despres = widget.table.rowCount()
    
    # Prova a partir de la funció load_users
    users = widget.db.get_users()
    trobat = False
    for i in range(len(users)):
        nom_taula = widget.table.item(i,0).text()
        pass_taula = widget.table.item(i,1).text()
        role_taula = widget.table.item(i,2).text()
        
        if (nom_taula == nom_user) and (pass_taula == pass_user) and (role_user == role_taula):
            trobat = True
            break
        
        
    
        
    ###ara anem a comprovar que s'afegeix a la base de dades
    widget.db = QSqlDatabase.addDatabase('QSQLITE')
    widget.db.setDatabaseName(db_path)
    if widget.db.open():
        query = QSqlQuery()
        query.prepare("SELECT name, password, role FROM users WHERE name=? AND password=? AND role=?")
        query.addBindValue(nom_user)
        query.addBindValue(pass_user)
        query.addBindValue(role_user)
        query.exec()
    widget.db.close()
    query.next()
    nom_trobat = query.value(0)
    pass_trobat = query.value(1)
    role_trobada = query.value(2)
    
    assert files_abans == (files_despres-1)
    
    assert trobat

    assert nom_trobat == nom_user
    assert pass_trobat == pass_user
    assert role_trobada == role_user
    
