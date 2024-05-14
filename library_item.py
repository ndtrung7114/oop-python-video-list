class LibraryItem:
    def __init__(self, name, director, rating=1, image_path=None, video_path=None):
        if name == '':
            raise ValueError('Name can not be empty')
        if director == '':
            raise ValueError('Director can not be empty')
        try:
            rating = int(rating)
        except ValueError:
            raise ValueError('Rating must be integer number')
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be in range(1, 5)')
        self.name = name
        self.director = director
        self.rating = rating
        self.play_count = 0
        self.image_path = image_path
        self.video_path = video_path

    def info(self):
        return f"{self.name} - {self.director} {self.stars()}"

    def stars(self):
        stars = ""
        for i in range(self.rating):
            stars += "*"
        return stars



class LibraryItemEpisode(LibraryItem):
    def __init__(self, name, director, rating, episode_number, image_path=None, video_path=None):
        super().__init__(name, director, rating, image_path, video_path)

        self.play_count = 0
        try:
            episode_number = int(episode_number)
        except ValueError:
            raise ValueError('Episode number must be integer number')
        if episode_number <= 0:
            raise ValueError('Episode number must be an integer > 0')
        self.episode_number = episode_number

    def info(self):
        return f"Episode{self.episode_number}: {self.name} -  {self.play_count} - {self.stars()}"


