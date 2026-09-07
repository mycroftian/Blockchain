import React from 'react';

const MySubscriptionCard = ({
  planId,
  title,
  price,
  nextPayment,
  memberId,
  logo,
  onUnsubscribe,
  isProcessing,
}) => {
  const formatDate = (timestamp) => {
    if (!timestamp) return 'N/A';
    return new Date(Number(timestamp) * 1000).toLocaleDateString();
  };

  return (
    <div className='bg-white rounded-xl border-2 border-green-200 hover:shadow-lg transition-all overflow-hidden'>
      {/* Membership Card Header */}
      <div className='bg-linear-to-br from-green-500 to-emerald-600 p-6 text-white'>
        <div className='flex justify-between items-start'>
          <div className='flex items-center gap-3'>
            {logo ? (
              <img
                src={logo}
                alt={title}
                className='h-12 w-12 object-contain rounded-lg bg-white p-1'
              />
            ) : (
              <div className='h-12 w-12 bg-white rounded-lg flex items-center justify-center text-xl font-bold text-green-600'>
                {title.charAt(0)}
              </div>
            )}
            <div>
              <h3 className='text-lg font-bold'>{title}</h3>
              <span className='text-xs bg-white/20 px-2 py-1 rounded-full'>
                Active Member
              </span>
            </div>
          </div>
          <div className='text-right'>
            <div className='text-xs opacity-80'>Member ID</div>
            <div className='text-2xl font-bold'>{memberId.toString()}</div>
          </div>
        </div>
      </div>

      {/* Card Details */}
      <div className='p-6'>
        <div className='grid grid-cols-2 gap-4 mb-6'>
          <div>
            <div className='text-xs text-gray-500 mb-1'>Price</div>
            <div className='text-lg font-bold text-gray-800'>
              {price} tokens
            </div>
          </div>
          <div>
            <div className='text-xs text-gray-500 mb-1'>Next Payment</div>
            <div className='text-lg font-bold text-gray-800'>
              {formatDate(nextPayment)}
            </div>
          </div>
        </div>

        <button
          onClick={() => onUnsubscribe(planId)}
          disabled={isProcessing}
          className={`w-full py-3 rounded-lg font-semibold transition-colors ${
            isProcessing
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-red-600 text-white hover:bg-red-700'
          }`}
        >
          {isProcessing ? 'Cancelling...' : 'Cancel Membership'}
        </button>
      </div>
    </div>
  );
};

export default MySubscriptionCard;
