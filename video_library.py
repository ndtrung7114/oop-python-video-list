# Import necessary modules
from library_item import LibraryItem, LibraryItemEpisode
import csv

# Function to load video library from a CSV file
def load_video_library(file_path):
    library = {}

    # Open the CSV file for reading
    with open(file_path, 'r', encoding='utf-8') as f:
        # Create a CSV reader
        reader = csv.reader(f)
        # Skip the header row
        next(reader)

        # Initialize an index counter
        now_index = 1
        # Iterate through rows in the CSV file
        for row in reader:
            i = now_index
            # Create a LibraryItem and add it to the library
            library['0' + str(i)] = LibraryItem(row[0], row[1], row[2], row[3], row[4])
            now_index += 1

    # Return the loaded library
    return library

# Function to load episode library from a CSV file
def load_episode_library(file_path):
    library_episode = {}

    # Open the CSV file for reading
    with open(file_path, 'r') as csvfile:
        # Create a CSV reader
        csv_reader = csv.reader(csvfile)
        # Skip the header row
        headers = next(csv_reader)

        # Iterate through rows in the CSV file
        for row in csv_reader:
            # Extract data from the row
            video_number = row[0]
            name = row[1]
            director = row[2]
            rating = int(row[3])
            episode_number = int(row[4])
            image_path = row[5]
            video_path = row[6]

            # Check if video number is already in the library
            if video_number not in library_episode:
                library_episode[video_number] = []

            # Create a LibraryItemEpisode and add it to the episode library
            library_episode[video_number].append(
                LibraryItemEpisode(name, director, rating, episode_number, image_path, video_path)
            )

    # Return the loaded episode library
    return library_episode

# Hardcoded file names for video and episode libraries
video_library_file = 'video.csv'
episode_library_file = 'episodes.csv'

# Load video and episode libraries
library = load_video_library(video_library_file)
library_episode = load_episode_library(episode_library_file)

# Function to list all video items in the library
def list_all():
    # Load the video library
    library = load_video_library(video_library_file)
    output = ""
    # Iterate through items in the library and concatenate information to the output string
    for key in library:
        item = library[key]
        output += f"{key} {item.info()}\n"
    return output

# Function to list all episodes for a given video
def list_episode(video_number):
    # Load the episode library
    library_episode = load_episode_library(episode_library_file)
    output = ''
    # Iterate through episodes for the given video and concatenate information to the output string
    for episode in library_episode[video_number]:
        output += f'{episode.info()}\n'
    return output

# Function to get the name of a video by its key
def get_name(key):
    # Load the video library
    library = load_video_library('video.csv')
    try:
        # Get the video item and return its name
        item = library[key]
        return item.name
    except KeyError:
        raise KeyError(f'Can not find video with number: {key}')

# Function to set the name of a video by its key
def set_name(key, value):
    # Load the video library
    library = load_video_library('video.csv')
    try:
        # Get the video item and update its name
        item = library[key]
        item.name = value
    except KeyError:
        raise KeyError(f'Can not find video with number: {key}')

# Function to set the name of an episode for a given video and episode number
def set_name_episode(video_number, number_episode, value):
    # Load the episode library
    library_episode = load_episode_library(episode_library_file)
    try:
        # Get the list of episodes for the given video
        item = library_episode[video_number]
        # Check if the episode number is valid
        if number_episode < 1:
            raise ValueError('There are no results')
        # Update the name of the specified episode
        item[number_episode - 1].name = value
    except KeyError:
        raise KeyError(f'Can not find video with number: {video_number}')
    except ValueError:
        raise ValueError('There is no result with this episode')

# Function to get the name of an episode for a given video and episode number
def get_name_episode(video_number, number_episode):
    # Load the episode library
    library_episode = load_episode_library(episode_library_file)
    try:
        # Get the list of episodes for the given video
        item = library_episode[video_number]
        # Check if the episode number is valid
        if number_episode < 1:
            raise ValueError('There are no results')
        # Get the name of the specified episode
        name_episode = item[number_episode - 1].name
        return name_episode
    except KeyError:
        raise KeyError(f'Can not find video with number: {video_number}')

