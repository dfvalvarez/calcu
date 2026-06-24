from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle


AZUL = (0.1, 0.4, 0.8, 1)          
PLOMO_BAJO = (0.88, 0.88, 0.88, 1) 
BLANCO = (1, 1, 1, 1)           
NEGRO = (0, 0, 0, 1)              


class Calculadora(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.historial = []

        
        with self.canvas.before:
            Color(*BLANCO)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

       
        self.pantalla = TextInput(
            multiline=False,
            halign="right",
            font_size=32,
            size_hint=(1, 0.2),
            background_normal='',
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=NEGRO
        )
        self.add_widget(self.pantalla)

       
        btn_historial = Button(
            text="Historial",
            font_size=20,
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
                color_boton = AZUL
                color_texto = BLANCO
            else:
                color_boton = PLOMO_BAJO
                color_texto = NEGRO

            btn = Button(
                text=tecla,
                font_size=24,
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
        self.parent.manager.current = "historial"

    def presionar(self, instancia):
        texto = instancia.text

        if texto == "C":
            self.pantalla.text = ""
        elif texto == "<-":
            self.pantalla.text = self.pantalla.text[:-1]
        elif texto == "DEL":
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
            self.pantalla.text += texto


class PantallaHistorial(Screen):

    def __init__(self, calculadora, **kwargs):
        super().__init__(**kwargs)
        self.calculadora = calculadora

      
        with self.canvas.before:
            Color(*BLANCO)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

    
        titulo = Label(
            text="Historial",
            font_size=28,
            size_hint=(1, 0.15),
            color=AZUL,
            
        )
        layout.add_widget(titulo)

       
        self.label_historial = Label(
            text="No hay operaciones",
            font_size=20,
            color=NEGRO,
            halign="center",
            valign="middle"
        )
        self.label_historial.bind(size=self.label_historial.setter('text_size'))
        layout.add_widget(self.label_historial)

        
        btn_volver = Button(
            text="Volver",
            font_size=22,
            size_hint=(1, 0.15),
            background_normal='',
            background_color=PLOMO_BAJO,
            color=NEGRO
        )
        btn_volver.bind(on_press=self.volver)
        layout.add_widget(btn_volver)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_pre_enter(self):
        if self.calculadora.historial:
            self.label_historial.text = "\n".join(
                reversed(self.calculadora.historial)
            )
        else:
            self.label_historial.text = "No hay operaciones"

    def volver(self, instance):
        self.manager.current = "calculadora"


class CalculadoraApp(App):

    def build(self):
        sm = ScreenManager()
        calculadora = Calculadora()

        pantalla_calculadora = Screen(name="calculadora")
        pantalla_calculadora.add_widget(calculadora)

        pantalla_historial = PantallaHistorial(calculadora, name="historial")

        sm.add_widget(pantalla_calculadora)
        sm.add_widget(pantalla_historial)

        return sm


if __name__ == "__main__":
    CalculadoraApp().run()
