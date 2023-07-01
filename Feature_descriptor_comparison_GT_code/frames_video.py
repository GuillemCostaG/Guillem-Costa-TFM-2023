import estudi_descriptors
import os
import cv2

def extract_frames_from_video(video_path, output_folder):
    # Crea la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Abre el video
    video = cv2.VideoCapture(video_path)
    frame_count = 0

    # Lee los frames del video
    while True:
        success, frame = video.read()

        frame=estudi_descriptors.resize_bordes(frame)

        # Si no se puede leer el siguiente frame, se sale del bucle
        if not success:
            break

        # Guarda el frame en la carpeta de salida
        output_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(output_path, frame)

        frame_count += 1

    # Cierra el video
    video.release()

    print(f"Se han guardado {frame_count} frames en la carpeta {output_folder}.")

# Ejemplo de uso
video_path = "video/30s.mp4"
output_folder = "video/frames"
extract_frames_from_video(video_path, output_folder)