FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el contenido del proyecto al directorio de trabajo
COPY ./app /app

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir pandas pycaret fastapi[all]

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8001

# Comando para iniciar la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
