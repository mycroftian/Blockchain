from crypto.hashing import create_hash

# Build a Merkle Tree and return the root hash
def build_merkle_tree(transactions_list):
    hash_list = [] 
    for transaction in transactions_list:
        hash_list.append(create_hash(transaction))
    
    while len(hash_list) > 1:
        temp_list = []
        for i in range(0, len(hash_list), 2):
            if i + 1 < len(hash_list):
                combined_hash = create_hash(hash_list[i] + hash_list[i + 1])
            else:
                combined_hash = create_hash(hash_list[i] + hash_list[i])
            temp_list.append(combined_hash)
        hash_list = temp_list

    return hash_list[0]
