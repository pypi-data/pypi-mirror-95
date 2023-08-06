'''
Utility functions: conversions, hashing, etc.
text=equivalent utf-8 text
hex=hex string
bytes=bytes
'''
import binascii
import hashlib

'''
Convert ASCII text to hex equivalent
'''
def text_to_hex(string):
    bstring = string.encode('utf-8')
    return binascii.hexlify(bstring).decode('utf-8')

'''
Convert hex to ASCII text equivalent
'''
def hex_to_text(hex):
    bstring = binascii.unhexlify(hex)
    return bstring.decode('utf-8')

'''
Convert from bytes to hex
'''
def bytes_to_hex(bytes):
    return binascii.hexlify(bytes).decode('utf-8')

'''
Convert from hex to bytes
'''
def hex_to_bytes(hex):
    return binascii.unhexlify(hex)

'''
Get RIPEMD digest from input bytes
TODO: expand to check input and convert to bytes first?!
'''
def ripemd160(ibytes):
    ripemd_algo = hashlib.new('ripemd160')
    ripemd_algo.update(ibytes)
    return ripemd_algo.digest()

'''
Convert from hex to int
'''
def hex_to_int(hex):
    return int(hex, 16)


'''
Get chain type (string with blockchain plus whether it is testing or not. Blochchains
supported are 'bitcoin' and 'litecoin'.
'''
def get_chain_type(chain, testnet):
    if chain not in ['bitcoin', 'litecoin']:
       return None

    if(testnet):
        return chain + '_testnet'
    else:
        return chain

'''
Get the chain and whether it is for testing given a chain type
'''
def get_chain_and_testnet(chain_type):
    chain = chain_type.split('_')
    if len(chain == 2):
       return chain[0], True
    else:
       return chain[0], False



