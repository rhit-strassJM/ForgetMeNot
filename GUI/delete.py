import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Function to open and display image from URL using Tkinter
def open_and_display_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            image_data = Image.open(BytesIO(response.content))
            root = tk.Tk()
            root.title("Image Viewer")
            image_label = tk.Label(root)
            image_label.pack()
            photo = ImageTk.PhotoImage(image_data)
            image_label.config(image=photo)
            root.mainloop()
        except Exception as e:
            print(f"Error opening image: {e}")
    else:
        print(f"Failed to retrieve image from URL. Status code: {response.status_code}")

# Example usage:
url = "https://drive.google.com/uc?id=1iHP6vFBFq1IdQ6wsBgNIFtjRIjwgR6Ki"
open_and_display_image(url)
