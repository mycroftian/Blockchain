import React, { useState, useEffect, useContext } from 'react';
import { ethers } from 'ethers';
import { BlockchainContext } from '../context/BlockchainContext';

const RecieverDashboard = () => {
  const { contracts, addresses, currentAccount } =
    useContext(BlockchainContext);

  const [planName, setPlanName] = useState('');
  const [price, setPrice] = useState('');
  const [frequency, setFrequency] = useState('');
  const [logo, setLogo] = useState('');
  const [loading, setLoading] = useState(false);
  const [myPlans, setMyPlans] = useState([]);
  const [loadingPlans, setLoadingPlans] = useState(true);

  useEffect(() => {
    fetchMyPlans();
  }, [contracts, currentAccount]);

  const fetchMyPlans = async () => {
    if (!contracts || !currentAccount) {
      setLoadingPlans(false);
      return;
    }

    try {
      const planCount = await contracts.manager.planCount();
      const creatorPlans = [];

      for (let i = 0; i < Number(planCount); i++) {
        const plan = await contracts.manager.plans(i);
        if (plan.owner.toLowerCase() === currentAccount.toLowerCase()) {
          creatorPlans.push({
            id: i,
            name: plan.name,
            price: ethers.formatUnits(plan.price, 18),
            frequency: Number(plan.frequency) / (24 * 60 * 60),
            logo: plan.logo,
          });
        }
      }

      setMyPlans(creatorPlans);
    } catch (error) {
      console.error('Error fetching plans:', error);
    } finally {
      setLoadingPlans(false);
    }
  };

  const handleCreatePlan = async (e) => {
    e.preventDefault();

    if (!contracts) {
      alert('Please connect your wallet first.');
      return;
    }

    if (!planName || !price || !frequency) {
      alert('Please fill all fields.');
      return;
    }

    try {
      setLoading(true);

      const frequencyInSeconds = parseInt(frequency) * 24 * 60 * 60;

      const tx = await contracts.manager.createPlan(
        planName,
        ethers.parseUnits(price, 18),
        addresses.token,
        frequencyInSeconds,
        logo
      );

      await tx.wait();
      alert('Plan created successfully!');
      setPlanName('');
      setPrice('');
      setFrequency('');
      setLogo('');

      await fetchMyPlans();
    } catch (err) {
      alert('Error: ' + (err.reason || err.message));
    } finally {
      setLoading(false);
    }
  };

  if (!currentAccount) {
    return (
      <div className='flex items-center justify-center min-h-[60vh]'>
        <div className='text-center'>
          <h2 className='text-2xl font-bold text-gray-800 mb-2'>
            Connect Your Wallet
          </h2>
          <p className='text-gray-600'>
            Please connect your wallet to create plans
          </p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className='mb-8'>
        <h1 className='text-3xl font-bold text-gray-800 mb-2'>
          Create Subscription Plan
        </h1>
        <p className='text-gray-600'>
          Set up recurring payment plans for your services
        </p>
      </div>

      <div className='grid grid-cols-1 lg:grid-cols-2 gap-8'>
        <div className='bg-white p-6 rounded-lg border border-gray-200'>
          <h2 className='text-xl font-bold text-gray-800 mb-6'>New Plan</h2>
          <form onSubmit={handleCreatePlan} className='space-y-4'>
            <div>
              <label className='block text-sm font-semibold text-gray-700 mb-2'>
                Plan Name
              </label>
              <input
                className='w-full px-4 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
                type='text'
                placeholder='Premium Monthly'
                value={planName}
                onChange={(e) => setPlanName(e.target.value)}
                disabled={loading}
              />
            </div>

            <div>
              <label className='block text-sm font-semibold text-gray-700 mb-2'>
                Price (tokens)
              </label>
              <input
                className='w-full px-4 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
                type='number'
                step='0.01'
                placeholder='100'
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                disabled={loading}
              />
            </div>

            <div>
              <label className='block text-sm font-semibold text-gray-700 mb-2'>
                Billing Cycle (days)
              </label>
              <input
                className='w-full px-4 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
                type='number'
                placeholder='30'
                value={frequency}
                onChange={(e) => setFrequency(e.target.value)}
                disabled={loading}
              />
            </div>

            <div>
              <label className='block text-sm font-semibold text-gray-700 mb-2'>
                Logo URL (optional)
              </label>
              <input
                className='w-full px-4 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
                type='url'
                placeholder='https://example.com/logo.png'
                value={logo}
                onChange={(e) => setLogo(e.target.value)}
                disabled={loading}
              />
            </div>

            <div className='pt-2'>
              <button
                type='submit'
                disabled={loading}
                className={`w-full py-3 px-6 rounded-lg font-semibold ${
                  loading
                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {loading ? 'Creating Plan...' : 'Create Plan'}
              </button>
            </div>
          </form>
        </div>

        <div>
          <h2 className='text-xl font-bold text-gray-800 mb-6'>Your Plans</h2>
          {loadingPlans ? (
            <div className='flex justify-center py-10'>
              <div className='animate-spin rounded-full h-10 w-10 border-4 border-blue-600 border-t-transparent'></div>
            </div>
          ) : myPlans.length === 0 ? (
            <div className='bg-white p-8 rounded-lg border border-gray-200 text-center'>
              <p className='text-gray-600'>No plans created yet</p>
            </div>
          ) : (
            <div className='space-y-4'>
              {myPlans.map((plan) => (
                <div
                  key={plan.id}
                  className='bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow'
                >
                  <div className='flex items-center gap-3 mb-3'>
                    {plan.logo ? (
                      <img
                        src={plan.logo}
                        alt={plan.name}
                        className='h-10 w-10 object-contain rounded'
                      />
                    ) : (
                      <div className='h-10 w-10 bg-blue-100 rounded flex items-center justify-center text-blue-600 font-bold'>
                        {plan.name.charAt(0)}
                      </div>
                    )}
                    <h3 className='text-lg font-bold text-gray-800'>
                      {plan.name}
                    </h3>
                  </div>
                  <div className='space-y-2 text-sm'>
                    <div className='flex justify-between'>
                      <span className='text-gray-600'>Plan ID</span>
                      <span className='font-semibold text-gray-900'>
                        #{plan.id}
                      </span>
                    </div>
                    <div className='flex justify-between'>
                      <span className='text-gray-600'>Price</span>
                      <span className='font-semibold text-gray-900'>
                        {plan.price} tokens
                      </span>
                    </div>
                    <div className='flex justify-between'>
                      <span className='text-gray-600'>Billing Cycle</span>
                      <span className='font-semibold text-gray-900'>
                        {plan.frequency} days
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecieverDashboard;
