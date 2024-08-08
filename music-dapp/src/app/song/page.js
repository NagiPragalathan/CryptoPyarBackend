"use client";

import { useState } from 'react';
import { signer, contract } from './ethers';
import ConnectMetaMaskButton from './ConnectMetaMaskButton';

const AddSongForm = () => {
  const [form, setForm] = useState({
    musicIpfs: '',
    musicName: '',
    duration: '',
    language: '',
    artistName: '',
    genre: '',
    ipfsSongImage: ''
  });

  const [userAddress, setUserAddress] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!signer || !contract) {
      alert('Contract not initialized. Please ensure MetaMask is connected.');
      return;
    }
    try {
      const message = `Adding a song with name: ${form.musicName}`;
      const signature = await signer.signMessage(message);

      console.log('User Address:', userAddress);
      console.log('Signature:', signature);

      const tx = await contract.addSong(
        userAddress,
        form.musicIpfs,
        form.musicName,
        parseInt(form.duration),
        form.language,
        form.artistName,
        form.genre,
        form.ipfsSongImage
      );
      await tx.wait();
      alert('Song added successfully');
    } catch (error) {
      console.error('Error adding song', error);
      alert('Error adding song');
    }
  };

  return (
    <div>
      <ConnectMetaMaskButton onConnected={(address) => setUserAddress(address)} />
      <form onSubmit={handleSubmit}>
        <input type="text" name="musicIpfs" placeholder="Music IPFS" onChange={handleChange} required />
        <input type="text" name="musicName" placeholder="Music Name" onChange={handleChange} required />
        <input type="number" name="duration" placeholder="Duration" onChange={handleChange} required />
        <input type="text" name="language" placeholder="Language" onChange={handleChange} required />
        <input type="text" name="artistName" placeholder="Artist Name" onChange={handleChange} required />
        <input type="text" name="genre" placeholder="Genre" onChange={handleChange} required />
        <input type="text" name="ipfsSongImage" placeholder="IPFS Song Image" onChange={handleChange} required />
        <button type="submit">Add Song</button>
      </form>
    </div>
  );
};

export default AddSongForm;
