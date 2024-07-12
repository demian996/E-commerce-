# Usa una imagen base oficial de Python como imagen base
FROM python:3.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y luego instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de tu proyecto en el contenedor
COPY . .

# Establece el comando de inicio del contenedor
CMD ["flask", "run", "--host=0.0.0.0"]