# Function to get the director of a video by its key
def get_director(key):
    # Load the video library
    library = load_video_library('video.csv')
    try:
        # Get the video item and return its director
        item = library[key]
        return item.director
    except KeyError:
        raise KeyError(f'Can not find director with number: {key}')

# Function to set the director of a video by its key
def set_director(key, value):
    # Load the video library
    library = load_video_library('video.csv')
    try:
        # Get the video item and update its director
        item = library[key]
        item.director = value
    except KeyError:
        raise KeyError(f'Can not find video with number: {key}')

# Function to get the director of a video episode by its key
def get_director_episode(key):
    # Load the video library
    library = load_video_library(video_library_file)
    try:
        # Get the video item and return its director
        item = library[key]
        return item.director
    except KeyError:
        raise KeyError(f'Can not find director with number: {key}')

# Function to set the director of an episode for a given video and episode number
def set_director_episode(video_number, number_episode, value):
    # Load the episode library
    library_episode = load_episode_library(episode_library_file)
    try:
        # Get the list of episodes for the given video
        item = library_episode[video_number]
        # Check if the episode number is valid
        if number_episode < 1:
            raise ValueError('There are no results')
        # Update the director of the specified episode
        item[number_episode - 1].director = value
    except KeyError:
        raise KeyError(f'Can not find video with number: {video_number}')
    except ValueError:
        raise ValueError('There is no result with this episode')

# Function to get the rating of a video by its key
def get_rating(key):
    # Load the video library
    library = load_video_library('video.csv')
    try:
        # Get the video item and return its rating
        item = library[key]
        return item.rating
    except KeyError:
        raise KeyError('Invalid number')

# Function to get the rating of an episode for a given video and episode number
def get_rating_episode(video_number, number_episode):
    # Load the episode library
    library_episode = load_episode_library(episode_library_file)
    try:
        # Get the list of episodes for the given video
        item = library_episode[video_number]
        # Get the rating of the specified episode
        rating_episode = item[number_episode - 1].rating
        return rating_episode
    except KeyError:
        raise KeyError('Invalid number')

# Function to update the CSV file with video library information
def update_csv():
    # Load the video library
    library = load_video_library('video.csv')
    # Open the CSV file for writing
    with open('video.csv', 'w', newline='', encoding='utf-8') as f:
        # Create a CSV writer
        writer = csv.writer(f)
        # Write the header row
        writer.writerow(['Name', 'Director', 'Rating', 'ImagePath', 'VideoPath'])
        # Iterate through items in the library and write them to the CSV file
        for key in library:
            item = library[key]
            writer.writerow([item.name, item.director, item.rating, item.image_path, item.video_path])

# Function to set the rating of a video by its key
def set_rating(key, rating):
    # Load the video library
    library = load_video_library('video.csv')
    try:
        # Convert the rating to an integer
        rating = int(rating)
        # Check if the rating is within the valid range
        if rating <= 0 or rating > 5:
            raise ValueError('Rating must be in the range of 1 to 5')

        try:
            # Get the video item and update its rating
            item = library[key]
            item.rating = rating
            # Update the CSV file with the new information
            update_csv()
        except KeyError:
            raise KeyError('Invalid number')

    except ValueError:
        raise ValueError('Rating must be an integer number and in range(1,5)')

