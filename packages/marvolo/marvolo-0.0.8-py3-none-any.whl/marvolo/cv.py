import imageio
import cv2
import os

def video_to_image(video_path, image_folder, type = 'png', stride = 1, clear = True):
    video = imageio.get_reader(video_path)

    os.makedirs(image_folder, exist_ok = True)

    if clear:
        os.system(f'rm -rf {image_folder}')
        os.makedirs(image_folder, exist_ok = True)

    for frame_number, frame_data in enumerate(video):
        if frame_number % stride != 0:
            continue
        imageio.imwrite(os.path.join(image_folder, f'{frame_number}.{type}'), frame_data)
    
    print(f'Total {frame_number + 1} frames, saved {(frame_number + 1) // stride} frames')


