'''
Functions related to network services
'''
import sys
import queue
import requests
from threading import Thread
import bitcoinrpc.authproxy as proxy

import blockchain_certificates.utils as utils

import logging
log = logging.getLogger( 'CRED Corelib' )


'''
Gets all the op_return hexes stored from the specified txid (used to issue the
certificates. Get tx before issuance (for checking revoked addresses) and after
issuance (for checking revoked batches and/or certificates
'''
def get_all_op_return_hexes(address, txid, blockchain_services, chain, testnet=False):

    chain_type = utils.get_chain_type(chain, testnet)
    if chain_type is None:
        raise ValueError("Unsupported blockchain {} - {}".format(chain, testnet))

    services = blockchain_services[chain_type]['services']
    required_successes = blockchain_services[chain_type]['required_successes']

    # instantiate a Queue to get thread exceptions
    my_queue = queue.Queue()

    successes = 0
    threads_results = {list(s.keys())[0]:{'success':False, 'before':[], 'after':[]} for s in services}
    final_results = []

    # threads to call all functions/APIs simultaneously
    threads = []
    for s in services:
        name = list(s.keys())[0]
        target = globals()["get_" + name + "_op_return_hexes"]
        thread = Thread(target=target, args=[my_queue, address, txid, threads_results,
                                             name, s[name], testnet])
        thread.start()
        threads.append(thread)

    # execute threads
    for t in threads:
        t.join()

    thread_exceptions = []
    while not my_queue.empty():
        thread_exceptions.append(my_queue.get())

    # logic that makes sure that there is enough decentralization and
    # redundancy in the results; currently ensure that we have
    # required_successes identical results returned from all the services
    for s in services:
        name = list(s.keys())[0]
        if threads_results[name]['success']:
            successes += 1
            final_results.append(threads_results[name])
            if successes >= required_successes:
                break

    if successes >= required_successes:
        if len(final_results) > 1:
            for i in range(1, len(final_results)):
                if final_results[0] != final_results[i]:
                    raise ValueError("API services produced different results",
                                    thread_exceptions)
        return final_results[0]['before'], final_results[0]['after']
    else:
        raise ValueError("Not enough API services results", thread_exceptions)


def get_op_return_data_from_script(script):
    # when > 75 op_pushdata1 (4c) is used before length
    if script.startswith('6a4c'):
        # 2 for 1 byte op_return + 2 for 1 byte op_pushdata1 + 2 for 1 byte
        # data length
        ignore_hex_chars = 6
    else:
        # 2 for 1 byte op_return + 2 for 1 byte data length
        ignore_hex_chars = 4

    return script[ignore_hex_chars:]



'''
Uses blockcypher's free API (note there is a limit of around a thousand
validations per day
'''
def get_blockcypher_op_return_hexes(queue, address, txid, results, key, conf, testnet=False):

    try:
        #print("blockcypher start")
        blockcypher_url = 'http://api.blockcypher.com/v1/btc'
        network = 'test3' if testnet else 'main'

        address_txs_url = '{}/{}/addrs/{}/full'.format(blockcypher_url, network, address)

        params = { 'limit': 50 }  # max tx per request on blockcypher
        address_txs = requests.get(address_txs_url, params=params).json()

        if 'error' in address_txs:
            raise ValueError(address_txs['error'])

        new_start_height = address_txs['txs'][-1]['block_height']
        all_relevant_txs = address_txs['txs']

        while 'hasMore' in address_txs and address_txs['hasMore']:
            params['before'] = new_start_height
            address_txs = requests.get(address_txs_url, params=params).json()
            # this is required due to a bug in blockcypher where if it has 51
            # txs it returns them all in the first request above but hasMore is
            # still true thus breaks when we try to get [-1] of the empty list
            if len(address_txs['txs']):
                new_start_height = address_txs['txs'][-1]['block_height']
                # results are newest first
                all_relevant_txs = all_relevant_txs + address_txs['txs']

        data_before_issuance = []
        data_after_issuance = []
        found_issuance = False
        for tx in all_relevant_txs:
            # only consider txs that have at least one confirmation
            if tx['confirmations'] <= 0:
                continue

            # tx hash needs to be identical with txid from proof and that is the
            # actual issuance
            if tx['hash'] == txid:
                found_issuance = True

            outs = tx['outputs']

            for o in outs:
                # get op_return_hex, if any, and exit
                if o['script'].startswith('6a'):
                    data = get_op_return_data_from_script(o['script'])

                    if not found_issuance:
                        # to check certs revocations we can iterate this list in reverse!
                        data_after_issuance.append(data)
                    else:
                        # current issuance is actually the first element of this list!
                        # to check for addr revocations we can iterate this list as is
                        data_before_issuance.append(data)

        if not found_issuance:
            raise ValueError("Txid for issuance not found in address' transactions")

        results[key]['before'] = data_before_issuance
        results[key]['after'] = data_after_issuance
        results[key]['success'] = True

        #print("blockcypher end")
    except Exception as e:
        log.error("Blockcypher Thread:" + sys.exc_info().__str__())

        # add to queue to be visible to parent
        queue.put(["Blockcypher Thread:", sys.exc_info()])
        #print("blockcypher exception clause end")



