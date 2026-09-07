import React, { useState, useEffect, useContext } from 'react';
import { ethers } from 'ethers';
import PlanCard from '../components/PlanCard';
import { BlockchainContext } from '../context/BlockchainContext';

const Home = () => {
  const { contracts, currentAccount } = useContext(BlockchainContext);

  const [plans, setPlans] = useState([]);
  const [loadingPlanId, setLoadingPlanId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPlans = async () => {
      if (!contracts) {
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        const count = await contracts.manager.planCount();

        if (Number(count) > 0) {
          const fetchedPlans = [];
          for (let i = 0; i < count; i++) {
            const planData = await contracts.manager.plans(i);
            fetchedPlans.push({
              id: i,
              name: planData.name,
              price: ethers.formatUnits(planData.price, 18),
              frequency: Number(planData.frequency) / (24 * 60 * 60), // Convert seconds to days
              token: 'tokens',
              logo: planData.logo,
            });
          }
          setPlans(fetchedPlans);
        }
      } catch (error) {
        console.error('Failed to fetch plans:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPlans();
  }, [contracts]);

  const handleSubscribe = async (planId) => {
    if (!contracts) return alert('Please connect your wallet first!');
    if (!currentAccount) return alert('Please connect your wallet!');

    try {
      setLoadingPlanId(planId);

      const planData = await contracts.manager.plans(planId);
      const price = planData.price;

      const approveTx = await contracts.token.approve(
        contracts.manager.target,
        price
      );
      await approveTx.wait();

      const tx = await contracts.manager.subscribe(planId);
      await tx.wait();

      alert(`Successfully subscribed to ${planData.name}!`);

      // Refresh plans
      const count = await contracts.manager.planCount();
      const fetchedPlans = [];
      for (let i = 0; i < count; i++) {
        const plan = await contracts.manager.plans(i);
        fetchedPlans.push({
          id: i,
          name: plan.name,
          price: ethers.formatUnits(plan.price, 18),
          frequency: Number(plan.frequency) / (24 * 60 * 60),
          token: 'tokens',
          logo: plan.logo,
        });
      }
      setPlans(fetchedPlans);
    } catch (error) {
      console.error(error);
      alert(
        'Transaction Error: ' +
          (error.reason || error.message || error.toString())
      );
    } finally {
      setLoadingPlanId(null);
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
            Please connect your wallet to discover subscription plans
          </p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className='mb-8'>
        <h1 className='text-3xl font-bold text-gray-800 mb-2'>
          Discover Plans
        </h1>
        <p className='text-gray-600'>Browse available subscription plans</p>
      </div>

      {isLoading ? (
        <div className='flex justify-center items-center py-20'>
          <div className='animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent'></div>
        </div>
      ) : plans.length === 0 ? (
        <div className='text-center py-20 bg-white rounded-lg border border-gray-200'>
          <h3 className='text-xl font-bold text-gray-800 mb-2'>
            No Plans Available
          </h3>
          <p className='text-gray-600'>
            Be the first to create a subscription plan!
          </p>
        </div>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
          {plans.map((plan) => (
            <PlanCard
              key={plan.id}
              id={plan.id}
              title={plan.name}
              price={plan.price}
              frequency={plan.frequency}
              tokenSymbol={plan.token}
              logo={plan.logo}
              onSubscribe={() => handleSubscribe(plan.id)}
              isProcessing={loadingPlanId === plan.id}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;
