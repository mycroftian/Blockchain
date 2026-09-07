import React, { useState, useEffect, createContext } from 'react';
import { ethers } from 'ethers';
import { getContracts, getAddresses, getNetworkConfig } from '../blockchain';

export const BlockchainContext = createContext();

export const BlockchainProvider = ({ children }) => {
  const [currentAccount, setCurrentAccount] = useState(null);
  const [provider, setProvider] = useState(null);
  const [signer, setSigner] = useState(null);
  const [contracts, setContracts] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const connectWallet = async () => {
    try {
      if (!window.ethereum) return alert('Please install MetaMask.');

      setIsLoading(true);

      // Request account access
      await window.ethereum.request({ method: 'eth_requestAccounts' });

      const accounts = await window.ethereum.request({
        method: 'eth_accounts',
      });
      if (accounts.length) {
        setCurrentAccount(accounts[0]);

        // Get contracts using centralized connector
        const contractInstances = await getContracts();
        setProvider(contractInstances.provider);
        setSigner(contractInstances.signer);
        setContracts(contractInstances);

        // Network Check (Force Localhost)
        const network = await contractInstances.provider.getNetwork();
        if (
          Number(network.chainId) !== 1337 &&
          Number(network.chainId) !== 31337
        ) {
          alert('Please switch MetaMask to Localhost 8545 (Chain ID: 31337)');
        }
      }
    } catch (error) {
      console.error('Error connecting wallet:', error);
      alert('Error connecting wallet: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle account changes and auto-connect
  useEffect(() => {
    if (window.ethereum) {
      // Auto-connect if trusted
      const checkConnection = async () => {
        try {
          const accounts = await window.ethereum.request({
            method: 'eth_accounts',
          });
          if (accounts.length) {
            setCurrentAccount(accounts[0]);
            const contractInstances = await getContracts();
            setProvider(contractInstances.provider);
            setSigner(contractInstances.signer);
            setContracts(contractInstances);
          }
        } catch (error) {
          console.error('Auto-connect failed:', error);
        }
      };
      checkConnection();

      // Listen for account changes
      window.ethereum.on('accountsChanged', async (accounts) => {
        if (accounts.length > 0) {
          setCurrentAccount(accounts[0]);
          try {
            const contractInstances = await getContracts();
            setProvider(contractInstances.provider);
            setSigner(contractInstances.signer);
            setContracts(contractInstances);
          } catch (error) {
            console.error('Error switching accounts:', error);
          }
        } else {
          setCurrentAccount(null);
          setSigner(null);
          setProvider(null);
          setContracts(null);
        }
      });
    }
  }, []);

  return (
    <BlockchainContext.Provider
      value={{
        connectWallet,
        currentAccount,
        provider,
        signer,
        contracts,
        isLoading,
        addresses: getAddresses(),
        networkConfig: getNetworkConfig(),
      }}
    >
      {children}
    </BlockchainContext.Provider>
  );
};
