import re
import os

js_path = "gd_web.js"
data_path = "gd_web.data"
output_dir = "Resources"

if not os.path.exists(js_path) or not os.path.exists(data_path):
    print("Asegúrate de que gd_web.js y gd_web.data estén en la misma carpeta.")
    exit()

with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
    js_content = f.read()

# Buscar los metadatos de los archivos empaquetados en el JS
matches = re.findall(r'\{\s*"filename"\s*:\s*"([^"]+)"\s*,\s*"start"\s*:\s*(\d+)\s*,\s*"end"\s*:\s*(\d+)', js_content)

if not matches:
    # Intento con formato alternativo de emscripten
    matches = re.findall(r'packageData\.files\.push\(\{\s*filename:\s*[\'"]([^\'"]+)[\'"]\s*,\s*start:\s*(\d+)\s*,\s*end:\s*(\d+)', js_content)

if not matches:
    print("No se encontró el mapa de archivos en gd_web.js.")
    exit()

os.makedirs(output_dir, exist_ok=True)

with open(data_path, "rb") as f_data:
    for filename, start, end in matches:
        start_bytes = int(start)
        end_bytes = int(end)
        length = end_bytes - start_bytes
        
        f_data.seek(start_bytes)
        file_bytes = f_data.read(length)
        
        # Guardar en la carpeta
        clean_name = os.path.basename(filename)
        out_file_path = os.path.join(output_dir, clean_name)
        
        with open(out_file_path, "wb") as f_out:
            f_out.write(file_bytes)
        print(f"Extraído: {clean_name} ({length} bytes)")

print("\n¡Extracción completada!")