import argparse
import cv2
import torch
import numpy as np


def crop_center(image):
    # crop the center of an image and matching the height with the width of the image
    shape = image.shape[:-1]
    max_size_index = np.argmax(shape)
    diff1 = abs((shape[0] - shape[1]) // 2)
    diff2 = shape[max_size_index] - shape[1 - max_size_index] - diff1
    return image[:, diff1: -diff2] if max_size_index == 1 else image[diff1: -diff2, :]


def get_dtype():
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = torch.device(dev)
    if dev == 'cuda':
        dtype = torch.cuda.FloatTensor
    else:
        dtype = torch.FloatTensor
    print(f'Using device {device}')
    return dtype


def get_video_properties(video):
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # get videos properties
    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        length = int(video.get(cv2.cv.CAP_PROP_FRAME_COUNT))
        v_width = int(video.get(cv2.cv.CAP_PROP_FRAME_WIDTH))
        v_height = int(video.get(cv2.cv.CAP_PROP_FRAME_HEIGHT))
    else:
        fps = video.get(cv2.CAP_PROP_FPS)
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        v_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        v_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, length, v_width, v_height


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_stickman_line_connection():
    # stic kman line connection with keypoints indices for R-CNN
    line_connection = [
        (7, 9), (7, 5), (10, 8), (8, 6), (6, 5), (15, 13), (13, 11), (11, 12), (12, 14), (14, 16), (5, 11), (12, 6)
    ]
    return line_connection

def plot_cv2_img_using_matplotlib(img):
    
    # Convert the image from BGR to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Display the image
    plt.imshow(image_rgb)
    plt.axis('off')  # Hide axes for a cleaner display
    plt.show()
    
def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def save_video(output_video_frames, output_video_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (output_video_frames[0].shape[1], output_video_frames[0].shape[0]))
    for frame in output_video_frames:
        out.write(frame)
    out.release()