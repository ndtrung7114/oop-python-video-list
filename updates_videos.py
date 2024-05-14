import tkinter as tk
import font_manager as fonts
import video_library as lib
from tkinter import messagebox as msb
from video_library import library_episode
from PIL import Image, ImageTk

class UpdatesVideos:
    def __init__(self, window):
        self.window = window
        image = Image.open('image/background3.jpg')
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        # Labels for Video Information
        enter_number = tk.Label(self.window, text='Enter Video Number')
        enter_number.grid(row=0, column=0, padx=10, pady=10)

        lbl_name_video = tk.Label(self.window, text='Name Video')
        lbl_name_video.grid(row=0, column=2, padx=10, pady=10)

        lbl_director_video = tk.Label(self.window, text='Director Video')
        lbl_director_video.grid(row=1, column=2, padx=10, pady=10)

        lbl_rating_video = tk.Label(self.window, text='Rating Video')
        lbl_rating_video.grid(row=2, column=2, padx=10, pady=10)

        lbl_imgpath_video = tk.Label(self.window, text='ImagePath Video')
        lbl_imgpath_video.grid(row=3, column=2, padx=10, pady=10)

        lbl_videopath = tk.Label(self.window, text='VideoPath Video')
        lbl_videopath.grid(row=4, column=2, padx=10, pady=10)

        # Entry Widgets for Video Information
        self.number_video_entry = tk.Entry(self.window, width=5)
        self.number_video_entry.grid(row=0, column=1)

        self.name_video_entry = tk.Entry(self.window, width=20)
        self.name_video_entry.grid(row=0, column=3, padx=10, pady=10)

        self.video_director_entry = tk.Entry(self.window, width=20)
        self.video_director_entry.grid(row=1, column=3, padx=10, pady=10)

        self.video_rating_entry = tk.Entry(self.window, width=20)
        self.video_rating_entry.grid(row=2, column=3, padx=10, pady=10)

        self.video_imgpath_entry = tk.Entry(self.window, width=20)
        self.video_imgpath_entry.grid(row=3, column=3, padx=10, pady=10)

        self.videopath_video_entry = tk.Entry(self.window, width=20)
        self.videopath_video_entry.grid(row=4, column=3, padx=10, pady=10)

        # Labels for Episode Information
        lbl_episode = tk.Label(self.window, text='Episodes')
        lbl_episode.grid(row=0, column=4, padx=10, pady=5)

        lbl_name_episode = tk.Label(self.window, text='Name Episode')
        lbl_name_episode.grid(row=5, column=4, padx=10, pady=10)

        lbl_rating_episode = tk.Label(self.window, text='Rating Episode')
        lbl_rating_episode.grid(row=6, column=4, padx=10, pady=10)

        # Listbox for Episodes
        self.lst_episode = tk.Listbox(self.window, width=55)
        self.lst_episode.grid(row=1, column=4, columnspan=3, rowspan=4, padx=10, pady=10)
        self.lst_episode.bind("<<ListboxSelect>>", self.display_selected_episode)

        # Entry Widgets for Episode Information
        self.name_episode_entry = tk.Entry(self.window, width=20)
        self.name_episode_entry.grid(row=5, column=5, padx=10, pady=10)

        self.rating_episode_entry = tk.Entry(self.window, width=20)
        self.rating_episode_entry.grid(row=6, column=5, padx=10, pady=10)

        # Buttons to trigger video update and check
        btn_update = tk.Button(self.window, text='Update', command=self.update_video)
        btn_update.grid(row=2, column=0, padx=(0, 10))

        btn_check = tk.Button(self.window, text='Check', command=self.check_video)
        btn_check.grid(row=2, column=1, padx=(10, 0))

        btn_update_episode = tk.Button(self.window, text='Update Episode', command=self.update_episode)
        btn_update_episode.grid(row=3, column=0, padx=(0, 10))

        fonts.configure()
    def display_selected_episode(self, event):
        try:
            selected_index = self.lst_episode.curselection()
            if selected_index:
                selected_episode_info = self.lst_episode.get(selected_index)

                # Check if the selected item is the special message
                if selected_episode_info != "This video has no episodes":
                    video_number = self.number_video_entry.get()

                    # Extract episode number from the selected item
                    split_info = selected_episode_info.split(":")[0].strip()

                    # Ensure episode_number is not empty before converting to integer
                    episode_number = ''.join(filter(str.isdigit, split_info))
                    if episode_number:
                        episode_number = int(episode_number)

                        selected_episode_info = self.get_episode_info_after_check(video_number, episode_number)

                        # Display episode information in text entries
                        self.name_episode_entry.delete(0, tk.END)
                        self.name_episode_entry.insert(0, selected_episode_info["name"])

                        self.rating_episode_entry.delete(0, tk.END)
                        self.rating_episode_entry.insert(0, str(selected_episode_info["rating"]))

        except Exception as e:
            msb.showerror("Error", str(e))

    def get_episode_info_after_check(self, video_number, episode_number):
        try:
            name = lib.get_name_episode(video_number, episode_number)
            rating = lib.get_rating_episode(video_number, episode_number)

            episode_info = {
                "name": name,
                "rating": rating,
            }
            return episode_info
        except KeyError:
            raise ValueError(f"Episode not found with video number: {video_number} and episode number: {episode_number}")

    # Function to handle checking video information
    def check_video(self):
        try:
            # Get the video number from the entry widget
            video_number = self.number_video_entry.get()

            # Retrieve video information using the get_video_info method
            video_info = self.get_video_info(video_number)

            # Display video information in text entries
            self.name_video_entry.delete(0, tk.END)
            self.name_video_entry.insert(0, video_info["name"])

            self.video_director_entry.delete(0, tk.END)
            self.video_director_entry.insert(0, video_info["director"])

            self.video_rating_entry.delete(0, tk.END)
            self.video_rating_entry.insert(0, str(video_info["rating"]))

            self.video_imgpath_entry.delete(0, tk.END)
            self.video_imgpath_entry.insert(0, video_info["image_path"])

            self.videopath_video_entry.delete(0, tk.END)
            self.videopath_video_entry.insert(0, video_info["video_path"])

            # Display episode information in listbox if episodes exist
            episode_info = self.get_episode_info(video_number)

            self.lst_episode.delete(0, tk.END)
            if episode_info == 'This video have no episodes':
                # Display a message in the listbox if there are no episodes
                self.lst_episode.insert(tk.END, episode_info)
            else:
                # Display each episode in the listbox
                for episode in episode_info:
                    self.lst_episode.insert(tk.END, episode)

        except ValueError as v:
            # Handle ValueError (e.g., if the video number is not valid)
            msb.showerror("Error", str(v))

    def get_video_info(self, video_number):
        try:
            name = lib.get_name(video_number)
            director = lib.get_director(video_number)
            rating = lib.get_rating(video_number)
            image_path = lib.get_image_path(video_number)
            video_path = lib.get_video_path(video_number)

            video_info = {
                "name": name,
                "director": director,
                "rating": rating,
                "image_path": image_path,
                "video_path": video_path,
            }
            return video_info
        except KeyError:
            raise ValueError(f"Video not found with number: {video_number}")

    def get_episode_info(self, video_number):

        if video_number in library_episode:
            episode_info = lib.list_episode(video_number)
            return episode_info.split("\n")  # Assuming the list_episode returns a string
        else:
            return 'This video have no episodes'

    def update_video(self):

        try:
            key = self.number_video_entry.get()
            new_rate = self.video_rating_entry.get()
            new_name = self.name_video_entry.get()
            new_director = self.video_director_entry.get()

            name = lib.get_name(key)
            if name is not None:
                lib.set_rating(key, new_rate)
                lib.set_name(key, new_name)
                lib.set_director(key, new_director)
                play_count = lib.get_play_count(key)
                msb.showinfo(f'Video number {key} - {name}', f'Rate: {new_rate} \n Play count: {play_count}\n ')
        except KeyError as err:
            msb.showerror('Error', str(err))
        except ValueError as err:
            msb.showerror('Error', str(err))

    def update_episode(self):

        try:

            selected_index = self.lst_episode.curselection()
            if selected_index:
                video_number = self.number_video_entry.get()
                selected_episode_info = self.lst_episode.get(selected_index)
                split_info = selected_episode_info.split(":")[0].strip()

                # Extract the numeric part from the split_info
                episode_number = ''.join(filter(str.isdigit, split_info))
                episode_number = int(episode_number)

                new_name = self.name_episode_entry.get()
                new_rate_episode = self.rating_episode_entry.get()
                new_rate_episode = int(new_rate_episode)

                # Update the specific item in the listbox
                updated_episode_info = f"{episode_number}: {new_name} - Rating: {new_rate_episode}"
                self.lst_episode.delete(selected_index)
                self.lst_episode.insert(selected_index, updated_episode_info)

                # Update the library data
                lib.set_name_episode(video_number, episode_number, new_name)
                lib.set_rating_episode(video_number, episode_number, new_rate_episode)

                # Refresh the listbox by calling check_video again
                self.check_video()
                msb.showinfo('Update', 'Update successfully')
            else:
                msb.showwarning('Warning', 'You are not selecting any episode')



        except Exception:
            msb.showerror("Error", 'Invalid action')




