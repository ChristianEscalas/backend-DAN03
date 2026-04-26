# Versión de Python
FROM python:3.12.10

# Carpeta donde está el código
WORKDIR /app

# Copiar requerimientos
COPY requerimientos.txt .

# Instalar las dependencias del entorno virtual
RUN pip install --no-cache-dir -r requerimientos.txt

# Copiar código
COPY app/ /app/

# Puerto usado
EXPOSE 5000

# Como arrancar la app
CMD ["python", "app.py"]