from django.shortcuts import render, redirect
from base.models import Song
import requests
from .WebThree import StoreMusic

# List all songs
def song_list(request):
    songs = Song.objects.all()
    return render(request, 'songs/song_list.html', {'songs': songs})


def upload_to_ipfs(file_path, file_type):
    url = "https://api.verbwire.com/v1/nft/store/file"
    
    with open(file_path, "rb") as f:
        files = {
            "filePath": (file_path.split("/")[-1], f, file_type)
        }
        headers = {
            "accept": "application/json",
            "X-API-Key": "sk_live_fdd243a1-07c3-4c90-a976-c133c47f1b3a"
        }

        response = requests.post(url, files=files, headers=headers)
        ipfs_url = response.json().get("ipfs_storage", {}).get("ipfs_url")
        return ipfs_url

def upload_song(request, address):
    if request.method == 'POST':
        music_file = request.FILES['music_file']
        song_image = request.FILES['song_image']
        music_name = request.POST['music_name']
        duration = request.POST['duration']
        language = request.POST['language']
        artist_name = request.POST['artist_name']
        genre = request.POST['genre']
        
        music_ipfs_url = upload_to_ipfs(music_file.temporary_file_path(), "audio/mpeg")
        image_ipfs_url = upload_to_ipfs(song_image.temporary_file_path(), "image/jpeg")
        
        song = Song.objects.create(
            current_address=address,
            music_ipfs=music_ipfs_url,
            music_name=music_name,
            duration=duration,
            language=language,
            artist_name=artist_name,
            genre=genre,
            ipfs_song_image=image_ipfs_url,
            transaction = StoreMusic(address, music_ipfs_url, music_name, int(duration), language, artist_name, genre, image_ipfs_url)
        )
        
        return redirect('song_list')
    
    return render(request, 'songs/add_song.html')

def music_player(request):
    songs = list(Song.objects.values('music_name', 'artist_name', 'music_ipfs'))
    return render(request, 'songs/musicplayer.html', {'songs': songs})