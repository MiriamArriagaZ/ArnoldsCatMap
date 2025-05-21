import os
import tkinter as tk
from PIL import Image, ImageTk
#Cambiar al directorio del archivo forzando la búsqueda en el actual
os.chdir(os.path.dirname(__file__))
#Verifica si dos imágenes son idénticas
def images_are_equal(img1: Image.Image, img2: Image.Image) -> bool:
    return list(img1.getdata()) == list(img2.getdata())
#Aplica una iteración para modificar la imagen
def arnold_cat_map(img: Image.Image) -> Image.Image:
    width, height = img.size
    new_img = Image.new(img.mode, img.size)
    for x in range(width):
        for y in range(height):
            nx = (2 * x + y) % width
            ny = (x + y) % height
            new_img.putpixel((nx, height - ny - 1), img.getpixel((x, height - y - 1)))
    return new_img
#Inicia la animación de transformaciones para no tener que generar un archivo nuevo por iteración
def start_animation(original_img: Image.Image, delay=200):
    current_img = original_img.copy()
    iteration = 0
    frames = [original_img.copy()]
    def update():
        nonlocal current_img, iteration
        iteration += 1
        current_img = arnold_cat_map(current_img)
        frames.append(current_img.copy())
        #Mostrar imagen
        img_tk = ImageTk.PhotoImage(current_img)
        label.config(image=img_tk)
        label.image = img_tk
        print(f"Iteración {iteration}")
        #Detener si vuelve a su forma original
        if images_are_equal(current_img, original_img):
            print(f"\n🔁 La imagen volvió a su estado original tras {iteration} iteraciones.")
        else:
            root.after(delay, update)
    update()
#Ruta de la imagen
image_path = "cat.jpeg"
if not os.path.exists(image_path):
    print("Carpeta actual:", os.getcwd())
    print("Archivos en la carpeta:", os.listdir())
    raise FileNotFoundError(f"No se encontró la imagen '{image_path}' en la carpeta actual.")
#Cargar imagen original
original_img = Image.open(image_path).convert("RGB")
if original_img.size[0] != original_img.size[1]:
    raise ValueError("La imagen debe ser cuadrada (mismo ancho y alto)")
#Crear interfaz
root = tk.Tk()
root.title("Arnold's Cat Map (Visualizador)")
#Mostrar imagen inicial
img_tk = ImageTk.PhotoImage(original_img)
label = tk.Label(root, image=img_tk)
label.pack()
#Iniciar transformación
root.after(1000, lambda: start_animation(original_img, delay=300))
root.mainloop()
