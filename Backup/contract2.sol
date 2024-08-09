// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

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

    struct Chat {
        string chatId;
        string senderAddress;
        string content;
        string endpoint;
        uint256 timestamp;
    }

    struct Profile {
        string userAddress;
        string name;
        string location;
        string gender;
        uint256 age;
        string bio;
        bool isOnMatch;
    }

    Song[] public songs;
    Chat[] public chats;
    Profile[] public profiles;

    mapping(string => uint256[]) private songsByLanguage;
    mapping(string => uint256) private songIndexByName;
    mapping(string => uint256) private profileIndexByAddress;
    mapping(string => uint256[]) private chatsByAddress;

    // Function to add a new song
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

    // Function to get a song by index
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

    // Function to get song IDs by language
    function getSongsByLanguage(string memory _language) public view returns (uint256[] memory) {
        return songsByLanguage[_language];
    }

    // Function to add a new chat
    function addChat(
        string memory _chatId,
        string memory _senderAddress,
        string memory _content,
        string memory _endpoint,
        uint256 _timestamp
    ) public {
        Chat memory newChat = Chat({
            chatId: _chatId,
            senderAddress: _senderAddress,
            content: _content,
            endpoint: _endpoint,
            timestamp: _timestamp
        });

        chats.push(newChat);
        chatsByAddress[_senderAddress].push(chats.length - 1);
    }

    // Function to get a chat by index
    function getChat(uint256 _index) public view returns (
        string memory,
        string memory,
        string memory,
        string memory,
        uint256
    ) {
        require(_index < chats.length, "Invalid chat index");
        Chat memory chat = chats[_index];
        return (
            chat.chatId,
            chat.senderAddress,
            chat.content,
            chat.endpoint,
            chat.timestamp
        );
    }

    // Function to get a chat by chatId
    function getChatByChatId(string memory _chatId) public view returns (
        string memory,
        string memory,
        string memory,
        string memory,
        uint256
    ) {
        for (uint256 i = 0; i < chats.length; i++) {
            if (keccak256(abi.encodePacked(chats[i].chatId)) == keccak256(abi.encodePacked(_chatId))) {
                Chat memory chat = chats[i];
                return (
                    chat.chatId,
                    chat.senderAddress,
                    chat.content,
                    chat.endpoint,
                    chat.timestamp
                );
            }
        }
        revert("Chat with the given chatId does not exist.");
    }

    // Function to add a new profile
    function addProfile(
        string memory _userAddress,
        string memory _name,
        string memory _location,
        string memory _gender,
        uint256 _age,
        string memory _bio,
        bool _isOnMatch
    ) public {
        Profile memory newProfile = Profile({
            userAddress: _userAddress,
            name: _name,
            location: _location,
            gender: _gender,
            age: _age,
            bio: _bio,
            isOnMatch: _isOnMatch
        });

        profiles.push(newProfile);
        profileIndexByAddress[_userAddress] = profiles.length - 1;
    }

    // Function to get a profile by user address
    function getProfile(string memory _userAddress) public view returns (Profile memory) {
        require(profileIndexByAddress[_userAddress] < profiles.length, "Profile does not exist");
        return profiles[profileIndexByAddress[_userAddress]];
    }

    // Function to get all chats for a given user address
    function getAllChatsByUserAddress(string memory _userAddress) public view returns (Chat[] memory) {
        uint256[] storage chatIndexes = chatsByAddress[_userAddress];
        Chat[] memory userChats = new Chat[](chatIndexes.length);

        for (uint256 i = 0; i < chatIndexes.length; i++) {
            userChats[i] = chats[chatIndexes[i]];
        }

        return userChats;
    }

    // Internal function to remove a song from the language mapping
    function _removeFromLanguageMapping(string memory _language, uint256 _index) internal {
        uint256[] storage languageSongs = songsByLanguage[_language];
        for (uint256 i = 0; i < languageSongs.length; i++) {
            if (languageSongs[i] == _index) {
                languageSongs[i] = languageSongs[languageSongs.length - 1];
                languageSongs.pop();
                break;
            }
        }
    }
}
