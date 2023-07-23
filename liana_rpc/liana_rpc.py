import logging
import subprocess
import json
import time

from liana_rpc.utils.rpc import UnixDomainSocketRpc

log = logging.getLogger()


def get_liana_instances():
    command = 'ps -aux | grep lianad'
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    if result.returncode == 0:
        out = result.stdout
        out = out.splitlines()
        
        if len(out) > 2:
            liana_sockets = []
            out = out[:-2]
            for i in out:
                liana_sockets.append("/".join(i.split(' ')[-1].split('/')[:-1]) + '/lianad_rpc')
            return liana_sockets

    return []


def psbt_to_txid(psbt):
    command = f"bitcoin-cli decodepsbt {psbt}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    if result.returncode == 0:
        txid = json.loads(result.stdout)['tx']['txid']
        return txid
    else:
        data = {'error': f'Cannot decode psbt: {psbt}'}
        return data
   
    
def rawtx_to_txid(rawtx):
    command = f"bitcoin-cli decoderawtransaction {rawtx}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    if result.returncode == 0:
        txid = json.loads(result.stdout)['txid']
        return txid
    else:
        data = {'error': f'Cannot decode rawtx: {rawtx}'}
        return data


class LianaRPC:
    """
    This class is a RPC client for connect to Liana daemon (lianad) from wizarsardine
    https://github.com/wizardsardine/liana/blob/master/doc/API.md
    """
    
    def __init__(self, path=None):
        """
        :param path: the path to the socket file (usually  ~/.liana/<chain>/lianad_rpc), lianad might to be already
        running before start LianaRPC instance.
        """
        
        logger = logging.getLogger()
        
        if path is None:
            sockets = get_liana_instances()
            if len(sockets) == 1:
                self.path = sockets[0]
            elif len(sockets) == 0:
                raise Exception("We don't find a running instance of lianad, you might start it prior to instantiate the class or supply the path to socket")
            else:
                msg = "There is several running instances of lianad, you might specify the socket you want to connect:\n"
                for i in sockets:
                    msg += f"{i}\n"
                raise Exception(msg)
        else:
            self.path = path
        self.rpc = UnixDomainSocketRpc(self.path)
        
    def get_info(self):
        """
        Return general information about the daemon
        """
        ret = self.rpc.call('getinfo')
        if 'block_height' in ret.keys():
            return ret
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
        
    def stop_lianad(self):
        """
        Stops liana daemon.
        """
        ret = self.rpc.call('stop')
        if ret == {}:
            return {'ok': True}
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def get_new_address(self):
        """
        Get a new receiving address
        """
        ret = self.rpc.call('getnewaddress')
        if 'address' in ret.keys():
            return ret['address']
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret

    def list_coins(self):
        """
        List all wallet transaction outputs.
        """
        ret = self.rpc.call('listcoins')
        if 'coins' in ret.keys():
            return ret['coins']
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def list_unspent_coins(self):
        """
        Return the list of unspent coins
        """
        ret = self.list_coins()
        if type(ret) is not list:
            return ret
        unspent_coins = []
        for i in ret:
            if not i['spend_info']:
                unspent_coins.append(i)
        return unspent_coins
    
    def list_spend_coins(self):
        """
        Return the list of spend coins
        """
        ret = self.list_coins()
        if type(ret) is not list:
            return ret
        spend_coins = []
        for i in ret:
            if i['spend_info']:
                spend_coins.append(i)
        return spend_coins

    def create_psbt(self, coins: [], outputs: {}, feerate: int):
        """
        Create a PSBT from unspend coins list.
        
        :param coins: list of coins to spend in the form of [<tx_id_1>:<output_id>, <tx_id_2>:<output_id>, ]
        :param outputs: dict of outputs in the form of {<address>:<amount>, <address>:<amount>,}
        :param feerate: feerate in sats/VBytes
        
        Return Base64 encoded PSBT.
        """
        params = {
            'destinations': outputs,
            'outpoints': coins,
            'feerate': feerate,
        }
        ret = self.rpc.call('createspend', params)
        if 'psbt' in ret.keys():
            return ret['psbt']
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def upate_psbt(self, psbt: str):
        """
        Store the PSBT of a Spend transaction in database, updating it if it already exists.
        :param psbt: Base64-encoded PSBT of a Spend transaction.
        """
        ret = self.rpc.call('updatespend', {'psbt': psbt})
        if ret == {}:
            return {'ok': True}
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def list_psbt(self):
        """
        List PSBT stored in Liana DB.
        """
        ret =  self.rpc.call('listspendtxs')
        if 'spend_txs' in ret.keys():
            return ret['spend_txs']
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def del_psbt(self, txid: str):
        ret = self.rpc.call('delspendtx', {'txid': txid})
        if ret == {}:
            return {'ok': True}
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def broadcast_psbt(self, txid):
        ret = self.rpc.call('broadcastspend', {'txid': txid})
        if ret == {}:
            return {'ok': True}
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def start_rescan(self, timestamp):
        ret = self.rpc.call('startrescan', {'timestamp': timestamp})
        if 'error' in ret.keys() and ret['error']['message'] == 'There is already a rescan ongoing. Please wait for it to complete first.':
            return {'rescanning': True}
        else:
            return {}
    
    def list_confirmed_tx(self, start: int = None, end: int = None, limit: int = 100):
        if not start:
            start = 1231006505
            
        if not end:
            end = round(time.time())
            
        params = {
            'start': start,
            'end': end,
            'limit': limit,
        }
        
        ret = self.rpc.call('listconfirmed', params)
        if 'transactions' in ret.keys():
            return ret['transactions']
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
        
    def fetch_tx(self, txid):
        """
        Retrieve a single transaction given its txid.
        """
        ret = self.list_txs([txid])
        if type(ret) is list:
            return ret[0]
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def list_txs(self, txs: []):
        """
        Retrieves transactions with the given txids.
        :param txs: List of txids in the form of [<txid>, <txid>, <txid>,]
        """
        
        ret = self.rpc.call('listtransactions', {'txids': txs})
        if 'transactions' in ret.keys():
            return ret['transactions']
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
    
    def create_recovery_psbt(self, address, feerate, timelock=0):
        params = {
            'address': address,
            'feerate': feerate,
            'timelock': timelock,
        }
        ret = self.rpc.call('createrecovery', params)
        if 'psbt' in ret.keys():
            return ret['psbt']
        elif 'error' in ret.keys():
            return {'error': ret['error']}
        else:
            return ret
        

        