#'''
#Uses a fully indexed bitcoin core node (txindex=1) to get all transactions of
#the address. Note this will work ONLY if the addresses are wallet transactions.
#'''
# TODO This method is not very useful after all. TO DELETE?
#def get_bitcoincore_op_return_hexes(address, txid, results, key, conf,
#                                    testnet=False):
#    try:
#
#        url = conf['full_url']
#        rpc_conn = AuthServiceProxy(url)
#        addr_txs = rpc_conn.listreceivedbyaddress(0, True, True, address)[0]['txids']
#
#        # create batch jsonrpc to get all the txs data for each txid above
#        get_tx_commands = [ [ "getrawtransaction", trans_id, True] for trans_id in addr_txs ]
#        all_unsorted_relevant_txs = rpc_conn.batch_(get_tx_commands)
#
#        # sort transactions with blocktime desc (i.e. newest first)
#        all_relevant_txs = sorted(all_unsorted_relevant_txs, key=lambda x:
#                                  hash(x['blocktime']), reverse=True)
#
#        data_before_issuance = []
#        data_after_issuance = []
#        found_issuance = False
#        for tx in all_relevant_txs:
#            # tx hash needs to be identical with txid from proof and that is the
#            # actual issuance
#            if tx['txid'] == txid:
#                found_issuance = True
#
#            outs = tx['vout']
#            for o in outs:
#                # get op_return_hex, if any, and exit
#                if o['scriptPubKey']['hex'].startswith('6a'):
#                    data = get_op_return_data_from_script(o['scriptPubKey']['hex'])
#
#                    if not found_issuance:
#                        # to check certs revocations we can iterate this list in reverse!
#                        data_after_issuance.append(data)
#                    else:
#                        # current issuance is actually the first element of this list!
#                        # to check for addr revocations we can iterate this list as is
#                        data_before_issuance.append(data)
#
#        if not found_issuance:
#            raise ValueError("Txid for issuance not found in address' transactions")
#
#        results[key]['before'] = data_before_issuance
#        results[key]['after'] = data_after_issuance
#        results[key]['success'] = True
#
#    except Exception as e:
#        # TODO log error -- print(e)
#
#        # don't break -- ignore result of this thread
#        pass




'''
Uses a btcd node that contains address indexes (txindex=1, addrindex=1) to get
all transactions of the address.
'''
def get_btcd_op_return_hexes(queue, address, txid, results, key, conf, testnet=False):

    try:
        #print("btcd start")
        url = conf['full_url']
        rpc_conn = proxy.AuthServiceProxy(url)
        all_relevant_txs = rpc_conn.searchrawtransactions(address, 1, 0, 10000000, 0, True)

        data_before_issuance = []
        data_after_issuance = []
        found_issuance = False
        for tx in all_relevant_txs:
            # only consider txs that have at least one confirmation
            # note that tx will be None if confirmations is 0
            if not tx.get('confirmations', 0):
                continue

            # tx hash needs to be identical with txid from proof and that is the
            # actual issuance
            if tx['txid'] == txid:
                found_issuance = True

            outs = tx['vout']
            for o in outs:
                # get op_return_hex, if any, and exit
                if o['scriptPubKey']['hex'].startswith('6a'):
                    data = get_op_return_data_from_script(o['scriptPubKey']['hex'])

                    if not found_issuance:
                        # to check certs revocations we can iterate this list in reverse!
                        data_after_issuance.append(data)
                    else:
                        # current issuance is actually the first element of this list!
                        # to check for addr revocations we can iterate this list as is
                        data_before_issuance.append(data)

        if not found_issuance:
            raise ValueError("Txid for issuance not found in address' transactions")

        results[key]['before'] = data_before_issuance
        results[key]['after'] = data_after_issuance
        results[key]['success'] = True

        #print("btcd end")

    except Exception as e:
        log.error("Btcd Thread:" + sys.exc_info().__str__())

        # add to queue to be visible to parent
        queue.put(["Btcd Thread:", sys.exc_info()])
        #print("btcd exception clause end")



'''
Uses a custom API to get all transactions of the address in the same format
that btcd/ltcd returns.
'''
def get_custom_api_op_return_hexes(queue, address, txid, results, key, conf, testnet=False):

    try:
        #print("btcd start")
        url = conf['full_url']

        address_txs_url = '{}/{}'.format(url, address)
        all_relevant_txs = requests.get(address_txs_url).json()

        if 'error' in all_relevant_txs:
            raise ValueError(all_relevant_txs['error'])

        data_before_issuance = []
        data_after_issuance = []
        found_issuance = False
        for tx in all_relevant_txs:
            # only consider txs that have at least one confirmation
            # note that tx will be None if confirmations is 0
            if not tx.get('confirmations', 0):
                continue

            # tx hash needs to be identical with txid from proof and that is the
            # actual issuance
            if tx['txid'] == txid:
                found_issuance = True

            outs = tx['vout']
            for o in outs:
                # get op_return_hex, if any, and exit
                if o['scriptPubKey']['hex'].startswith('6a'):
                    data = get_op_return_data_from_script(o['scriptPubKey']['hex'])

                    if not found_issuance:
                        # to check certs revocations we can iterate this list in reverse!
                        data_after_issuance.append(data)
                    else:
                        # current issuance is actually the first element of this list!
                        # to check for addr revocations we can iterate this list as is
                        data_before_issuance.append(data)

        if not found_issuance:
            raise ValueError("Txid for issuance not found in address' transactions")

        results[key]['before'] = data_before_issuance
        results[key]['after'] = data_after_issuance
        results[key]['success'] = True

        #print("btcd end")

    except Exception as e:
        log.error("custom_api thread:" + sys.exc_info().__str__())

        # add to queue to be visible to parent
        queue.put(["custom_api thread:", sys.exc_info()])
        #print("btcd exception clause end")



