# Lamport signature implementation

import secrets
import argparse
import sys
from hashlib import sha256
from unittest.mock import patch
from io import StringIO


class _KeyPair:

    """ _KeyPair is only intended to be used as an internal Type """

    def __init__(self, zeropriv, onepriv, zeropub, onepub):
        self.zeropriv = zeropriv
        self.onepriv  = onepriv 
        self.zeropub  = zeropub 
        self.onepub   = onepub  

    @property
    def priv(self):
        return [self.zeropriv, self.onepriv]

    @property
    def pub(self):
        return [self.zeropub, self.onepub]


def generate_keys(filename='keys.txt'):
    """ 
    Generates and returns a public and private key pair

    """
    zeropriv = [secrets.token_hex(32) for i in range(256)]                      
    onepriv  = [secrets.token_hex(32) for i in range(256)]
    zeropub  = [sha256(block.encode()).hexdigest() for block in zeropriv]
    onepub   = [sha256(block.encode()).hexdigest() for block in onepriv]

    return _KeyPair(zeropriv, onepriv, zeropub, onepub)


def  sign_message(priv, msg):
    """
    signs a message using the given decoded private key

    accepts: msg: string

    returns signature: [256] 
    """

    bin_msg = message_to_hashed_binary(msg) 

    if len(priv[0]) != 256 and len(priv[1]) != 256:
        raise Exception('Invalid private key length')

    signed_message = []
    for i, bit in enumerate(bin_msg):
        block = priv[bit][i]
        signed_message.append(block)
         
    return signed_message


def verify_signature(pub, msg, sig):
    bin_msg = message_to_hashed_binary(msg)

    for i, block in enumerate(sig):
        hashed_block = sha256(block.encode()).hexdigest()
        if hashed_block != pub[bin_msg[i]][i]:
            return False

    return True
    


""""""""""""""""""""""""""
"""  Utility functions """
""""""""""""""""""""""""""

def export_key(key, filename):
    with open(filename, 'w') as f:
        f.writelines(key[0])
        f.writelines(key[1])


def export_key_pair(keypair, pub_file='pub.key', priv_file='priv.key'):
    export_key(keypair.pub, pub_file)
    export_key(keypair.priv, priv_file)


def parse_key(filename):
    key = [[],[]]
    start = 0
    end = 64  

    with open(filename, 'r') as f:
        key_str = f.read()

    if len(key_str) != 2 * 64 * 256: # 2 rows, 265 blocks, 64 char long blocks. 
        raise Exception('Invalid private key length')
    
    for i in range(256):
        key[0].append(key_str[start:end])
        start = end
        end += 64
        
    for i in range(256):
        key[1].append(key_str[start:end])
        start = end
        end += 64

    return key


def parse_key_pair(pub_file, priv_file):
    priv = parse_key(priv_file)
    pub = parse_key(pub_file)

    return  _KeyPair(priv[0], priv[1], pub[0], pub[1])


def str_to_sig(signature_str):
    stripped_sig = signature_str.rstrip()
    if len(stripped_sig) != 256 * 64:
        raise Exception('Invalid signature length')
    sig = []
    for i in range(0, len(stripped_sig), 64):
        sig.append(stripped_sig[i: i + 64])
    return sig 

def hex_to_bin_list(hex_string):
    results = []
    b = bytes.fromhex(hex_string)
    for byte in b:
        i = 128
        while(i > 0):
            if byte & i != 0:
                results.append(1)
            else:
                results.append(0)
            i = int(i/2)
    return results


def message_to_hashed_binary(msg):
    hashed_msg = sha256(msg.encode()).hexdigest()
    return hex_to_bin_list(hashed_msg)



""""""""""""""""""""""""""
"""  CLI functionality """
""""""""""""""""""""""""""

def cli(args):

    parser = argparse.ArgumentParser(description="Command-line interface for lamport-256")
    parser.add_argument('mode', choices=['generate_keys', 'sign', 'verify'], 
                        help="Command to run with lamport-256")
    parser.add_argument('--priv', type=str, metavar='', 
            help="sign: location of private key, generate_keys: where to put key")
    parser.add_argument('--pub', type=str, metavar='', 
                        help="Location of private key")
    parser.add_argument('--msg', type=str, metavar='',
                        help="Message or message file to sign or verify")
    parser.add_argument('--sig', type=str, metavar='',
                        help="Location of signature to verify")
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args(args)

    if args.mode == 'generate_keys':
        if  args.pub is None:
            args.pub  = 'pub.key' 
        if args.priv is None:
            args.priv = 'priv.key' 
        keypair = generate_keys()
        export_key_pair(keypair, args.pub, args.priv)
        if args.verbose:
            sys.stdout.write('Keys written to files ' + args.pub + ' & ' + args.priv +'\n')

    if args.mode == 'sign':
        if args.msg is None:
            parser.error('you need to attach a --msg to sign')
        if args.priv is None:
            parser.error('you need to attach a --priv to form a signature')

        try:
            f = open(args.msg, 'r')
            msg = f.read().strip()
            f.close()
        except:
            msg = args.msg

        print(''.join(sign_message(parse_key(args.priv), msg)))

    if args.mode == 'verify':
        if args.msg is None:
            parser.error('you need to attach a --msg to verify')
        if args.pub is None:
            parser.error('you need to attach a public key, using flag --pub, to verify')   
        if args.sig is None:
            parser.error('you need to attach a signature, using flag --sig, to verify')

        try:
            f = open(args.msg, 'r')
            msg = f.read().strip()
            f.close()
        except:
            msg = args.msg

        with open(args.sig, 'r') as f:
            sig = str_to_sig(f.read().strip())

        if verify_signature(parse_key(args.pub), msg, sig):
            print('valid')
        else:
            print('invalid')
            sys.exit(1)


            
if __name__ == "__main__":
    cli(sys.argv[1:])
