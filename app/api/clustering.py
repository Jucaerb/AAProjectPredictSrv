from fastapi import APIRouter, HTTPException, File, UploadFile, Form
import pandas as pd
from pycaret.clustering import setup, create_model, plot_model, pull
from io import BytesIO
from fastapi.responses import JSONResponse
import os
import base64

router = APIRouter()

@router.post("/create-pycaret-clusters")
async def create_pycaret_clusters(
    n_clusters: int = Form(...),
    normalize: bool = Form(...),
    session_id: int = Form(...),
    csv_file: UploadFile = File(...)
):
    try:
        # Leer el archivo CSV recibido en la solicitud
        contents = await csv_file.read()
        df = pd.read_csv(BytesIO(contents), encoding='latin1')

        if df.empty:
            raise HTTPException(status_code=400, detail="El archivo CSV está vacío o no tiene datos válidos")

        # Iniciar la configuración en PyCaret
        setup(df, normalize=normalize, session_id=session_id)

        setup_info_df = pull()

        # Crear modelo de clustering usando el número de clusters proporcionado
        kmeans_model = create_model('kmeans', num_clusters=n_clusters)

        plot_model(kmeans_model, plot='elbow', save=True)
        plot_model(kmeans_model, plot='silhouette', save=True)

        elbow_plot = None
        silhouette_plot = None
        for file in os.listdir():
            if file.startswith("Elbow Plot") and file.endswith(".png"):
                elbow_plot = file
            elif file.startswith("Silhouette Plot") and file.endswith(".png"):
                silhouette_plot = file

        if not elbow_plot or not silhouette_plot:
            raise HTTPException(status_code=500, detail="No se pudieron generar los gráficos")

        # Leer y codificar las imágenes a Base64
        with open(elbow_plot, "rb") as image_file:
            elbow_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        with open(silhouette_plot, "rb") as image_file:
            silhouette_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Eliminar los archivos temporales
        os.remove(elbow_plot)
        os.remove(silhouette_plot)

        # Convertir la tabla en formato JSON
        setup_info_json = setup_info_df.to_json(orient="records")

        # Devolver las imágenes en formato Base64 en la respuesta JSON
        return JSONResponse(content={
            "elbow_plot": elbow_base64,
            "silhouette_plot": silhouette_base64,
            "setup_table": setup_info_json
        })

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(e)}")
