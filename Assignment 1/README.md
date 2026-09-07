# Blockchain-based Medical Records System

This project is a blockchain-powered healthcare records system that stores patient data securely and transparently. It uses a Proof of Stake consensus mechanism where doctors stake tokens to participate in block validation. A simple Streamlit-based frontend is provided for doctors, patients and admins to interact with the system.


## Group Members
- Aniketh Korkonda Bhattar, 2023A8PS1070H
- Aravind Sathesh, 2023A8PS1187H
- Arihant Jha, 2023A8PS1072H
- Sai Abhinav Addagada, 2023A7PS0083H

## Features
- Doctors can add encrypted medical records to the blockchain
- Patients can view their complete medical history
- Admins can manage validators and enforce penalties
- Proof of Stake consensus for validator selection
- Digital signatures for authenticity of each transaction
- Encryption for patient privacy
- Merkle Trees to verify integrity of transactions in a block

## How It Works

### Tokens and Staking (POS algorithm)
Tokens flow like a currency while stakes act as a measure of voting power in the consensus process
Each doctor starts with a certain number of tokens.  
- Staking: Doctors must stake at least 10 tokens to become eligible validators  
- Validator Selection: When a block is created, a validator is chosen randomly, with the probability weighted by the size of their stake  
- Reward: The chosen validator earns 10 tokens for successfully validating a block  
- Penalty: Planned feature where malicious validators can lose their stake  

### Adding a New Medical Record (Doctor Flow)
1. A doctor fills out the "Add Record" form in the Streamlit frontend, providing patient ID and prescription text  
2. A digital signature is created using the doctor’s private key  
3. The prescription is encrypted using a shared symmetric key for that doctor-patient pair  
4. A transaction is built and added to pending_transactions.json  
5. When three pending transactions are collected, the blockchain logic triggers block creation  
6. The PoS module selects a validator from the active stakers  
7. A new block is assembled, including a merkle root and block hash  
8. The block is appended to the chain, the validator is rewarded with tokens, and the blockchain is saved to blockchain.json  

### Viewing Records (Patient Flow)
1. A patient selects "View Records" in the frontend  
2. The system loads the blockchain and pending transactions  
3. Transactions matching the patient ID are collected  
4. The corresponding doctor-patient shared key is retrieved  
5. The data is decrypted to reveal the original prescription  
6. All records are displayed in the frontend, showing the full medical history  

## Project Structure
- consensus/pos.py: Proof of Stake logic (validator selection, rewards, penalties)  
- consensus/staking.py: Token staking and management  
- models/block.py, blockchain.py: Block and blockchain definitions  
- storage/record_manager.py: Record handling (add, retrieve, decrypt)  
- crypto/: Digital signatures, hashing, encryption, merkle tree utilities  
- frontend.py: Streamlit interface for doctors, patients, and admins  

