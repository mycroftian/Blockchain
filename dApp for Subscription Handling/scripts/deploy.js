// scripts/deploy.js
import { network } from 'hardhat';
import fs from 'fs';
import path from 'path';

async function main() {
  const { ethers } = await network.connect();

  const [deployer] = await ethers.getSigners();
  console.log('Deploying contracts with account:', deployer.address);

  // Deploy TestToken
  const Token = await ethers.getContractFactory('TestToken');
  const token = await Token.deploy();
  await token.waitForDeployment();
  const tokenAddress = await token.getAddress();
  console.log('TestToken deployed at:', tokenAddress);

  // Deploy MembershipToken
  const MembershipTokenFactory = await ethers.getContractFactory(
    'MembershipToken'
  );
  const membershipToken = await MembershipTokenFactory.deploy();
  await membershipToken.waitForDeployment();
  const membershipTokenAddress = await membershipToken.getAddress();
  console.log('MembershipToken deployed at:', membershipTokenAddress);

  // Deploy SubscriptionManager (requires MembershipToken address)
  const Manager = await ethers.getContractFactory('SubscriptionManager');
  const manager = await Manager.deploy(membershipTokenAddress);
  await manager.waitForDeployment();
  const managerAddress = await manager.getAddress();
  console.log('SubscriptionManager deployed at:', managerAddress);

  // Link MembershipToken to manager
  await membershipToken.setSubscriptionManager(managerAddress);
  console.log('SubscriptionManager linked to MembershipToken.');

  // Write deployment addresses for frontend
  const deploymentData = {
    TestToken: tokenAddress,
    MembershipToken: membershipTokenAddress,
    SubscriptionManager: managerAddress,
    network: {
      name: 'localhost',
      rpc: 'http://127.0.0.1:8545',
      chainId: 31337,
    },
  };

  const frontendPath = path.join(process.cwd(), 'src');
  if (!fs.existsSync(frontendPath)) {
    fs.mkdirSync(frontendPath, { recursive: true });
  }

  fs.writeFileSync(
    path.join(frontendPath, 'deployments.json'),
    JSON.stringify(deploymentData, null, 2)
  );
  console.log('✅ Wrote src/deployments.json');

  // Copy ABIs to src/abi
  const abiPath = path.join(frontendPath, 'abi');
  if (!fs.existsSync(abiPath)) {
    fs.mkdirSync(abiPath, { recursive: true });
  }

  const artifactsPath = path.join(process.cwd(), 'artifacts', 'contracts');

  // Copy TestToken ABI
  const tokenArtifact = JSON.parse(
    fs.readFileSync(
      path.join(artifactsPath, 'TestToken.sol', 'TestToken.json'),
      'utf8'
    )
  );
  fs.writeFileSync(
    path.join(abiPath, 'TestToken.json'),
    JSON.stringify(tokenArtifact, null, 2)
  );

  // Copy MembershipToken ABI
  const nftArtifact = JSON.parse(
    fs.readFileSync(
      path.join(artifactsPath, 'MembershipToken.sol', 'MembershipToken.json'),
      'utf8'
    )
  );
  fs.writeFileSync(
    path.join(abiPath, 'MembershipToken.json'),
    JSON.stringify(nftArtifact, null, 2)
  );

  // Copy SubscriptionManager ABI
  const managerArtifact = JSON.parse(
    fs.readFileSync(
      path.join(
        artifactsPath,
        'SubscriptionManager.sol',
        'SubscriptionManager.json'
      ),
      'utf8'
    )
  );
  fs.writeFileSync(
    path.join(abiPath, 'SubscriptionManager.json'),
    JSON.stringify(managerArtifact, null, 2)
  );

  console.log('✅ Copied ABIs to src/abi/');
  console.log('\n🎉 Deployment complete! Frontend is ready to use.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