'''
Uses a ltcd node that contains address indexes (txindex=1, addrindex=1) to get
all transactions of the address.
'''
def get_ltcd_op_return_hexes(queue, address, txid, results, key, conf, testnet=False):

    try:
        #print("ltcd start")
        url = conf['full_url']
        rpc_conn = proxy.AuthServiceProxy(url)
        all_relevant_txs = rpc_conn.searchrawtransactions(address, 1, 0, 10000000, 0, True)

        data_before_issuance = []
        data_after_issuance = []
        found_issuance = False
        for tx in all_relevant_txs:
            # only consider txs that have at least one confirmation
            # note that tx will be None if confirmations is 0
            if not tx.get('confirmations', 0):
                continue

            # tx hash needs to be identical with txid from proof and that is the
            # actual issuance
            if tx['txid'] == txid:
                found_issuance = True

            outs = tx['vout']
            for o in outs:
                # get op_return_hex, if any, and exit
                if o['scriptPubKey']['hex'].startswith('6a'):
                    data = get_op_return_data_from_script(o['scriptPubKey']['hex'])

                    if not found_issuance:
                        # to check certs revocations we can iterate this list in reverse!
                        data_after_issuance.append(data)
                    else:
                        # current issuance is actually the first element of this list!
                        # to check for addr revocations we can iterate this list as is
                        data_before_issuance.append(data)

        if not found_issuance:
            raise ValueError("Txid for issuance not found in address' transactions")

        results[key]['before'] = data_before_issuance
        results[key]['after'] = data_after_issuance
        results[key]['success'] = True

        #print("ltcd end")

    except Exception as e:
        log.error("Ltcd Thread:" + sys.exc_info().__str__())

        # add to queue to be visible to parent
        queue.put(["Ltcd Thread:", sys.exc_info()])
        #print("ltcd exception clause end")






'''
Check all issuer verification methods in parallel.
'''
def check_issuer_verification_methods(issuer_address,
                                      issuer_verification, testnet):
    methods = issuer_verification
    threads_results = {list(m.keys())[0]:{ 'success':False, 'url':None } for m in methods}

    # threads to call all functions/APIs simultaneously
    threads = []
    for m in methods:
        name = list(m.keys())[0]
        target = globals()["check_" + name + "_verification_method"]
        thread = Thread(target=target, args=[issuer_address, threads_results, name,
                                             m[name], testnet])
        thread.start()
        threads.append(thread)

    # execute threads
    for t in threads:
        t.join()

    return threads_results


'''
Verify that issuing address exists in the issuer domain.
Note that the end-user should confirm that the domain is indeed the issuers.
'''
def check_domain_verification_method(address, results, key, conf, testnet):
    try:

        domain = conf['url']
        url = domain + "/cred.txt"
        cred_txt_file = requests.get(url)

        # set domain in results
        results[key]['url'] = domain

        if cred_txt_file.status_code == 200:
            if address in cred_txt_file.text:
                results[key]['success'] = True

    except Exception as e:
        # TODO log error -- print(e)

        # don't break -- ignore result of this thread
        pass


'''
Verify that issuing address exists in the issuer's github account using a gist.
Note that the end-user should confirm that the github account is indeed the issuer's.
'''
def check_github_verification_method(address, results, key, conf, testnet):
    try:

        user = conf['user']
        gist_id = conf['gist_id']
        url = "https://gist.githubusercontent.com/" + user + "/" + gist_id + "/raw"
        cred_txt_file = requests.get(url)

        # set gist url in results
        results[key]['url'] = url

        if cred_txt_file.status_code == 200:
            if address in cred_txt_file.text:
                results[key]['success'] = True

    except Exception as e:
        # TODO log error -- print(e)

        # don't break -- ignore result of this thread
        pass



'''
Verify that issuing address is managed by block.co.
This means that the issuer name has been verified by block.co
'''
def check_block_co_verification_method(address, results, key, conf, testnet):
    try:

        if testnet:
            url = 'https://test-api.block.co/auth/verify-address/{}/'.format(address)
        else:
            url = 'https://api.block.co/auth/verify-address/{}/'.format(address)
        res = requests.get(url)

        if res.status_code == 200:
            results[key]['success'] = True

    except Exception as e:
        # TODO log error -- print(e)

        # don't break -- ignore result of this thread
        pass
