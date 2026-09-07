import React, { useState, useEffect, useContext } from 'react';
import { ethers } from 'ethers';
import MySubscriptionCard from '../components/MySubscriptionCard';
import { BlockchainContext } from '../context/BlockchainContext';

const UserDashboard = () => {
  const { contracts, currentAccount } = useContext(BlockchainContext);

  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processingId, setProcessingId] = useState(null);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      if (!contracts || !currentAccount) {
        setLoading(false);
        return;
      }

      try {
        const planCount = await contracts.manager.planCount();
        const activeSubs = [];

        for (let i = 0; i < Number(planCount); i++) {
          const status = await contracts.manager.getSenderStatus(
            i,
            currentAccount
          );

          if (status.subscribed) {
            const planDetails = await contracts.manager.plans(i);

            activeSubs.push({
              planId: i,
              title: planDetails.name,
              price: ethers.formatUnits(planDetails.price, 18),
              nextPayment: status.nextPayment,
              memberId: status.tokenId,
              logo: planDetails.logo,
            });
          }
        }

        setSubscriptions(activeSubs);
      } catch (error) {
        console.error('Error fetching dashboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSubscriptions();
  }, [contracts, currentAccount]);

  const handleUnsubscribe = async (planId) => {
    if (!contracts) {
      alert('Please connect your wallet first!');
      return;
    }

    try {
      setProcessingId(planId);
      const tx = await contracts.manager.unsubscribe(planId);
      await tx.wait();
      alert('Unsubscribed successfully!');
      setSubscriptions((prev) => prev.filter((sub) => sub.planId !== planId));
    } catch (error) {
      console.error(error);
      alert('Unsubscribe Failed: ' + (error.reason || error.message));
    } finally {
      setProcessingId(null);
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
            Please connect your wallet to view your subscriptions
          </p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className='flex justify-center items-center min-h-[60vh]'>
        <div className='animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent'></div>
      </div>
    );
  }

  return (
    <div>
      <div className='mb-8'>
        <h1 className='text-3xl font-bold text-gray-800 mb-2'>
          My Subscriptions
        </h1>
        <p className='text-gray-600'>Manage your active subscriptions</p>
      </div>

      {subscriptions.length === 0 ? (
        <div className='text-center py-20 bg-white rounded-lg border border-gray-200'>
          <h3 className='text-xl font-bold text-gray-800 mb-2'>
            No Active Subscriptions
          </h3>
          <p className='text-gray-600'>
            You haven't subscribed to any plans yet. Head to Discover to find
            plans!
          </p>
        </div>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
          {subscriptions.map((sub) => (
            <MySubscriptionCard
              key={sub.planId}
              planId={sub.planId}
              title={sub.title}
              price={sub.price}
              nextPayment={sub.nextPayment}
              memberId={sub.memberId}
              logo={sub.logo}
              onUnsubscribe={handleUnsubscribe}
              isProcessing={processingId === sub.planId}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default UserDashboard;
