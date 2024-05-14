from library_item import LibraryItem, LibraryItemEpisode  # Replace 'your_module_name' with the actual module name

def test_valid_library_item():
    item = LibraryItem('Movie1', 'Director1', 4)
    assert item.name == 'Movie1'
    assert item.director == 'Director1'
    assert item.rating == 4
    assert item.play_count == 0
    assert item.image_path is None
    assert item.video_path is None

def test_empty_name_raises_value_error():
    try:
        item = LibraryItem('', 'Director1', 3)
        assert False
    except ValueError as e:
        assert str(e) == 'Name can not be empty'


def test_empty_director_raises_value_error():
    try:
        item = LibraryItem('Movie1', '', 3)
        assert False
    except ValueError as e:
        assert str(e) == 'Director can not be empty'

def test_non_integer_rating_raises_value_error():
    try:
        item = LibraryItem('Movie1', 'Director1', 'four')
        assert False
    except ValueError as e:
        assert str(e) == 'Rating must be integer number'

def test_invalid_rating_range_raises_value_error():
    try:
        item = LibraryItem('Movie1', 'Director1', 7)
        assert False
    except ValueError as e:
        assert str(e) == 'Rating must be in range(1, 5)'

def test_valid_library_item_info():
    item = LibraryItem('Movie1', 'Director1', 4)
    assert item.info() == 'Movie1 - Director1 ****'

def test_valid_library_item_stars():
    item = LibraryItem('Movie1', 'Director1', 3)
    assert item.stars() == '***'

def test_valid_episode():
    episode = LibraryItemEpisode('Episode1', 'Director1', 4, 1)
    assert episode.name == 'Episode1'
    assert episode.director == 'Director1'
    assert episode.rating == 4
    assert episode.play_count == 0
    assert episode.image_path is None
    assert episode.video_path is None
    assert episode.episode_number == 1

def test_valid_episode_info():
    episode = LibraryItemEpisode('Episode1', 'Director1', 4, 1)
    assert episode.info() == 'Episode1: Episode1 -  0 - ****'

def test_valid_episode_info_with_play_count():
    episode = LibraryItemEpisode('Episode1', 'Director1', 4, 1)
    episode.play_count = 5
    assert episode.info() == 'Episode1: Episode1 -  5 - ****'

def test_invalid_episode_number_raises_value_error():
    try:
        item = LibraryItemEpisode('Episode1', 'Director1', 4, 0)
        assert False
    except ValueError as e:
        assert str(e) == 'Episode number must be an integer > 0'

def test_valid_episode_with_image_and_video_paths():
    episode = LibraryItemEpisode('Episode1', 'Director1', 4, 1, image_path='image.jpg', video_path='video.mp4')
    assert episode.image_path == 'image.jpg'
    assert episode.video_path == 'video.mp4'

def test_valid_library_item_with_image_and_video_paths():
    item = LibraryItem('Movie1', 'Director1', 4, image_path='image.jpg', video_path='video.mp4')
    assert item.image_path == 'image.jpg'
    assert item.video_path == 'video.mp4'

def test_valid_library_item_with_default_rating():
    item = LibraryItem('Movie1', 'Director1')
    assert item.rating == 1


