def save_plot_as_base64(file_name: str) -> str:
    """Lee un archivo de imagen y lo convierte a Base64."""
    with open(file_name, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
