# Importar el módulo kivy
import kivy
# Importar la clase ProgressBar de kivy
from kivy.uix.progressbar import ProgressBar
# Importar la clase Image de kivy para cargar las imágenes
from kivy.core.image import Image
# Importar la clase Clock de kivy para animar la barra de progreso
from kivy.clock import Clock
# Importar la clase Rectangle de kivy
from kivy.graphics import Rectangle, Color, Ellipse
# Importar la clase App de kivy
from kivy.app import App
# Importar la clase BoxLayout de kivy
from kivy.uix.boxlayout import BoxLayout
# Importar la clase Button de kivy
from kivy.uix.button import Button
# Importar la clase CompoundSelectionBehavior de kivy
from kivy.graphics.stencil_instructions import StencilView
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
# Crear una clase que hereda de App
# Crear la clase ImageProgressBar que hereda de ProgressBar
class ImageProgressBar(ProgressBar):

    # Inicializar la clase con los parámetros splash y progressimg
    def __init__(self, splash, progressimg, **kwargs):
        # Llamar al método __init__ de la clase padre
        super(ImageProgressBar, self).__init__(**kwargs)

        # Cargar las imágenes como texturas
        self.splash = Image(splash).texture
        self.progressimg = Image(progressimg).texture

        # Crear una vista de estarcido (StencilView) para la imagen de progreso
        self.shape = StencilView(size=self.size)
        self.shape.add_widget(Ellipse(texture=self.progressimg, pos=(0, 0), size=self.progressimg.size))

        # Dibujar la barra de progreso con las imágenes
        self.draw()

    # Método para dibujar la barra de progreso con las imágenes
    def draw(self):
        # Limpiar el lienzo
        self.canvas.clear()

        # Dibujar la imagen de fondo
        with self.canvas:
            Rectangle(texture=self.splash, pos=self.pos, size=self.size)

        # Calcular el ancho de la barra de progreso según el valor normalizado
        width = self.value_normalized * self.width

        # Dibujar la barra de progreso detrás de la imagen recortada
        with self.canvas.after:
            Color(1, 0, 0, 0.1) # Rojo con 50% de opacidad
            Rectangle(pos=self.pos, size=(width, self.height))

        # Usar la forma compuesta como máscara de recorte
        with self.canvas.before:
            self.shape.use_clip = True
            self.shape.pos = self.pos
            self.shape.size = self.size

    # Método para actualizar el valor de la barra de progreso
    def set_value(self, value):
        # Asignar el valor al atributo value
        self.value = value

        # Redibujar la barra de progreso con el nuevo valor
        self.draw()

class ImageProgressBarApp(App):

    # Método para construir la interfaz de la aplicación
    def build(self):
        # Crear un contenedor vertical
        layout = BoxLayout(orientation='vertical')

        # Crear una instancia de la clase ImageProgressBar con las imágenes splash.png y progressimg.png
        # El valor máximo es 100 y el valor inicial es 0
        self.ipb = ImageProgressBar(splash='splash.png', progressimg='espectrometro.png', max=100, value=0)

        # Crear un botón para iniciar la animación de la barra de progreso
        button = Button(text='Iniciar', on_press=self.start, size_hint_y=0.1)

        # Añadir la barra de progreso y el botón al contenedor
        layout.add_widget(self.ipb)
        layout.add_widget(button)

        # Devolver el contenedor como la interfaz de la aplicación
        return layout

    # Método para iniciar la animación de la barra de progreso
    def start(self, instance):
        # Programar la función animate para que se ejecute cada 0.1 segundos
        Clock.schedule_interval(self.animate, 0.1)

    # Método para animar la barra de progreso
    def animate(self, dt):
        # Si el valor es menor que el máximo, incrementarlo en 1
        if self.ipb.value < self.ipb.max:
            self.ipb.set_value(self.ipb.value + 1)
        # Si no, reiniciar el valor a 0
        else:
            self.ipb.set_value(0)

# Ejecutar la aplicación
if __name__ == '__main__':
    ImageProgressBarApp().run()
