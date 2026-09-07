// src/blockchain.js
import { BrowserProvider, Contract } from 'ethers';
import managerAbi from './abi/SubscriptionManager.json';
import membershipTokenAbi from './abi/MembershipToken.json';
import tokenAbi from './abi/TestToken.json';
import deployments from './deployments.json';

const MANAGER = deployments.SubscriptionManager;
const MEMBERSHIP_TOKEN = deployments.MembershipToken;
const TOKEN = deployments.TestToken;

/**
 * Get all contract instances and blockchain connections
 * @returns {Promise<{provider: BrowserProvider, signer: Signer, manager: Contract, membershipToken: Contract, token: Contract, deployments: object}>}
 */
export async function getContracts() {
  if (!window.ethereum) {
    throw new Error('Please install MetaMask');
  }

  const provider = new BrowserProvider(window.ethereum);
  await provider.send('eth_requestAccounts', []);
  const signer = await provider.getSigner();

  const manager = new Contract(MANAGER, managerAbi.abi, signer);
  const membershipToken = new Contract(
    MEMBERSHIP_TOKEN,
    membershipTokenAbi.abi,
    signer
  );
  const token = new Contract(TOKEN, tokenAbi.abi, signer);

  return { provider, signer, manager, membershipToken, token, deployments };
}

/**
 * Get contract addresses
 */
export function getAddresses() {
  return {
    manager: MANAGER,
    membershipToken: MEMBERSHIP_TOKEN,
    token: TOKEN,
  };
}

/**
 * Get network configuration
 */
export function getNetworkConfig() {
  return deployments.network;
}
