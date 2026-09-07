# SubsCrypt - Decentralized Subscription Platform

A modern DApp for creating and managing subscription plans with token-based membership on Ethereum.

## Quick Start

### One-Time Setup

1. **Install MetaMask** and add local network:

   - Network: `Hardhat Local`
   - RPC: `http://127.0.0.1:8545`
   - Chain ID: `31337`

2. **Install & Deploy**:

   ```bash
   npm install
   npm run start:auto  # Terminal 1
   ```

3. **Import Test Account**:

   - Copy private key from Hardhat output
   - Import to MetaMask

4. **Start Frontend** (new terminal):
   ```bash
   npm run frontend  # Terminal 2
   ```

### Daily Workflow

```bash
npm run start:auto  # Terminal 1: Node + Deploy
npm run frontend    # Terminal 2: React App
```

## Features

- **Create Plans** - Set up recurring subscription plans with custom names
- **Subscribe** - Pay with TestToken (TTK) and receive membership token
- **Auto-Approval** - Automatic token approval before subscription
- **View Subscriptions** - Track active subscriptions and membership IDs
- **Creator Dashboard** - View all plans you've created

## NPM Scripts

| Command              | Description                |
| -------------------- | -------------------------- |
| `npm run compile`    | Compile Solidity contracts |
| `npm run start:auto` | Start node + auto-deploy   |
| `npm run frontend`   | Start React dev server     |

## Architecture

```
contracts/
  ├── TestToken.sol           # ERC20 payment token
  ├── MembershipToken.sol     # ERC721 membership token
  └── SubscriptionManager.sol # Main subscription logic

src/
  ├── blockchain.js          # Web3 connector
  ├── deployments.json       # Auto-generated addresses
  ├── abi/                   # Auto-copied ABIs
  ├── components/            # React components
  └── pages/                 # Page views
```

## Design Features

- **Modern UI** - Clean, pill-shaped elements
- **Responsive** - Works on all screen sizes

## Technical Stack

- **Blockchain**: Hardhat, Solidity 0.8.20
- **Frontend**: React 19, Vite
- **Web3**: Ethers.js v6
- **Styling**: Tailwind CSS
- **Tokens**: OpenZeppelin Contracts

## Workflow

### As Creator:

1. Connect wallet
2. Go to "Create Plan"
3. Enter plan name, price (TTK), billing cycle (days)
4. Click "Create Plan"
5. View your plans in the dashboard

### As Subscriber:

1. Connect wallet
2. Browse plans on "Discover"
3. Click "Subscribe Now"
4. Approve tokens (auto-calculated)
5. Confirm subscription
6. Receive Membership Token
7. View in "My Subscriptions"

## Important Notes

- **Local Only**: Each restart creates fresh blockchain
- **Test Accounts**: Use Hardhat private keys for testing
- **Chain ID**: Must be 31337
- **Auto-Generated**: `deployments.json` and ABIs are created automatically
