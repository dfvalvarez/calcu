from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.metrics import sp  # <-- IMPORTANTE: Escala los textos en móviles

# Paleta estricta Azul y Blanco
AZUL = (0.1, 0.4, 0.8, 1)
BLANCO = (1, 1, 1, 1)

class Calculadora(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.historial = []
        self.screen_manager = None

        with self.canvas.before:
            Color(*BLANCO)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Pantalla principal
        self.pantalla = TextInput(
            multiline=False,
            halign="right",
            font_size=sp(48),  # Aumentado y escalable
            size_hint=(1, 0.2),
            background_normal='',
            background_color=BLANCO,
            foreground_color=AZUL  # Texto azul
        )
        self.add_widget(self.pantalla)

        # Botón de historial
        btn_historial = Button(
            text="Historial",
            font_size=sp(22),
            size_hint=(1, 0.1),
            background_normal='',
            background_color=AZUL,
            color=BLANCO
        )
        btn_historial.bind(on_press=self.abrir_historial)
        self.add_widget(btn_historial)

        botones = GridLayout(cols=4, spacing=2, padding=2)

        teclas = [
            "C", "<-", "DEL", "/",
            "7", "8", "9", "*",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "0", ".", "%", "="
        ]

        for tecla in teclas:
            if tecla in ["C", "<-", "DEL", "/", "*", "-", "+", "=", "%"]:
                # Operadores: Fondo azul, texto blanco
                color_boton = AZUL
                color_texto = BLANCO
            else:
                # Números: Fondo blanco, texto azul
                color_boton = BLANCO
                color_texto = AZUL

            btn = Button(
                text=tecla,
                font_size=sp(34),  # Tamaño de botones mucho más grande para el tacto
                background_normal='',
                background_color=color_boton,
                color=color_texto
            )
            btn.bind(on_press=self.presionar)
            botones.add_widget(btn)

        self.add_widget(botones)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def abrir_historial(self, instance):
        if self.screen_manager:
            self.screen_manager.current = "historial"

    def presionar(self, instancia):
        texto = instancia.text

        if texto == "C":
            self.pantalla.text = ""
        elif texto == "DEL":
            self.pantalla.text = self.pantalla.text[:-1]
        elif texto == "<-":
            self.pantalla.text = ""
        elif texto == "=":
            try:
                expresion = self.pantalla.text.replace("%", "/100")
                resultado = eval(expresion)
                operacion = f"{self.pantalla.text} = {resultado}"
                self.historial.append(operacion)
                self.pantalla.text = str(resultado)
            except Exception:
                self.pantalla.text = "Error"
        else:
            if self.pantalla.text == "Error":
                self.pantalla.text = ""
