import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import csv
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
import video_library as lib
from tkinter import messagebox as msb
import font_manager as fonts



def set_text(text_area, content):
    text_area.delete('1.0', tk.END)
    text_area.insert(1.0, content)

video_list = {}

def list_all():
    output = ''
    for key, name in video_list.items():

        output += f"{name} \n"
    return output

class VideoPlaylist:
    def __init__(self, window):
        self.window = window
        #self.window.title("Video Playlist App")
        image = Image.open('image/background2.jpg')
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        self.saved_playlists = []
        self.create_widgets()
        fonts.configure()


    def create_widgets(self):
        # Entry widget for entering video numbers
        self.video_number_entry = tk.Entry(self.window)
        self.video_number_entry.grid(row=0, column=0, padx=10, pady=10)

        # Button to add video to the playlist
        add_button = tk.Button(self.window, text="Add to Playlist", command=self.add_to_playlist)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        head_list_playlist = tk.Label(self.window, text='List Play List Saved')
        head_list_playlist.grid(row=0, column=2, columnspan=3)

        self.text_save_list = tk.Text(self.window, height=10, width=30)
        self.text_save_list.grid(row=1, column=2, columnspan=3, rowspan=3, padx=10, pady=10)

        # Text area to display the playlist
        self.playlist_text = tk.Text(self.window, height=10, width=30)
        self.playlist_text.grid(row=1, column=0, columnspan=2, rowspan=3, padx=10, pady=10)

        # Button to play the playlist
        play_button = tk.Button(self.window, text="Play Playlist", command=self.play_playlist)
        play_button.grid(row=4, column=0, pady=10)

        # Button to save the playlist
        save_button = tk.Button(self.window, text="Save Playlist", command=self.save_playlist)
        save_button.grid(row=4, column=1, pady=10)

        # Button to load a saved playlist
        load_button = tk.Button(self.window, text="Load Playlist", command=self.load_playlist)
        load_button.grid(row=5, column=0,pady=10)

        # Button to reset the playlist
        reset_button = tk.Button(self.window, text="Reset Playlist", command=self.reset_playlist)
        reset_button.grid(row=5, column=1, pady=10)

        # Button to delete a saved playlist
        delete_button = tk.Button(self.window, text="Delete Saved Playlist", command=self.delete_playlist)
        delete_button.grid(row=5, column=2, pady=10)

    def add_to_playlist(self):
        try:
            key = self.video_number_entry.get()
            name = lib.get_name(key)

            if name is not None:
                # Ask the user if they want to choose specific episodes
                user_input = askstring("Choose Episodes", "Do you want to choose specific episodes? (yes/no)")
                if user_input is None:
                    # User clicked "Cancel," do nothing
                    return
                if user_input and user_input.lower() == 'yes':
                    # If yes, ask for specific episodes separated by commas

                    episodes_input = askstring("Specify Episodes", "Enter episode numbers:")
                    try:
                        episodes = [int(e.strip()) for e in episodes_input.split(',')]
                        name_episodes = [lib.get_name_episode(key, e) for e in episodes]
                        # Ensure unique video name, and add episodes to the existing set
                        if key not in video_list:
                            video_list[key] = set()

                        video_list[key].update(
                            f'{name}-episode {e}: {name_episode}' for e, name_episode in zip(episodes, name_episodes))
                    except ValueError:
                        msb.showerror('Error', 'Episode number must be an integer > 0')


                elif user_input and user_input.lower() == 'no':
                    # If no, add all episodes
                    video_list[key] = {name}
                else:
                    raise ValueError('Invalid syntax')

                set_text(self.playlist_text, list_all())
        except KeyError as err:
            msb.showerror('Error', str(err))
        except IndexError:
            msb.showerror('Error', 'There is no result')
        except ValueError as v:
            msb.showerror('Error', f'{v}')

    def play_playlist(self):
        try:
            if len(video_list) == 0:
                raise ValueError('There are no videos in the playlist')
            # Increment play count for each video episode in the playlist
            for key, episodes in video_list.items():
                for episode_info in episodes:
                    if '-episode' in episode_info:
                        # Extract episode key and episode number from the formatted string
                        episode_key = key
                        episode_number = (episode_info.split('-episode')[1].split(':')[0])

                        episode_number = int(episode_number)
                        try:
                            lib.increment_play_count_episode(episode_key, episode_number)
                        except KeyError:
                            msb.showerror('Error', f'Invalid number for video {episode_key} - episode {episode_number}')
                    else:
                        lib.increment_play_count(key)
                        item = lib.library_episode[key]
                        for i in range(len(item)):
                            lib.increment_play_count_episode(key, i + 1)
                            # Update the playlist_text with the updated playlist information
                set_text(self.playlist_text, list_all())
                msb.showinfo('Playlist', 'Playlist successfully')
        except ValueError as err:
            msb.showerror('Error', str(err))
        except Exception as e:
            msb.showerror('Error', f'Error playing playlist: {e}')

    def save_playlist(self):
        try:
            if not video_list:
                raise ValueError('The playlist is empty. Add videos to save.')

            # Ask the user for a playlist name
            playlist_name = askstring('Save Playlist', 'Enter a name for the playlist:')
            if playlist_name is not None:
                # Save the playlist to a CSV file with the specified name
                file_path = f"{playlist_name}.csv"
                with open(file_path, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, name in video_list.items():
                        writer.writerow([key, name])

                # Add the playlist name to the list of saved playlists
                self.saved_playlists.append(playlist_name)
                set_text(self.text_save_list, '\n'.join(self.saved_playlists))
                msb.showinfo('Success', f'Playlist "{playlist_name}" saved successfully!')
        except Exception as err:
            msb.showerror('Error', str(err))

    def load_playlist(self):
        try:
            if not self.saved_playlists:
                msb.showinfo('Info', 'No saved playlists available.')
                return
            # Ask the user to choose a playlist
            selected_playlist = askstring('Load Playlist', 'Choose a playlist:',initialvalue=self.saved_playlists[0])
            if selected_playlist is not None and selected_playlist in self.saved_playlists:
                file_path = f"{selected_playlist}.csv"
                video_list.clear()  # Clear existing playlist
                with open(file_path, 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    for row in reader:
                        if len(row) == 2:
                            key, name = row
                            video_list[key] = name
                set_text(self.playlist_text, list_all())
                msb.showinfo('Success', f'Playlist "{selected_playlist}" loaded successfully!')
        except Exception as err:
            msb.showerror('Error', str(err))


    def update_playlist_text(self):
        # Clear the current text and update with the video names in the playlist
        self.playlist_text.delete(1.0, tk.END)
        video_list.clear()

    def reset_playlist(self):
        # Reset the playlist and clear the text area

        self.update_playlist_text()

    def delete_playlist(self):
        try:
            if not self.saved_playlists:
                msb.showinfo('Info', 'No saved playlists available.')
                return

            # Ask the user to choose a playlist to delete
            selected_playlist = askstring('Delete Playlist', 'Choose a playlist to delete:',
                                          initialvalue=self.saved_playlists[0])
            if selected_playlist is not None and selected_playlist in self.saved_playlists:
                # Remove the playlist from the list of saved playlists
                self.saved_playlists.remove(selected_playlist)

                # Update the display of saved playlists
                set_text(self.text_save_list, '\n'.join(self.saved_playlists))
                msb.showinfo('Success', f'Playlist "{selected_playlist}" deleted successfully!')
        except Exception as err:
            msb.showerror('Error', str(err))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('900x400')
    app = VideoPlaylist(root)
    root.mainloop()




