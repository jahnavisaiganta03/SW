# -*- coding: utf-8 -*-
"""SmartWatch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14ELWiv--w_jfDnNaJkWMrSB-DcRgyxRg
"""

from google.colab import drive
drive.mount('/content/drive')

import cv2
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
from IPython.display import display, Image

video_path = '/content/drive/MyDrive/1705951007967.mp4'
vid = cv2.VideoCapture(video_path)

# Parameters for connected components
connectivity = 4  # or use 8 for 8-connected components
output_stats = True

# Parameters for frequency analysis
fps = vid.get(cv2.CAP_PROP_FPS)
num_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

# Function to apply FFT and identify frequency components
def identify_frequency_components(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    f_transform = fft(gray_frame)

    # Compute the amplitude spectrum
    amplitude_spectrum = np.abs(f_transform)

    # Compute the frequencies corresponding to the components
    frequencies = np.fft.fftfreq(len(amplitude_spectrum), 1 / fps)

    # Find components with frequency in the range 0-1 Hz
    relevant_indices = np.where((frequencies >= 0) & (frequencies <= 1))[0]
    relevant_amplitudes = amplitude_spectrum[relevant_indices]

    # Thresholding or other logic to identify relevant components
    threshold = 1  # Adjust as needed
    relevant_components = np.where(relevant_amplitudes > threshold)[0]

    return relevant_components

# Process each frame in the video
while True:
    ret, frame = vid.read()
    if not ret:
        break

    # Identify frequency components in the current frame
    relevant_components = identify_frequency_components(frame)

    # Highlight relevant components in the frame
    frame_highlighted = frame.copy()
    frame_highlighted[:, :, 1][relevant_components] = 255  # Highlight in green

    # Find connected components based on identified indices
    _, labeled_frame = cv2.connectedComponents(np.zeros_like(frame[:, :, 0], dtype=np.uint8), connectivity=connectivity)
    labeled_frame[relevant_components] = 255  # Highlight relevant components

    # Convert BGR to RGB for display
    frame_rgb = cv2.cvtColor(frame_highlighted, cv2.COLOR_BGR2RGB)

    # Display the frame using IPython.display
    display(Image(data=cv2.imencode('.png', frame_rgb)[1]))

    if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to exit
        break

vid.release()
cv2.destroyAllWindows()