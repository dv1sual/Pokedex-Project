import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, \
    QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QComboBox, QFrame
from PyQt6.QtGui import QPixmap, QImageReader, QFont
from PyQt6.QtCore import Qt, QBuffer


class PokedexApp(QFrame):
    def __init__(self):
        super().__init__()

        # Set up the layout and widgets
        self.init_ui()

    def init_ui(self):
        # Set up the layout
        main_layout = QVBoxLayout()

        # Create a title label
        title_label = QLabel("What are\nyou looking for?")
        title_label.setFont(QFont('Helvetica Neue', 28, QFont.Weight.ExtraBold))
        title_label.setStyleSheet('color: white;')
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(title_label)

        # Create a search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search pokemons, items, etc')
        self.search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid;
                border-radius: 10px;
                padding: 3 8px;
                background: white;
                selection-background-color: darkgray;
            }
        """)
        self.search_bar.returnPressed.connect(self.search_pokemon)  # Trigger search when Enter is pressed
        main_layout.addWidget(self.search_bar)

        # Create a big bold green Pokémon button
        pokemon_button = QPushButton('Pokémon')
        pokemon_button.setFont(QFont('Arial Rounded MT Bold', 12))
        pokemon_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                border: none;
                color: white;
                padding: 20px 25px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }
        """)
        main_layout.addWidget(pokemon_button)

        # Create two additional buttons for "Items" and "Moves"
        items_button = QPushButton('Items')
        items_button.setFont(QFont('Arial Rounded MT Bold', 12))
        items_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                border: none;
                color: white;
                padding: 20px 25px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }
        """)
        moves_button = QPushButton('Moves')
        moves_button.setFont(QFont('Arial Rounded MT Bold', 12))
        moves_button.setStyleSheet("""
            QPushButton {
                background-color: blue;
                border: none;
                color: white;
                padding: 20px 25px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.addWidget(items_button)
        button_layout.addWidget(moves_button)
        main_layout.addLayout(button_layout)

        # Create an image label to display the Pokemon sprite
        self.image_label = QLabel()
        main_layout.addWidget(self.image_label)

        # Create a label to display the Pokemon name
        self.name_label = QLabel()
        main_layout.addWidget(self.name_label)

        # Set the layout and window properties
        self.setLayout(main_layout)
        self.setWindowTitle('Pokedex')
        self.setGeometry(300, 300, 400, 400)

        # Set the background color of the window
        self.setStyleSheet("""
            PokedexApp {
                background-color: #252525;
            }
        """)

        self.show()

    def search_pokemon(self):
        # Get the user's input and query the PokeAPI
        query = self.search_bar.text().lower()
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{query}')

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Display the Pokemon sprite
            image_url = data['sprites']['front_default']
            image_response = requests.get(image_url)

            # Store the image data in a QBuffer
            image_buffer = QBuffer()
            image_buffer.setData(image_response.content)

            image_reader = QImageReader()
            image_reader.setDecideFormatFromContent(True)
            image_reader.setDevice(image_buffer)
            pixmap = QPixmap.fromImageReader(image_reader)
            self.image_label.setPixmap(pixmap)

            # Display the Pokemon name
            name = data['name'].capitalize()
            self.name_label.setText(name)
        else:
            self.name_label.setText('Pokemon not found')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pokedex_app = PokedexApp()
    sys.exit(app.exec())
