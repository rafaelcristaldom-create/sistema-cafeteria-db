import sys
import requests # Importação necessária para carregar a imagem da web
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QStackedWidget, QRadioButton, 
                             QButtonGroup, QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt

# Dados dos produtos para fácil manutenção
PRODUTOS = {
    "Café Comum": 4.00,
    "Café Expresso": 6.00,
    "Achocolatado": 8.00
}
TAXA_ENTREGA = 6.00

class TelaInicial(QWidget):
    """A tela de boas-vindas da aplicação."""
    def __init__(self, ir_para_menu_callback):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_titulo = QLabel("Café Aconchego")
        label_titulo.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("color: #4a2c2a;")

        # --- IMAGEM DA WEB REINSERIDA AQUI ---
        label_imagem = QLabel(self)
        try:
            # URL de uma imagem de alta qualidade de uma xícara de café
            image_url = "https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            # Baixa a imagem
            image_data = requests.get(image_url).content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            # Define a imagem no label, com um tamanho razoável
            label_imagem.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            label_imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            # Caso haja erro de conexão, exibe um texto alternativo
            print(f"Erro ao carregar imagem da web: {e}")
            label_imagem.setText("Imagem não disponível")
            label_imagem.setFont(QFont("Arial", 10))
            label_imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)


        label_descricao = QLabel(
            "Onde cada xícara conta uma história. Clique abaixo para iniciar seu pedido."
        )
        label_descricao.setFont(QFont("Arial", 12))
        label_descricao.setWordWrap(True)
        label_descricao.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_descricao.setStyleSheet("color: #6b4f4b;")

        self.botao_iniciar = QPushButton("Fazer Pedido")
        self.botao_iniciar.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.botao_iniciar.setMinimumHeight(50)
        self.botao_iniciar.setStyleSheet("""
            QPushButton { background-color: #c8a2c8; color: white; border-radius: 10px; }
            QPushButton:hover { background-color: #a47ab4; }
        """)
        self.botao_iniciar.clicked.connect(ir_para_menu_callback)

        layout.addWidget(label_titulo)
        layout.addWidget(label_imagem) # Imagem adicionada ao layout
        layout.addWidget(label_descricao)
        layout.addStretch()
        layout.addWidget(self.botao_iniciar)
        self.setLayout(layout)

class TelaMenu(QWidget):
    """A tela para seleção de produtos."""
    def __init__(self, ir_para_entrega_callback):
        super().__init__()
        self.ir_para_entrega_callback = ir_para_entrega_callback
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label_titulo = QLabel("Escolha seu Produto")
        label_titulo.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        label_titulo.setStyleSheet("color: #4a2c2a;")
        layout.addWidget(label_titulo)

        self.grupo_produtos = QButtonGroup(self)
        for nome, preco in PRODUTOS.items():
            radio = QRadioButton(f"{nome} - R$ {preco:.2f}")
            radio.setFont(QFont("Arial", 14))
            self.grupo_produtos.addButton(radio)
            layout.addWidget(radio)
        
        self.grupo_produtos.buttonClicked.connect(self.habilitar_botao)

        self.botao_avancar = QPushButton("Selecionar Entrega")
        self.botao_avancar.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.botao_avancar.setMinimumHeight(50)
        self.botao_avancar.setEnabled(False) # Começa desabilitado
        self.botao_avancar.setStyleSheet("""
            QPushButton { background-color: #a0a0a0; color: white; border-radius: 10px; }
            QPushButton:enabled { background-color: #c8a2c8; }
            QPushButton:hover:enabled { background-color: #a47ab4; }
        """)
        self.botao_avancar.clicked.connect(self.avancar)
        
        layout.addStretch()
        layout.addWidget(self.botao_avancar)
        self.setLayout(layout)

    def habilitar_botao(self):
        self.botao_avancar.setEnabled(True)
    
    def avancar(self):
        produto_selecionado = self.grupo_produtos.checkedButton().text().split(" - ")[0]
        preco = PRODUTOS[produto_selecionado]
        self.ir_para_entrega_callback(produto_selecionado, preco)

