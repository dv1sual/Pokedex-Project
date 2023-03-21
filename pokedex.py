import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCompleter, QFrame
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import threading
from PyQt6.QtCore import Qt, QMetaObject
from PyQt6.QtCore import Q_ARG
from PyQt6 import QtCore
from PyQt6.QtGui import QFont





import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCompleter, QFrame
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import threading
from PyQt6.QtCore import Qt, QMetaObject
from PyQt6.QtCore import Q_ARG
from PyQt6 import QtCore
from PyQt6.QtGui import QFont

class PokemonApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Pokedex')
        self.setFixedSize(1000, 600)

        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()

        self.label = QLabel("Pokémon:")
        label_font = QFont()
        label_font.setBold(True)
        label_font.setPointSize(26)
        self.label.setFont(label_font)
        input_layout.addWidget(self.label)

        self.textbox = QLineEdit()
        self.textbox.setFixedSize(700, 32)
        self.textbox.setStyleSheet("QLineEdit {"
                                   "border: 1px solid #000;"
                                   "border-radius: 10px;"
                                   "padding-left: 10px;"
                                   "padding-right: 10px;"
                                   "font: 14px;}")
        input_layout.addWidget(self.textbox)

        self.button = QPushButton("Get Info")
        self.button.setFixedSize(90, 28)
        self.button.setStyleSheet("QPushButton {"
                                  "background-color: #32CD32;"
                                  "border: none;"
                                  "border-radius: 10px;"
                                  "padding-left: 20px;"
                                  "padding-right: 20px;"
                                  "color: white;}"
                                  "QPushButton:hover {"
                                  "background-color: #2DB62D;}")
        input_layout.addWidget(self.button)

        main_layout.addLayout(input_layout)

        content_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.pokemon_name_label = QLabel()
        self.pokemon_name_label.setMargin(20)
        self.pokemon_name_label.setFixedSize(400, 80)
        left_layout.addWidget(self.pokemon_name_label)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setMinimumWidth(400)
        self.result_box.setMinimumHeight(400)
        left_layout.addWidget(self.result_box)

        content_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()

        # Image layout for main Pokemon image
        image_layout = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(230, 500)
        self.image_label.setStyleSheet("QLabel { background-color : transparent; }")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.image_label.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        image_layout.addWidget(self.image_label)
        self.set_image_position(margin_left=80, margin_top=150, margin_right=0, margin_bottom=0)
        right_layout.addLayout(image_layout)

        # Image layout for below Pokemon image
        below_image_layout = QHBoxLayout()
        below_pokemon_image = QPixmap("/Users/luca/Code/Pokemon Project/resources/Pokédex_logo.png")
        self.below_pokemon_image_label = QLabel()
        self.below_pokemon_image_label.setPixmap(
            below_pokemon_image.scaled(175, 175, Qt.AspectRatioMode.KeepAspectRatio))
        below_image_layout.addWidget(self.below_pokemon_image_label)
        self.set_below_image_position(margin_left=80, margin_top=0, margin_right=0, margin_bottom=0)
        right_layout.addLayout(below_image_layout)

        content_layout.addLayout(right_layout)

        main_layout.addLayout(content_layout)

        self.button.clicked.connect(self.fetch_pokemon_info)
        self.textbox.returnPressed.connect(self.button.click)

        self.autocomplete()

        self.setLayout(main_layout)

    def set_image_position(self, margin_left, margin_top, margin_right, margin_bottom):
        self.image_label.setContentsMargins(margin_left, margin_top, margin_right, margin_bottom)

    def set_below_image_position(self, margin_left, margin_top, margin_right, margin_bottom):
        self.below_pokemon_image_label.setContentsMargins(margin_left, margin_top, margin_right, margin_bottom)

    def autocomplete(self):
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1118')
        pokemon_names = [pokemon['name'] for pokemon in response.json()['results']]

        completer = QCompleter(pokemon_names)
        self.textbox.setCompleter(completer)

    def fetch_pokemon_info(self):
        pokemon_name = self.textbox.text().lower()

        if not pokemon_name:
            self.image_label.clear()
            self.pokemon_name_label.clear()
            self.result_box.clear()
            return

        # Disable the UI elements while fetching data
        self.textbox.setEnabled(False)
        self.button.setEnabled(False)
        self.result_box.clear()

        # Show a loading message
        self.result_box.setHtml("<p>Loading...</p>")

        # Create a thread to fetch data in the background
        thread = FetchPokemonThread(pokemon_name)
        thread.dataFetched.connect(self.show_pokemon_info)
        thread.start()

    @QtCore.pyqtSlot(object)
    def show_pokemon_info(self, data):

        # Enable the UI elements
        self.textbox.setEnabled(True)
        self.button.setEnabled(True)

        if data is None:
            # Show an error message if the data could not be fetched
            self.result_box.setHtml("<p>Error: Pokemon not found</p>")
            self.image_label.clear()
            self.pokemon_name_label.clear()
            return

        image_url = data['sprites']['front_default']
        image_data = requests.get(image_url).content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.image_label.setPixmap(
            pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        self.pokemon_name_label.setText(f"<b><font size='7'>{data['name'].capitalize()}</font></b><br><br>")

        species_response = requests.get(data['species']['url'])
        species_data = species_response.json()

        regions = []
        for pokedex in species_data['pokedex_numbers']:
            region_response = requests.get(pokedex['pokedex']['url'])
            region_data = region_response.json()
            if region_data['region'] is not None:
                region_name = region_data['region']['name']
                if region_name not in regions:
                    regions.append(region_name)

        moves = [move['move']['name'] for move in data['moves']]

        evolution_chain_response = requests.get(species_data['evolution_chain']['url'])
        evolution_chain_data = evolution_chain_response.json()
        evo_chain = []

        def extract_evolutions(evo_data):
            species_name = evo_data['species']['name']
            evo_chain.append(species_name)

            for evo_details in evo_data['evolves_to']:
                extract_evolutions(evo_details)

        extract_evolutions(evolution_chain_data['chain'])

        info = f"<b>Regions:</b> {self.format_bullet_points(regions)}<br>"
        info += f"<b>Moves:</b><br>{self.format_bullet_points(moves, three_columns=True)}<br><br>"
        info += f"<b>Evolution Chain:</b> {self.format_bullet_points(evo_chain)}<br>"
        self.result_box.setHtml(info)


    def format_bullet_points(self, items, two_columns=False, three_columns=False, three_columns_threshold=50):
        if not (two_columns or three_columns):
            return "<ul>" + "".join([f"<li>{item.capitalize()}</li>" for item in items]) + "</ul>"
        else:
            if three_columns and len(items) >= three_columns_threshold:
                col_size = len(items) // 3
                col1_items = items[:col_size]
                col2_items = items[col_size:2 * col_size]
                col3_items = items[2 * col_size:]
                columns = [col1_items, col2_items, col3_items]
            else:
                mid = len(items) // 2
                col1_items = items[:mid]
                col2_items = items[mid:]
                columns = [col1_items, col2_items]

            column_html = []
            for column_items in columns:
                column_html.append("<ul>" + "".join([f"<li>{item.capitalize()}</li>" for item in column_items]) + "</ul>")

            return f'<table><tr>{"".join([f"<td valign=top>{col}</td>" for col in column_html])}</tr></table>'

    def fetch_pokemon_info(self):
        pokemon_name = self.textbox.text().lower()

        if not pokemon_name:
            self.image_label.clear()
            self.pokemon_name_label.clear()
            self.result_box.clear()
            return

        # Disable the UI elements while the data is being fetched
        self.textbox.setEnabled(False)
        self.button.setEnabled(False)

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        t = threading.Thread(target=self.fetch_pokemon_info_thread, args=(url,))
        t.start()

    def fetch_pokemon_info_thread(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # Use invokeMethod() to call a slot in the main GUI thread to update the GUI elements
            QMetaObject.invokeMethod(self, "show_pokemon_info", Qt.ConnectionType.QueuedConnection,
                                      Q_ARG(object, data))
        else:
            # Use invokeMethod() to call a slot in the main GUI thread to update the GUI elements
            QMetaObject.invokeMethod(self, "show_pokemon_info", Qt.ConnectionType.QueuedConnection,
                                      Q_ARG(object, None))


    def autocomplete(self):
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1118')
        pokemon_names = [pokemon['name'] for pokemon in response.json()['results']]

        completer = QCompleter(pokemon_names)
        self.textbox.setCompleter(completer)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_widget = PokemonApp()
    main_widget.show()

    sys.exit(app.exec())