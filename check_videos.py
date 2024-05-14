import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox as msb

import tkVideoPlayer
from PIL import Image, ImageTk
import video_library as lib
import font_manager as fonts
from video_library import library_episode

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)


class CheckVideos():
    def __init__(self, window):
        self.window = window

        image = Image.open('image/background1.jpg')
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        search_lbl = tk.Label(self.window, text="Search by Name:")  # create search label
        search_lbl.grid(row=2, column=2, padx=10, pady=10)

        self.search_entry = tk.Entry(self.window, width=20)  # create search entry
        self.search_entry.grid(row=2, column=3, padx=10, pady=10)

        search_btn = tk.Button(self.window, text="Search", command=self.search_clicked)  # create search button
        search_btn.grid(row=2, column=4, padx=10, pady=10)

        view_lbl = tk.Label(self.window, text="View by Director:")  # create view label
        view_lbl.grid(row=3, column=2, padx=10, pady=10)

        self.view_entry = tk.Entry(self.window, width=20)  # create view entry
        self.view_entry.grid(row=3, column=3, padx=10, pady=10)

        view_btn = tk.Button(self.window, text="View", command=self.view_clicked)  # create view button
        view_btn.grid(row=3, column=4, padx=10, pady=10)

        list_videos_btn = tk.Button(self.window, text="List All Videos", command=self.list_videos_clicked)  # create list video button
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10)

        enter_lbl = tk.Label(self.window, text="Enter Video Number")  # create enter number video label
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.input_entry = tk.Entry(self.window, width=3)  # create input entry
        self.input_entry.grid(row=0, column=2, padx=10, pady=10)

        check_video_btn = tk.Button(self.window, text="Check Video", command=self.check_video_clicked)  # create check video button
        check_video_btn.grid(row=0, column=3, padx=10, pady=10)

        self.list_txt = tkst.ScrolledText(self.window, width=50, height=12, wrap="none")  # create list video text to display all video and episode
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.video_txt = tk.Text(self.window, width=24, height=4, wrap="none") # create video text to display information about video
        self.video_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=20)

        #unresolved
        # self.video_player = tkVideoPlayer.TkinterVideo(self.window, width=20, height=12)
        # self.video_player.grid(row=1, column=5, columnspan=3, padx=10, pady=10)
        # self.video_player.set_size((200, 200))

        self.status_lbl = tk.Label(self.window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        self.list_videos_clicked()
        fonts.configure()

    def display_video(self, video_path):
        try:
            # Remove any existing video player widget
            if hasattr(self, 'video_player'):
                self.video_player.destroy()
            # Video player widget
            video_player = tkVideoPlayer.TkinterVideo(self.window)
            video_player.grid(row=1, column=5, columnspan=3, padx=10, pady=10)
            video_player.set_size((200, 200))
            video_player.load(video_path)
            video_player.play()

        except Exception as e:
            # Handle any errors that may occur during video loading
            msb.showerror('Error', f"Error loading video: {str(e)}")

    def search_clicked(self):
        search_term = self.search_entry.get().lower()
        if search_term is not None:

            results = lib.search_by_name(search_term)

            if results:
                set_text(self.list_txt, results)
                self.status_lbl.configure(text=f"Search results for '{search_term}':")
            else:
                set_text(self.list_txt, "No matching results.")
                self.status_lbl.configure(text=f"No results found for '{search_term}'.")

    def view_clicked(self):
        search_term = self.view_entry.get().lower()
        if search_term is not None:

            results = lib.view_by_director(search_term)

            if results:
                set_text(self.list_txt, results)
                self.status_lbl.configure(text=f"Search results for '{search_term}':")
            else:
                set_text(self.list_txt, "No matching results.")
                self.status_lbl.configure(text=f"No results found for '{search_term}'.")



    def remove_image_label(self):
        # Remove the existing image label
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Label) and hasattr(widget, 'image'):
                widget.destroy()

    def remove_video_label(self):
        # Remove the existing image label
        for widget in self.window.winfo_children():
            if isinstance(widget, tkVideoPlayer.TkinterVideo) and hasattr(widget, 'video_player'):
                widget.destroy()

    # Function to display an image in a label
    def display_image(self, image_path):
        try:
            image = Image.open(image_path)  # open image
            image = image.resize((200, 200), Image.ANTIALIAS)  # resize image
            photo = ImageTk.PhotoImage(image)  # Convert the image to a PhotoImage

            # Create a label to display the image
            image_label = tk.Label(self.window, image=photo)
            image_label.image = photo
            # Grid placement of the image label in the window
            image_label.grid(row=1, column=4, sticky="W", padx=10, pady=10)

        except Exception as e:
            # Handle any errors that may occur during image loading
            msb.showerror('Error', f"Error displaying image: {str(e)}")

    # Function to handle the "Check Video" button click
    def check_video_clicked(self):
        try:
            # Get the video key from the input text entry
            key = self.input_entry.get()
            # Retrieve video details using the library functions
            name = lib.get_name(key)
            if name is not None:
                director = lib.get_director(key)
                rating = lib.get_rating(key)
                play_count = lib.get_play_count(key)
                # Format the video details
                video_details = f"{name}\n{director}\nrating: {rating}\nplays: {play_count}"
                # Check if the video key is in the episode library
                if key in library_episode:
                    # Get episode details and update text areas
                    video_details_episode = lib.list_episode(key)
                    if video_details_episode:
                        set_text(self.video_txt, video_details)
                        set_text(self.list_txt, video_details_episode)
                    else:
                        set_text(self.video_txt, video_details)
                        set_text(self.list_txt, "")
                else:
                    # Handle the case when library_episode doesn't have an entry for the key
                    set_text(self.video_txt, video_details)
                    set_text(self.list_txt, "No episode information available.")
                video_path = lib.get_video_path(key)
                if video_path:
                    self.display_video(video_path)

                else:
                    self.remove_video_label()
                # Get the image path for the video key
                image_path = lib.get_image_path(key)

                # Display the image if available, otherwise remove the image label
                if image_path:
                    self.display_image(image_path)
                else:
                    self.remove_image_label()
        except KeyError as err:
            # Handle KeyError (e.g., if the video key is not found)
            msb.showerror('Error', str(err))
            self.status_lbl.configure(text="Check Video button was clicked!")

    def list_videos_clicked(self):
        video_list = lib.list_all()
        set_text(self.list_txt, video_list)
        self.status_lbl.configure(text="List Videos button was clicked!")



