// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MusicList {
    struct Song {
        address currentAddress;
        string musicIpfs;
        string musicName;
        uint256 duration;
        string language;
        string artistName;
        string genre;
        string ipfsSongImage;
    }

    Song[] public songs;

    mapping(string => uint256[]) private songsByLanguage;
    mapping(string => uint256) private songIndexByName;

    function addSong(
        address _currentAddress,
        string memory _musicIpfs,
        string memory _musicName,
        uint256 _duration,
        string memory _language,
        string memory _artistName,
        string memory _genre,
        string memory _ipfsSongImage
    ) public {
        Song memory newSong = Song({
            currentAddress: _currentAddress,
            musicIpfs: _musicIpfs,
            musicName: _musicName,
            duration: _duration,
            language: _language,
            artistName: _artistName,
            genre: _genre,
            ipfsSongImage: _ipfsSongImage
        });

        songs.push(newSong);
        uint256 songId = songs.length - 1;
        songsByLanguage[_language].push(songId);
        songIndexByName[_musicName] = songId;
    }

    function getSong(uint256 _index) public view returns (
        address,
        string memory,
        string memory,
        uint256,
        string memory,
        string memory,
        string memory,
        string memory
    ) {
        require(_index < songs.length, "Invalid song index");
        Song memory song = songs[_index];
        return (
            song.currentAddress,
            song.musicIpfs,
            song.musicName,
            song.duration,
            song.language,
            song.artistName,
            song.genre,
            song.ipfsSongImage
        );
    }

    function getSongsByLanguage(string memory _language) public view returns (uint256[] memory) {
        return songsByLanguage[_language];
    }

    function getSongByMusicName(string memory _musicName) public view returns (
        address,
        string memory,
        string memory,
        uint256,
        string memory,
        string memory,
        string memory,
        string memory
    ) {
        uint256 songId = songIndexByName[_musicName];
        return getSong(songId);
    }

    function setSong(
        uint256 _index,
        address _currentAddress,
        string memory _musicIpfs,
        string memory _musicName,
        uint256 _duration,
        string memory _language,
        string memory _artistName,
        string memory _genre,
        string memory _ipfsSongImage
    ) public {git 
        require(_index < songs.length, "Invalid song index");
        Song storage song = songs[_index];
        song.currentAddress = _currentAddress;
        song.musicIpfs = _musicIpfs;
        song.musicName = _musicName;
        song.duration = _duration;
        song.language = _language;
        song.artistName = _artistName;
        song.genre = _genre;
        song.ipfsSongImage = _ipfsSongImage;

        // Update mappings if necessary
        if (keccak256(abi.encodePacked(song.language)) != keccak256(abi.encodePacked(_language))) {
            // Remove from old language mapping
            uint256[] storage oldLanguageSongs = songsByLanguage[song.language];
            for (uint256 i = 0; i < oldLanguageSongs.length; i++) {
                if (oldLanguageSongs[i] == _index) {
                    oldLanguageSongs[i] = oldLanguageSongs[oldLanguageSongs.length - 1];
                    oldLanguageSongs.pop();
                    break;
                }
            }
            // Add to new language mapping
            songsByLanguage[_language].push(_index);
        }

        if (keccak256(abi.encodePacked(song.musicName)) != keccak256(abi.encodePacked(_musicName))) {
            delete songIndexByName[song.musicName];
            songIndexByName[_musicName] = _index;
        }
    }
}
