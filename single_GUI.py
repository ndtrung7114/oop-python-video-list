import tkinter as tk
from tkinter import ttk

from create_video_list import VideoPlaylist
from check_videos import CheckVideos
from updates_videos import UpdatesVideos
from add_videos import AddVideoGUI
class VideoPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Video Player")



        # Create a notebook (tabs container)
        self.notebook = ttk.Notebook(window)

        # Create tabs and add them to the notebook

        tab1 = ttk.Frame(self.notebook)
        tab2 = ttk.Frame(self.notebook)
        tab3 = ttk.Frame(self.notebook)
        tab4 = ttk.Frame(self.notebook)


        self.notebook.add(tab1, text="Check Videos")
        self.notebook.add(tab2, text="Create Video List")
        self.notebook.add(tab3, text="Update Videos")
        self.notebook.add(tab4, text='Add Videos')

        

        # Load GUI content for each tab

        CheckVideos(tab1)
        VideoPlaylist(tab2)
        UpdatesVideos(tab3)
        AddVideoGUI(tab4)

        # Pack the notebook to make it visible
        self.notebook.pack(expand=True, fill="both")



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('900x400')
    app = VideoPlayer(root)
    root.mainloop()