from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHeaderView, QDialog
from database import Database
import sys
import os
from PySide6.QtUiTools import QUiLoader
from functools import partial

class UserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestió d'Usuaris")
        self.setGeometry(100, 100, 600, 500)
        self.db = Database(db_name=os.path.join(os.path.dirname(__file__), 'users.db'))
        
        #Carreguem la finestra
        loader = QUiLoader()
        finestra_path = os.path.join(os.path.dirname(__file__), "finestra.ui")
        self.finestra = loader.load(finestra_path, None)
        

        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)
        
        #Propietat que ens ajuda en fer els tests
        self.test = False

        # # Formulari (afegit directament a la finestra)
        # self.name_input = QLineEdit()
        # self.password_input = QLineEdit() 
        # self.role_input = QLineEdit() 

        # self.layout.addWidget(QLabel("Nom:"))
        # self.layout.addWidget(self.name_input)
        # self.layout.addWidget(QLabel("Contrasenya:"))  
        # self.layout.addWidget(self.password_input)
        # self.layout.addWidget(QLabel("Rol (Admin, Usuari, Convidat):")) 
        # self.layout.addWidget(self.role_input)

        # Botons per afegir i modificar
        # He possat lo del partial per a que no m'aparga la finestra de plenar els camps
        # durant el test i que es quede penjada. Vull dir, com no sabia com
        # no cridar a esta finestra durant el test l'he posat fora de les funcions
        # add_user i modificar_user i axina cride a estes funcions desde la funció
        # de executar_finestra. Però com necessitava saber qui crida a la finestra he gastat partial.
        # Ho faig aixina pq no sé fer test de un QMainWindow amb un Qdialeg
        self.add_button = QPushButton("Afegir Usuari")
        self.add_button.clicked.connect(partial(self.executar_finestra, "add"))
        self.layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Modificar Usuari")
        self.edit_button.clicked.connect(partial(self.executar_finestra, "mod"))
        self.layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar Usuari")
        self.delete_button.clicked.connect(self.delete_user)
        self.layout.addWidget(self.delete_button)

        # Taula d'usuaris
        self.table = self.create_table()
        self.layout.addWidget(self.table)

        self.load_users()
        
    def executar_finestra(self, opcio):
        if opcio == "add" and self.finestra.exec_() == QDialog.Accepted:
            self.add_user()
        elif opcio == "mod":
            selected_row = self.table.currentRow()
            if selected_row == -1:
                #Ací cridem a un QMessageBox
                QMessageBox.warning(self, "Error", "Ha s de seleccionar un usuari")
                return
            
            if self.test == False:
                self.boto_pres = QMessageBox.warning(self,"Confirmació d'acció","Modificar usuari?",buttons=QMessageBox.Ok | QMessageBox.Close, defaultButton=QMessageBox.Close)
            if self.boto_pres == QMessageBox.Ok:
            
                user_id = self.db.get_users()[selected_row][0]
                user_name = self.db.get_users()[selected_row][1]
                user_pass = self.db.get_users()[selected_row][2]
                user_role = self.db.get_users()[selected_row][3]

                self.finestra.lineEdit.setText(user_name)
                self.finestra.lineEdit_2.setText(user_pass)
                self.finestra.lineEdit_3.setText(user_role)
                if self.finestra.exec_() == QDialog.Accepted:
                    self.edit_user(user_id)
                    # print("Es canviara el usuari")

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nom", "Contrasenya", "Rol"])  
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        table.setSelectionBehavior(QTableWidget.SelectRows)  
        return table

    def load_users(self):
        self.table.setRowCount(0)
        users = self.db.get_users()
        for row_index, (user_id,name, password, role) in enumerate(users):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(password))  
            self.table.setItem(row_index, 2, QTableWidgetItem(role))

    def add_user(self):
        # name = self.name_input.text()
        # password = self.password_input.text() 
        # role = self.role_input.text()  
        
        name = self.finestra.lineEdit.text()
        password = self.finestra.lineEdit_2.text()
        role = self.finestra.lineEdit_3.text()

        if name and password and role:
            self.db.add_user(name, password, role)
            self.load_users()

    def edit_user(self, user_id):
        # new_name = self.name_input.text()
        # new_password = self.password_input.text()  
        # new_role = self.role_input.text()
        
        new_name = self.finestra.lineEdit.text()
        new_password = self.finestra.lineEdit_2.text()
        new_role = self.finestra.lineEdit_3.text()
        if new_name and new_password and new_role:
            self.db.update_user(user_id, new_name, new_password, new_role)
            self.load_users()

    def delete_user(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Ha s de seleccionar un usuari")
            return
        
        if self.test == False:
            self.boto_pres = QMessageBox.warning(self,"Confirmació d'acció","Eliminar usuari?",buttons=QMessageBox.Ok | QMessageBox.Close, defaultButton=QMessageBox.Close)
        
        if self.boto_pres == QMessageBox.Ok:

            user_id = self.db.get_users()[selected_row][0]
            self.db.delete_user(user_id)
            self.load_users()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserApp()
    window.show()
    sys.exit(app.exec())