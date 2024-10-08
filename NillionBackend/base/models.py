from django.db import models
import uuid

class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    photo = models.JSONField()  # Storing photo URLs as a JSON array
    location = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    age = models.IntegerField()
    interest = models.JSONField()  # Storing interests as a JSON array
    liked = models.IntegerField(default=0)
    looking_for = models.CharField(max_length=50, choices=[('male', 'Male'), ('female', 'Female')])
    overall = models.IntegerField(default=0)
    bio = models.TextField()
    work = models.CharField(max_length=255)
    edu = models.CharField(max_length=255)
    zodiac = models.CharField(max_length=50)
    isonmatch = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_id = models.UUIDField()
    sender_address = models.CharField(max_length=255)
    content = models.TextField()
    transaction = models.TextField()
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender_address}: {self.content[:20]}...'

class Rejectd(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_address = models.CharField(max_length=255)
    rejected_address = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rejected from {self.from_address} to {self.rejected_address} on {self.datetime}"

class Favorites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    accept_status = models.BooleanField(default=False)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Favorite from {self.from_address} to {self.to_address} - Status: {'Accepted' if self.accept_status else 'Pending'}"

class Song(models.Model):
    current_address = models.CharField(max_length=42)  # Ethereum addresses are 42 characters long
    music_ipfs = models.CharField(max_length=255)
    music_name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()  # Assuming duration is in seconds
    language = models.CharField(max_length=50)
    artist_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    ipfs_song_image = models.CharField(max_length=255)
    transaction = models.TextField()

    def __str__(self):
        return self.music_name