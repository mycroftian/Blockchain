import React, { useContext } from 'react';
import { BlockchainContext } from '../context/BlockchainContext';

const Navbar = ({ view, setView }) => {
  const { currentAccount, connectWallet, isLoading } =
    useContext(BlockchainContext);

  return (
    <nav className='bg-white border-b border-gray-200 sticky top-0 z-50'>
      <div className='container mx-auto px-6 py-4'>
        <div className='flex justify-between items-center'>
          <div className='flex items-center gap-8'>
            <h1 className='text-2xl font-bold text-blue-600'>SubsCrypt</h1>
            <div className='flex gap-2'>
              <button
                onClick={() => setView('discover')}
                className={`px-6 py-2 rounded-lg font-medium ${
                  view === 'discover'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Discover
              </button>
              <button
                onClick={() => setView('subscriptions')}
                className={`px-6 py-2 rounded-lg font-medium ${
                  view === 'subscriptions'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                My Subscriptions
              </button>
              <button
                onClick={() => setView('creator')}
                className={`px-6 py-2 rounded-lg font-medium ${
                  view === 'creator'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Create Plan
              </button>
            </div>
          </div>
          {currentAccount ? (
            <div className='flex items-center gap-3'>
              <div className='px-4 py-2 bg-green-50 rounded-lg border border-green-200'>
                <span className='text-sm font-mono text-green-700'>
                  {currentAccount.slice(0, 6)}...{currentAccount.slice(-4)}
                </span>
              </div>
            </div>
          ) : (
            <button
              onClick={connectWallet}
              disabled={isLoading}
              className='px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50'
            >
              {isLoading ? 'Connecting...' : 'Connect Wallet'}
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
