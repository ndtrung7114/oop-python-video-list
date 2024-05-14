import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
from tkinter import messagebox as msb
from video_library import *
import font_manager as fonts

dict_episode = {}


class AddVideoGUI:
    def __init__(self, window):
        self.window = window

        #self.window.title("Add New Video")
        # Open the image with Pillow and convert it to PhotoImage
        image = Image.open('image/background4.jpg')
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        self.create_widgets()
        # Bind the resize function to window resize events
        fonts.configure()



    def create_widgets(self):

        # Labels and Entry widgets for video details
        lbl_title = tk.Label(self.window, text="Title:") # create a title/name video label
        lbl_title.grid(row=0, column=0, padx=10, pady=5)

        self.title_entry = tk.Entry(self.window) # create title/name entry
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        lbl_director = tk.Label(self.window, text="Director:") # create label director
        lbl_director.grid(row=1, column=0, padx=10, pady=5)

        self.director_entry = tk.Entry(self.window)  # create director entry
        self.director_entry.grid(row=1, column=1, padx=10, pady=5)

        lbl_rating = tk.Label(self.window, text="Rating:") # create label rating
        lbl_rating.grid(row=2, column=0, padx=10, pady=5)

        self.rating_entry = ttk.Combobox(self.window, values=[1, 2, 3, 4, 5], state="readonly") # create rating entry
        self.rating_entry.grid(row=2, column=1, padx=10, pady=5)
        #self.rating_entry.set(3)  # Default rating value

        lbl_imgpath = tk.Label(self.window, text='ImagePath: ') # create label image path label
        lbl_imgpath.grid(row=3, column=0, padx=10, pady=10)

        self.imgpath_entry = tk.Entry(self.window) # create image path entry
        self.imgpath_entry.grid(row=3, column=1, padx=10, pady=10)
        default_img_path = 'image/'  # set default value for image path
        self.imgpath_entry.insert(0, default_img_path)
        # Bind an event to prevent deletion of the default string
        self.imgpath_entry.bind('<Key>', lambda e: self.prevent_delete(e, default_img_path))

        lbl_videopath = tk.Label(self.window, text='VideoPath: ') # set label video path
        lbl_videopath.grid(row=4, column=0, padx=10, pady=10)

        self.videopath_entry = tk.Entry(self.window) # set video path entry
        self.videopath_entry.grid(row=4, column=1, padx=10, pady=10)
        # Set default value for video_path entry
        default_video_path = 'video/' # set default value for video path
        self.videopath_entry.insert(0, default_video_path)
        # Bind an event to prevent deletion of the default string
        self.videopath_entry.bind('<Key>', lambda e: self.prevent_delete(e, default_video_path))

        tk.Label(self.window, text="Quantity Episodes:").grid(row=5, column=0, padx=10, pady=5) # set quantity episodes label
        self.quantity_episode_entry = tk.Entry(self.window)
        self.quantity_episode_entry.grid(row=5, column=1, padx=10, pady=5)

        add_button = tk.Button(self.window, text="Add Video", command=self.add_video) # set add button
        add_button.grid(row=6, column=0, columnspan=2, pady=10)

    # this function was create to prevent if user delete video's path or image's path
    def prevent_delete(self, event, default_value):
        if self.imgpath_entry.get() == default_value or self.videopath_entry.get() == default_value:
            if event.keysym in ['BackSpace', 'Delete']:
                return 'break'
        return None

    # Function to handle adding a new video
    def add_video(self):
        try:
            # Get user-input values from entry widgets
            title = self.title_entry.get()
            director = self.director_entry.get()
            rating = self.rating_entry.get()
            img_path = self.imgpath_entry.get()
            video_path = self.videopath_entry.get()

            # Check if the entered paths are equal to the default values and update them
            img_path = '' if img_path == 'image/' else img_path
            video_path = '' if video_path == 'video/' else video_path

            # Create a LibraryItem object with the entered information
            item = LibraryItem(title, director, rating, img_path, video_path)

            # Validate and get the quantity of episodes
            quantity_video_str = self.quantity_episode_entry.get()
            if not quantity_video_str.isdigit() or int(quantity_video_str) < 0:
                raise ValueError("Please enter a non-negative integer for the Episode Number.")

            quantity_video = int(self.quantity_episode_entry.get())

            # Generate a new video number and enter new episodes for the video
            video_number = '0' + str(len(library) + 1)
            list_episode = self.enter_new_episode(quantity_video)
            # Ensure if video has episode, user have type full information about episode
            if list_episode != None:
                dict_episode[video_number] = list_episode
                self.save_episode_to_csv(dict_episode)
                # Save the new item to a CSV file
                self.save_video_to_csv(item)

                # Display information about the added video
                msb.showinfo('Video Added', f'Added Video:\n{item.info()}')

            # You can add the item to your system (e.g., update a database) here

        except Exception as err:
            # Handle any general exceptions
            msb.showerror('Error', str(err))
        except ValueError as v:
            # Handle specific ValueError (e.g., invalid input)
            msb.showerror('Error', str(v))

    def save_episode_to_csv(self, dict_episode):
        with open('episodes.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)


            for video_number, episodes in dict_episode.items():
                for episode in episodes:
                    csv_writer.writerow(
                        [video_number, episode.name, episode.director, episode.rating, episode.episode_number,
                         episode.image_path, episode.video_path])

    def save_video_to_csv(self, item):
        try:
            # open 'video.csv' with mode append to write new information
            with open('video.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # write on CSV file has columns: Name,Director,episodes,Rating,ImagePath
                writer.writerow([item.name, item.director, item.rating, item.image_path, item.video_path])
        except Exception as err:
            msb.showerror('Error', f'Failed to save to CSV: {str(err)}')

    def enter_new_episode(self, quantity):
        list_episode = []
        for i in range(quantity):
            name = simpledialog.askstring("Input", f"Enter name for Episode {i + 1}:")
            if name == '' or name is None:  # User clicked "Cancel" or entered an empty string
                return None

            director = simpledialog.askstring("Input", f"Enter director for Episode {i + 1}:")
            if director == '' or director is None:  # User clicked "Cancel" or entered an empty string
                return None

            rating = simpledialog.askinteger("Input", f"Enter rating for Episode {i + 1}:")
            if rating is None:  # User clicked "Cancel"
                return None

            episode_number = simpledialog.askinteger("Input", f"Enter episode number for Episode {i + 1}:")
            if episode_number is None:  # User clicked "Cancel"
                return None

            episode = LibraryItemEpisode(name, director, rating, episode_number)
            list_episode.append(episode)

        return list_episode


