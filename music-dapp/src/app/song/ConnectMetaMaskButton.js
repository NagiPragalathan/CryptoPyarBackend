"use client";

import { useState } from 'react';
import { initializeEthers } from './ethers';

const ConnectMetaMaskButton = ({ onConnected }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [address, setAddress] = useState('');
  const [error, setError] = useState('');

  const handleConnect = async () => {
    try {
      const { signer } = await initializeEthers();
      if (signer) {
        const userAddress = await signer.getAddress();
        setIsConnected(true);
        setAddress(userAddress);
        if (onConnected) {
          onConnected(userAddress);
        }
      }
    } catch (error) {
      setError(error.message);
      console.error('Error connecting to MetaMask:', error);
    }
  };

  return (
    <div>
      {!isConnected ? (
        <button onClick={handleConnect}>Connect MetaMask</button>
      ) : (
        <div>
          <p>Connected as: {address}</p>
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default ConnectMetaMaskButton;
