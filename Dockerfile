FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# Instalar libgomp1 para soporte de operaciones paralelas
RUN apt-get update && apt-get install -y libgomp1

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias antes de copiar el código del proyecto
COPY requirements.txt /app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . /app

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8001

# Comando para iniciar la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--log-level", "debug"]
