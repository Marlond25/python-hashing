from hashlib import sha256
import json
import time


class Block:


    def __init__(self, index, transactions, timestamp, previousHash):
        """
            Constructor for Block
            :param index: Unique ID of the Block
            :param transaction: List of transactions (data)
            :param timestamp: Time of generation of the Block
            :param previousHash: Hash of the previous block in the chain
            which this block is part of
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previousHash =  previousHash


    def computeHash(self):
        """
            Reurns the hash of the block instance
            by first converting it into JSON string
        """
        blockString = json.dumps(self.__dict__, sort_keys = True)
        return sha256(blockString.encode()).hexdigest()


class BlockChain:
    """
        Constructor for BlockChain
    """

    def __init__(self):
        # difficulty of pow algoritm
        difficulty = 2
        self.unconfirmedTransactions = []
        self.chain = []
        self.createGenesisBlock()


    def createGenesisBlock(self):
        """
            Generates the genesis block appending it to the chain.
            index: 0
            previousHash: 0
            hash: valid hash
        """
        genesisBlock = Block(0, [], time.time(), "0")
        genesisBlock.hash = genesisBlock.computeHash()
        self.chain.append(genesisBlock)


    @property
    def lastBlock(self):
        """
            Retrieve the most recent block in the chain
            The chain will always consist of at least one block
        """
        return self.chain[-1]


    def proofOfWork(self, block):
        """
            tries different values of the nonce to get a hash
            that satisfies the difficult criteria
        """

        block.nonce = 0

        computedHash = block.computeHash()
        while not computedHash.startswith("0" * BlockChain.difficulty):
            block.nonce += 1
            computedHash = block.computeHash()
        return computedHash


    def addBlock(self, block, proof):
        """
            Adds a block to the chain after validation
            Validation:
            *Check if the proof is valid
            *hash of previous block = previousHash of current block
        """
        previousHash = self.lastBlock.hash

        if previousHash != block.previousHash:
            return False

        if not BlockChain.isValidProof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True


    def isValidProof(self, block, blockHash):
        """
            Check if blockHash is valid hash of block and satisfies
            the difficulty parameter
        """
        return (blockHash.startswith("0" * BlockChain.difficulty) and
                blockHash == block.computeHash())


    def addNewTransaction(self, transaction):
        self.unconfirmedTransactions.append(transaction)


    def mine(self):
        """
            Serves as an interface to add the pending transactions
            to the block chain by adding them to the block
            and figuring out proof of work
        """
        if not self.unconfirmedTransactions:
            return false

        lastBlock = self.lastBlock

        newBlock = Block(index=lastBlock.index+1,
                        transactions=self.unconfirmedTransactions,
                        timestamp=time.time(),
                        previousHash=lastBlock.hash)
        proof = self.proofOfWork(newBlock)
        self.addBlock(newBlock, proof)
        self.unconfirmedTransactions = []
        return newBlock.index
