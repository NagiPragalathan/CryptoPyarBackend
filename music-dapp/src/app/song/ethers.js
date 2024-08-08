import { ethers } from 'ethers';
import abi from './abi.json'; // Ensure this path is correct

const contractAddress = '0x55796A0A1f934f2c8c738ee8137146DaBE60bb0b'; // Your deployed contract address

let provider;
let signer;
let contract;

async function initializeEthers() {
  if (typeof window !== 'undefined' && typeof window.ethereum !== 'undefined') {
    try {
      provider = new ethers.BrowserProvider(window.ethereum);
      await provider.send('eth_requestAccounts', []); // Request access to MetaMask
      signer = await provider.getSigner();
      contract = new ethers.Contract(contractAddress, abi, signer);
      console.log('Ethers.js initialized', { provider, signer, contract });
      return { provider, signer, contract };
    } catch (error) {
      console.error('Error initializing Ethers.js', error);
      throw new Error('Failed to initialize Ethers.js');
    }
  } else {
    const errorMessage = 'Ethereum provider not found. Please install MetaMask.';
    console.error(errorMessage);
    throw new Error(errorMessage);
  }
}

export { provider, signer, contract, initializeEthers };
