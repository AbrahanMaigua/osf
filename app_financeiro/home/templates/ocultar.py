from Stegano import lsb
from PIL import Image

# Cargar la imagen donde deseas ocultar el mensaje
image_path = "47bc88ff92a7f6eadc837c0c48f1c550.jpg"  # Cambia por la ruta de tu imagen
output_path = "imagen_oculta.png"
mensaje = "Este es un mensaje oculto."
print(image_path)
# Ocultar el mensaje en la imagen
oculta = lsb.hide(image_path, mensaje)
oculta.save(output_path)

print(f"Mensaje oculto en '{output_path}'")