class TelaEntrega(QWidget):
    """A tela para escolher o tipo de entrega e finalizar."""
    def __init__(self, voltar_callback):
        super().__init__()
        self.produto_nome = ""
        self.produto_preco = 0.0

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.label_resumo = QLabel("Resumo do Pedido")
        self.label_resumo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.label_resumo.setStyleSheet("color: #4a2c2a;")
        layout.addWidget(self.label_resumo)

        self.label_subtotal = QLabel("Subtotal: R$ 0.00")
        self.label_subtotal.setFont(QFont("Arial", 14))
        layout.addWidget(self.label_subtotal)

        label_tipo_entrega = QLabel("Como deseja receber?")
        label_tipo_entrega.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(label_tipo_entrega)

        self.radio_retirar = QRadioButton("Retirar no local")
        self.radio_retirar.setFont(QFont("Arial", 12))
        self.radio_retirar.setChecked(True)
        self.radio_retirar.toggled.connect(self.atualizar_total)
        layout.addWidget(self.radio_retirar)

        self.radio_entregar = QRadioButton("Entregar (+ R$ 6,00)")
        self.radio_entregar.setFont(QFont("Arial", 12))
        self.radio_entregar.toggled.connect(self.atualizar_total)
        layout.addWidget(self.radio_entregar)

        self.campo_endereco = QLineEdit()
        self.campo_endereco.setPlaceholderText("Digite seu endereço completo")
        self.campo_endereco.setFont(QFont("Arial", 12))
        self.campo_endereco.setVisible(False) # Começa oculto
        layout.addWidget(self.campo_endereco)

        self.label_total = QLabel("Total: R$ 0.00")
        self.label_total.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.label_total.setStyleSheet("color: #c0392b;")
        layout.addWidget(self.label_total)
        
        self.botao_finalizar = QPushButton("Finalizar Pedido")
        self.botao_finalizar.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.botao_finalizar.setMinimumHeight(50)
        self.botao_finalizar.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; border-radius: 10px; }
            QPushButton:hover { background-color: #229954; }
        """)
        self.botao_finalizar.clicked.connect(self.finalizar_pedido)
        
        layout.addStretch()
        layout.addWidget(self.botao_finalizar)
        self.setLayout(layout)

    def set_pedido(self, produto, preco):
        self.produto_nome = produto
        self.produto_preco = preco
        self.label_resumo.setText(f"Produto: {self.produto_nome}")
        self.radio_retirar.setChecked(True) # Garante que a opção padrão seja selecionada
        self.atualizar_total()

    def atualizar_total(self):
        self.label_subtotal.setText(f"Subtotal: R$ {self.produto_preco:.2f}")
        total = self.produto_preco
        if self.radio_entregar.isChecked():
            total += TAXA_ENTREGA
            self.campo_endereco.setVisible(True)
        else:
            self.campo_endereco.setVisible(False)
        
        self.label_total.setText(f"Total: R$ {total:.2f}")
    
    def finalizar_pedido(self):
        entrega = self.radio_entregar.isChecked()
        endereco = self.campo_endereco.text()

        if entrega and not endereco.strip():
            QMessageBox.warning(self, "Endereço Faltando", "Por favor, insira o endereço de entrega.")
            return

        QMessageBox.information(self, "Pedido Confirmado!", "Seu pedido foi realizado com sucesso e já está sendo preparado!")
        self.parent().parent().ir_para_inicio()


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Café Aconchego - Sistema de Pedidos")
        self.setGeometry(100, 100, 500, 650) # Aumentei a altura para a imagem caber bem
        self.setStyleSheet("background-color: #f5e6e8;")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Criação das telas
        self.tela_inicial = TelaInicial(self.ir_para_menu)
        self.tela_menu = TelaMenu(self.ir_para_entrega)
        self.tela_entrega = TelaEntrega(self.ir_para_menu)

        # Adição das telas ao "baralho"
        self.stacked_widget.addWidget(self.tela_inicial)
        self.stacked_widget.addWidget(self.tela_menu)
        self.stacked_widget.addWidget(self.tela_entrega)

    def ir_para_inicio(self):
        self.stacked_widget.setCurrentWidget(self.tela_inicial)

    def ir_para_menu(self):
        self.stacked_widget.setCurrentWidget(self.tela_menu)

    def ir_para_entrega(self, produto, preco):
        self.tela_entrega.set_pedido(produto, preco)
        self.stacked_widget.setCurrentWidget(self.tela_entrega)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
