import React from 'react';

const PlanCard = ({
  id,
  title,
  price,
  tokenSymbol,
  frequency,
  logo,
  onSubscribe,
  isProcessing,
}) => {
  return (
    <div className='bg-white rounded-xl border-2 border-gray-200 hover:border-blue-400 hover:shadow-lg transition-all overflow-hidden'>
      {/* Logo/Banner */}
      <div className='h-32 bg-blue-500 flex items-center justify-center'>
        {logo ? (
          <img
            src={logo}
            alt={title}
            className='h-20 w-20 object-contain rounded-lg bg-white p-2'
          />
        ) : (
          <div className='h-20 w-20 bg-white rounded-lg flex items-center justify-center text-3xl font-bold text-blue-600'>
            {title.charAt(0)}
          </div>
        )}
      </div>

      {/* Content */}
      <div className='p-6'>
        <h3 className='text-xl font-bold text-gray-800 mb-4'>{title}</h3>

        <div className='mb-6'>
          <div className='flex items-baseline gap-2 mb-1'>
            <span className='text-4xl font-bold text-blue-600'>{price}</span>
            <span className='text-gray-600 font-medium'>{tokenSymbol}</span>
          </div>
          <p className='text-sm text-gray-500'>Every {frequency} days</p>
        </div>

        <button
          onClick={() => onSubscribe(id)}
          disabled={isProcessing}
          className={`w-full py-3 rounded-lg font-semibold transition-colors ${
            isProcessing
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {isProcessing ? 'Processing...' : 'Subscribe'}
        </button>
      </div>
    </div>
  );
};

export default PlanCard;