# Function to set the rating of an episode for a given video and episode number
def set_rating_episode(number_video, number_episode, rating):
    # Load the episode library
    library_episode = load_episode_library(episode_library_file)
    try:
        # Convert the rating to an integer
        if rating <= 0 or rating > 5:
            raise ValueError('Rating must be in the range of 1 to 5')

        # Get the list of episodes for the given video
        item = library_episode[number_video]
        # Check if the episode number is valid
        if number_episode < 1:
            raise ValueError('There are no results')
        # Update the rating of the specified episode
        item[number_episode - 1].rating = rating
        # Open the episode library CSV file for writing
        with open('episodes.csv', 'w', newline='') as csvfile:
            # Create a CSV writer
            csv_writer = csv.writer(csvfile)
            # Write the header row
            csv_writer.writerow(['VideoNumber', 'Name', 'Director', 'Rating', 'Episode Number', 'Image Path', 'VideoPath'])
            # Iterate through videos and episodes, writing them to the CSV file
            for video_number, episodes in library_episode.items():
                for episode in episodes:
                    csv_writer.writerow(
                        [video_number, episode.name, episode.director, episode.rating, episode.episode_number,
                         episode.image_path, episode.video_path])

    except KeyError:
        raise KeyError('Invalid number')
    except ValueError:
        raise ValueError('Rating must be an integer number and in range(1,5)')

# Function to get the play count of a video by its key
def get_play_count(key):
    # Load the video library
    library = load_video_library('video.csv')
    try:
        # Get the video item and return its play count
        item = library[key]
        return item.play_count
    except KeyError:
        raise KeyError('Invalid number')

# Function to get play count for a specific episode
def get_play_count_episode(video_number, number_episode):
    # Load the episode library from a file
    library_episode = load_episode_library(episode_library_file)

    # Try to access the episode information
    try:
        item = library_episode[video_number]
        # Check if the episode number is valid
        if number_episode < 1:
            raise ValueError('There are no result')
        # Retrieve the play count for the specified episode
        play_count_episode = item[number_episode - 1].play_count

        return play_count_episode
    except KeyError:
        raise KeyError('Invalid number')


# Function to increment play count for a video
def increment_play_count(key):
    # Load the video library from a CSV file
    library = load_video_library('video.csv')

    # Try to access the video information
    try:
        item = library[key]
        # Increment the play count for the video
        item.play_count += 1
    except KeyError:
        raise KeyError('Invalid number')


# Function to increment play count for a specific episode
def increment_play_count_episode(video_number, number_episode):
    # Load the episode library from a file
    library_episode = load_episode_library(episode_library_file)
    # Try to access the episode information
    try:
        item = library_episode[video_number]
        # Check if the episode number is valid
        if number_episode < 1:
            raise ValueError('There are no result')
        # Increment the play count for the specified episode
        item[number_episode - 1].play_count += 1
    except KeyError:
        raise KeyError('Invalid number')


# Function to get the image path for a video
def get_image_path(key):
    # Load the video library from a CSV file
    library = load_video_library('video.csv')
    # Try to access the video information
    try:
        item = library[key]
        # Return the image path for the video
        return item.image_path
    except KeyError:
        raise KeyError(f'Can not found image path for video with number: {key}')


# Function to get the video path for a video
def get_video_path(key):
    # Load the video library from a CSV file
    library = load_video_library('video.csv')
    # Try to access the video information
    try:
        item = library[key]
        # Return the video path for the video
        return item.video_path
    except KeyError:
        raise KeyError(f'Can not found video path for video with number: {key}')


# Function to search videos by name
def search_by_name(search_term):
    # Load the video library from a CSV file
    library = load_video_library('video.csv')

    # Initialize an empty list to store search results
    results = []

    # Iterate through the library
    for key in library:
        # Get the video item using the key
        item = library[key]
        # Check if the search term is present in the lowercase name of the video
        if search_term in item.name.lower():
            # Append the formatted result to the list
            results.append(f"{key} {item.info()}")

    # Join the results into a string with newline characters and return
    return "\n".join(results)


# Function to view videos by director
def view_by_director(search_term):
    # Load the video library from a CSV file
    library = load_video_library('video.csv')

    # Initialize an empty list to store search results
    results = []

    # Iterate through the library
    for key in library:
        # Get the video item using the key
        item = library[key]
        # Check if the search term is present in the lowercase director name of the video
        if search_term in item.director.lower():
            # Append the formatted result to the list
            results.append(f"{key} {item.info()}")

    # Join the results into a string with newline characters and return
    return "\n".join(results)





