from django.shortcuts import render, redirect
from base.models import Song

# List all songs
def song_list(request):
    songs = Song.objects.all()
    return render(request, 'song_list.html', {'songs': songs})

# Form to add a new song
def add_song(request):
    if request.method == 'POST':
        current_address = request.POST.get('current_address')
        music_ipfs = request.POST.get('music_ipfs')
        music_name = request.POST.get('music_name')
        duration = request.POST.get('duration')
        language = request.POST.get('language')
        artist_name = request.POST.get('artist_name')
        genre = request.POST.get('genre')
        ipfs_song_image = request.POST.get('ipfs_song_image')

        Song.objects.create(
            current_address=current_address,
            music_ipfs=music_ipfs,
            music_name=music_name,
            duration=duration,
            language=language,
            artist_name=artist_name,
            genre=genre,
            ipfs_song_image=ipfs_song_image
        )

        return redirect('song_list')

    return render(request, 'add_song.html')
