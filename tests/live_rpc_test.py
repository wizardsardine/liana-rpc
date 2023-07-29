import pytest
import time

from liana_rpc.liana_rpc import LianaRPC, get_liana_instances, psbt_to_txid, rawtx_to_txid, decode_tx


@pytest.fixture(scope='session')
def liana():
    socket = get_liana_instances()[0]
    return LianaRPC(socket)


def test_psbt_to_txid():
    psbt = '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'
    txid = psbt_to_txid(psbt, network='signet')
    
    assert txid == '41bb1efaa164109ca8094e1215a7a29ae4a509d85218e92604e4b03d0f159033'


def test_rawtx_to_txid():
    rawtx = '02000000000109399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440700000000fdffffffdc3a444b9b9232f6f79ccf1bcb67bdc53f27fdd00f318505ada98f5dd419743b0100000000fdffffff94c9408f0a8031b5e827233d0c65332cb7d0c95f937e3a1b12660036fb9f2f5a0000000000fdffffff90be24c5fdc0c3c207f3c97d3710b90449a5996f1989b5a6bf8afe71b83e864a0000000000fdffffff9da736317b8ce41a9dfdbccd1e95bd7e1e4daf8c7ef3abf24387b553fd7d22a40100000000fdffffff399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440200000000fdffffff399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440300000000fdffffff399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440400000000fdffffff399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440500000000fdffffff0240420f0000000000220020afbbcb5ff084cae0355b57fc470ec8a6769b3e97c7e1aecfa266a08b8a79ee25a14f460000000000220020381f95a37678490f2767f85a4d2e49318e5f0d45ae0878adaad6a85b87aaab7d05004730440220656becace2eb1a1d544d7621806a4274d37a82da7cefbb5aa3dda7df3cd00bd802204fb4a0d2d0d3710dc025489124b5c3ee2db46f969c7453447a4a7b1dfbd259990147304402201798bf6b51ff779621dc892ffd90f8cd40f50cb074629cd5b65cf714daf6187f022024b24b075d668bdaf986b8da95b8a337d7a00f5f2bedb0f2781c148958f9e7110100846376a91486863f443b074f2dd1aa4b0bb46d5f99b849247988ad0114b26752210326a0c556e5b89902bbf933637958eeb506c757b39b91dc7ab2302f7c2b6504aa2102b0fd6e6f4e5ff916637a20a08a69fdc642df6960db01ce34aa2c3c5978d8ce9252ae736476a914935c015b1fcac698c9bc6b605477bf9e4b100cb488ad5ab26868050047304402200acde2fc9ee6c991851b4fc66e791591017e356dc0c8d8922bee3614801bde09022014b34de017e763bd195f8d2f3c46118a8364f4074b98f82006dc3133606f0fab01483045022100a23b79fd96e505c22c3c37eab7501efadfc8fee030aca136e5998200622cd88a02207f81466c5edf5568047ce0ab451e8a0181c3d9de3ebfc84209bebfc5371299df0100846376a914f7ddb806c825ec1e5a812c5e239df8b1149aef9688ad0114b267522102f066562208fda7d160554cb518941281ef85ef1b3ca82ca2d414ebdccfbb0a53210241abc970c8ae67cee2946b2ccc22896acdb604263a998dc22219060b6e61fb7d52ae736476a914bbca9f734ac7bebe7f0fe2593f01cba73b669d4d88ad5ab2686805004730440220336dfec05ea9fc448d75a311f815521b3bc87403f2eba5177fa1fcc53d509ce3022060d9ac46f8429342ebc55c02d2af5a71bf9f98b0ccd6312aded79acb25a556ed0147304402205ea148caca34735da543cce134bef7d2e2f035de9668617f645ceb035dca833602202aa6fa2db7d66f91837069eb177a64fa9084e41a913764357219df455d6cde2e0100846376a9147d85739805576464fc4e3309d822ed50f1b7ddd388ad0114b267522102b8f1656e002fe2999bfa63a3bdb1a3f15f538e02c0790bb859ea01699a8ea5d621028d1afefc2fd4e4e9afc315bccf403188c8e6c0592e66a35bec11db6142f0831d52ae736476a914d76f9b70a59cc06f906af91f111068700692608088ad5ab268680500473044022013dbe9a1d851b69ce81693f0976150cccbe1451704b10519fab3d67f835d308102207f07314f2a102b2b2121213038f2ffbd9efccaa8c3eb679e9ae64c55427de5b80147304402207b022859482f2431060eb8fe5c39a1c7205af1b61c989bf6a2e08de47ea0c89e02202ea8d78ffae1b7ff4ae4615057d4d7d5783649aae2f99343e75a582fe34c50d30100846376a9148c1f531c0a25ebddce1d5e8fe7b7ed868305231788ad0114b267522103f56cd5c7203da0a38ad28f78b98948c0ea60c21d490c5c4ce26cc1c08da0e4d62102456439a9511f69bc635d4893484bd6e774d02d178eedbaf2d6a2d65c6795d6a652ae736476a914d32cf1fe1fce0eca02fa9f1c4a1a55ae9625743f88ad5ab268680500473044022039520b73cfe21d3ea50e916af7b8c89f1fca40db524473f0836aed9940a7cec80220549689c35653802bc9576bcd373ba4a27fc63d0ac260e9b4c76e5ba86ff0f9170147304402203825acda80285fa11d0d788c0120b7aae2a1ef0df6836a93d28fbeaabde561740220706022fdf2261ec942038dd3b0955f23d1f5667067fb6260bbe19792a18af2f90100846376a9141138c8c5df663ca226334cf443d1cdfabf45b38d88ad0114b2675221030d287dbb4eb74285f9261b32126a26db381faff7a4f255e8575ffc48dbf744782103314a8f8fc2a240ffd015930866f28ef78903240db5dcd462295720460bc020c352ae736476a9141269e81dd4f81eef566f22699569949f9f6999fb88ad5ab26868050047304402202d3b99853c05d79e9af22da2ac9dae27f652bb027900eb4259ab9e16a3b588b6022026bd7c837ad5c4ef1daceb61f78ad00ebd1ac7e3a56fa7576d7736b3783a9fdc01473044022100e08ce4e41201ecd2444f6968ee786d5a0121c047076c574da48e0aee456ecdc1021f5ca84e37a3951d755ed11d5b5f7d199a2eadbebc4003495ddd58c2c9a222b10100846376a914da0fad154bd25905ef43213dbe93a31b5211fc7c88ad0114b267522102fe6ed5df5e44df893840c9bffc5c1a100aad0f0e7ce68188a80f26545626960f21027f743df254973f6019d892e0a875e92f49ca5fbd65a52111e638c3411070d1cd52ae736476a91498d1e0b644f2e9102d6046833673007292b6f67588ad5ab26868050047304402205dd43da2535425e2c37fd1b2654c8e15318336a9849740ea4e9ffbf7d46f50d202207ce7e00e8c2efdb8f7238d560f5a5621846732bb4a30c53a416d7d7e26d69b76014730440220689ca9f0a2e30523f92a0e2f23ed06ee33c3d537d6075e53bdc58bd7efdbe8b202207908c0c29535c21e644410820baa2be5ff3312d45182c76402023bfda511b22c0100846376a9145d82a99eb4eaf194caa0487c5f693318a831a8d288ad0114b267522103a57742665c3e4d530dfb08a0f36dcb044f3a0f25ea6c4da0fe5e5ab387edc0632102d7839db83c80e3db30625d3d69e1529df63ceb235bc05738e99262eda9875a1652ae736476a91402ac8f193b745486ce3aafca88b81e426c1c9e9888ad5ab2686805004730440220174b5a26522b841a8102d1110d24edabb7193a731eed22fef6c9075fd0bdd8d4022045048b9f74534d513f731cca49f1e0d54d5913f47b302a6d18e4db8d07c7763001483045022100f9fca579602f8504b5b3ca830498086afeea2fb7248d5f2eafe3c4d8ccc98b2802201820c1bb79197935fcca791ac5d9c3ac16e1483a868954741932f510a2c41f2a0100846376a91475cd9524b70aebe6550fa612931ac009b52d722a88ad0114b267522103636ed78aba3b251b52b17c51a7b44fabcc4481b2b0bf0656a18ef9d5d97155252102092434b3c8db4394f46aa65eaf20b9841d50a8ec8d8662e7b40e105792be5c1852ae736476a914b0f2b2a5786ce38511c373858449795a3309954f88ad5ab26868050047304402201bad622af5e0da4e9975d5643fd1f9c03b5ae9dc7ce3a968f6488cc5dc1967d6022076e2efd84b1850fee260a8e4b2a354ba4d63e6ccdee170646856c7b68d5731f0014830450221008d205d5f723af95daf2d0542071b69f4eb5bc99254ca91a89d222a702b9f615302204937fc8450f06a40301e6f93a0c939e717373198819923b12344cdd53ed47ec00100846376a914f78e5361c3c847e3f4a555fa4682c1643b1a6de988ad0114b267522102e8ee6dd299285ac5628420da43b5f09f13e900315567f6812dc799cd10e846b821030f647bccc4e265d5c4b38935bec049e64b808c74d83137e9c877a5ac252a321352ae736476a91416b48b379db57850e3ee0e1873645c31662d4d3c88ad5ab2686800000000'
    txid = rawtx_to_txid(rawtx, network='signet')
    assert txid == '9b20145363703a3309166aa1af48d7907cc42dd98d49843ffb24ef909d1da108'
    
    
def test_decode_tx():
    rawtx = '02000000000109399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440700000000fdffffffdc3a444b9b9232f6f79ccf1bcb67bdc53f27fdd00f318505ada98f5dd419743b0100000000fdffffff94c9408f0a8031b5e827233d0c65332cb7d0c95f937e3a1b12660036fb9f2f5a0000000000fdffffff90be24c5fdc0c3c207f3c97d3710b90449a5996f1989b5a6bf8afe71b83e864a0000000000fdffffff9da736317b8ce41a9dfdbccd1e95bd7e1e4daf8c7ef3abf24387b553fd7d22a40100000000fdffffff399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440200000000fdffffff399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440300000000fdffffff399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440400000000fdffffff399e2eddae06d0e21e5303189e5b2c857f7168504b8e8974294a1e113c5850440500000000fdffffff0240420f0000000000220020afbbcb5ff084cae0355b57fc470ec8a6769b3e97c7e1aecfa266a08b8a79ee25a14f460000000000220020381f95a37678490f2767f85a4d2e49318e5f0d45ae0878adaad6a85b87aaab7d05004730440220656becace2eb1a1d544d7621806a4274d37a82da7cefbb5aa3dda7df3cd00bd802204fb4a0d2d0d3710dc025489124b5c3ee2db46f969c7453447a4a7b1dfbd259990147304402201798bf6b51ff779621dc892ffd90f8cd40f50cb074629cd5b65cf714daf6187f022024b24b075d668bdaf986b8da95b8a337d7a00f5f2bedb0f2781c148958f9e7110100846376a91486863f443b074f2dd1aa4b0bb46d5f99b849247988ad0114b26752210326a0c556e5b89902bbf933637958eeb506c757b39b91dc7ab2302f7c2b6504aa2102b0fd6e6f4e5ff916637a20a08a69fdc642df6960db01ce34aa2c3c5978d8ce9252ae736476a914935c015b1fcac698c9bc6b605477bf9e4b100cb488ad5ab26868050047304402200acde2fc9ee6c991851b4fc66e791591017e356dc0c8d8922bee3614801bde09022014b34de017e763bd195f8d2f3c46118a8364f4074b98f82006dc3133606f0fab01483045022100a23b79fd96e505c22c3c37eab7501efadfc8fee030aca136e5998200622cd88a02207f81466c5edf5568047ce0ab451e8a0181c3d9de3ebfc84209bebfc5371299df0100846376a914f7ddb806c825ec1e5a812c5e239df8b1149aef9688ad0114b267522102f066562208fda7d160554cb518941281ef85ef1b3ca82ca2d414ebdccfbb0a53210241abc970c8ae67cee2946b2ccc22896acdb604263a998dc22219060b6e61fb7d52ae736476a914bbca9f734ac7bebe7f0fe2593f01cba73b669d4d88ad5ab2686805004730440220336dfec05ea9fc448d75a311f815521b3bc87403f2eba5177fa1fcc53d509ce3022060d9ac46f8429342ebc55c02d2af5a71bf9f98b0ccd6312aded79acb25a556ed0147304402205ea148caca34735da543cce134bef7d2e2f035de9668617f645ceb035dca833602202aa6fa2db7d66f91837069eb177a64fa9084e41a913764357219df455d6cde2e0100846376a9147d85739805576464fc4e3309d822ed50f1b7ddd388ad0114b267522102b8f1656e002fe2999bfa63a3bdb1a3f15f538e02c0790bb859ea01699a8ea5d621028d1afefc2fd4e4e9afc315bccf403188c8e6c0592e66a35bec11db6142f0831d52ae736476a914d76f9b70a59cc06f906af91f111068700692608088ad5ab268680500473044022013dbe9a1d851b69ce81693f0976150cccbe1451704b10519fab3d67f835d308102207f07314f2a102b2b2121213038f2ffbd9efccaa8c3eb679e9ae64c55427de5b80147304402207b022859482f2431060eb8fe5c39a1c7205af1b61c989bf6a2e08de47ea0c89e02202ea8d78ffae1b7ff4ae4615057d4d7d5783649aae2f99343e75a582fe34c50d30100846376a9148c1f531c0a25ebddce1d5e8fe7b7ed868305231788ad0114b267522103f56cd5c7203da0a38ad28f78b98948c0ea60c21d490c5c4ce26cc1c08da0e4d62102456439a9511f69bc635d4893484bd6e774d02d178eedbaf2d6a2d65c6795d6a652ae736476a914d32cf1fe1fce0eca02fa9f1c4a1a55ae9625743f88ad5ab268680500473044022039520b73cfe21d3ea50e916af7b8c89f1fca40db524473f0836aed9940a7cec80220549689c35653802bc9576bcd373ba4a27fc63d0ac260e9b4c76e5ba86ff0f9170147304402203825acda80285fa11d0d788c0120b7aae2a1ef0df6836a93d28fbeaabde561740220706022fdf2261ec942038dd3b0955f23d1f5667067fb6260bbe19792a18af2f90100846376a9141138c8c5df663ca226334cf443d1cdfabf45b38d88ad0114b2675221030d287dbb4eb74285f9261b32126a26db381faff7a4f255e8575ffc48dbf744782103314a8f8fc2a240ffd015930866f28ef78903240db5dcd462295720460bc020c352ae736476a9141269e81dd4f81eef566f22699569949f9f6999fb88ad5ab26868050047304402202d3b99853c05d79e9af22da2ac9dae27f652bb027900eb4259ab9e16a3b588b6022026bd7c837ad5c4ef1daceb61f78ad00ebd1ac7e3a56fa7576d7736b3783a9fdc01473044022100e08ce4e41201ecd2444f6968ee786d5a0121c047076c574da48e0aee456ecdc1021f5ca84e37a3951d755ed11d5b5f7d199a2eadbebc4003495ddd58c2c9a222b10100846376a914da0fad154bd25905ef43213dbe93a31b5211fc7c88ad0114b267522102fe6ed5df5e44df893840c9bffc5c1a100aad0f0e7ce68188a80f26545626960f21027f743df254973f6019d892e0a875e92f49ca5fbd65a52111e638c3411070d1cd52ae736476a91498d1e0b644f2e9102d6046833673007292b6f67588ad5ab26868050047304402205dd43da2535425e2c37fd1b2654c8e15318336a9849740ea4e9ffbf7d46f50d202207ce7e00e8c2efdb8f7238d560f5a5621846732bb4a30c53a416d7d7e26d69b76014730440220689ca9f0a2e30523f92a0e2f23ed06ee33c3d537d6075e53bdc58bd7efdbe8b202207908c0c29535c21e644410820baa2be5ff3312d45182c76402023bfda511b22c0100846376a9145d82a99eb4eaf194caa0487c5f693318a831a8d288ad0114b267522103a57742665c3e4d530dfb08a0f36dcb044f3a0f25ea6c4da0fe5e5ab387edc0632102d7839db83c80e3db30625d3d69e1529df63ceb235bc05738e99262eda9875a1652ae736476a91402ac8f193b745486ce3aafca88b81e426c1c9e9888ad5ab2686805004730440220174b5a26522b841a8102d1110d24edabb7193a731eed22fef6c9075fd0bdd8d4022045048b9f74534d513f731cca49f1e0d54d5913f47b302a6d18e4db8d07c7763001483045022100f9fca579602f8504b5b3ca830498086afeea2fb7248d5f2eafe3c4d8ccc98b2802201820c1bb79197935fcca791ac5d9c3ac16e1483a868954741932f510a2c41f2a0100846376a91475cd9524b70aebe6550fa612931ac009b52d722a88ad0114b267522103636ed78aba3b251b52b17c51a7b44fabcc4481b2b0bf0656a18ef9d5d97155252102092434b3c8db4394f46aa65eaf20b9841d50a8ec8d8662e7b40e105792be5c1852ae736476a914b0f2b2a5786ce38511c373858449795a3309954f88ad5ab26868050047304402201bad622af5e0da4e9975d5643fd1f9c03b5ae9dc7ce3a968f6488cc5dc1967d6022076e2efd84b1850fee260a8e4b2a354ba4d63e6ccdee170646856c7b68d5731f0014830450221008d205d5f723af95daf2d0542071b69f4eb5bc99254ca91a89d222a702b9f615302204937fc8450f06a40301e6f93a0c939e717373198819923b12344cdd53ed47ec00100846376a914f78e5361c3c847e3f4a555fa4682c1643b1a6de988ad0114b267522102e8ee6dd299285ac5628420da43b5f09f13e900315567f6812dc799cd10e846b821030f647bccc4e265d5c4b38935bec049e64b808c74d83137e9c877a5ac252a321352ae736476a91416b48b379db57850e3ee0e1873645c31662d4d3c88ad5ab2686800000000'
    tx = decode_tx(rawtx, network='signet')
    assert 'txid' in tx.keys()


def test_getinfo(liana):
    ret = liana.get_info()
    assert('block_height' in ret.keys())
    assert('error' not in ret.keys())


def test_get_new_address(liana):
    ret = liana.get_new_address()
    assert(ret[:4] == 'tb1q')
    
    
def test_list_coins(liana):
    ret = liana.list_coins()
    assert(type(ret) is list)
    
    
def test_create_update_psbt(liana):
    coins = liana.list_unspent_coins()
    total = 0
    coins_to_spend = []
    for i in coins:
        total += i['amount']
        coins_to_spend.append(i['outpoint'])
        
    if len(coins_to_spend) == 0:
        pytest.skip('No coins to spend, skipping...')
    
    rcv = liana.get_new_address()
    
    amount = round(total / 2)
    
    outputs = {
        rcv: amount,
    }
    
    psbts = len(liana.list_psbt())
    
    ret = liana.create_psbt(coins_to_spend, outputs, 20)
    
    txid = psbt_to_txid(ret, network='signet')
    
    liana.upate_psbt(ret)
    
    psbts2 = len(liana.list_psbt())
    
    assert psbts2 == (psbts + 1)
    
    ret = liana.broadcast_psbt(txid)
    
    assert('error' in ret.keys())
    
    
def test_del_psbt(liana):
    ret = liana.list_psbt()
    
    psbts = len(ret)
    
    txid = psbt_to_txid(ret[0]['psbt'], network='signet')

    liana.del_psbt(txid)
    
    psbts2 = len(liana.list_psbt())
    
    assert (psbts2 == psbts - 1)
    
    
def test_list_psbt(liana):
    ret = liana.list_psbt()
    
    assert type(ret) is list
    
    
def test_start_rescan(liana):
    timestamp = round(time.time() - 1000000)
    ret = liana.start_rescan(timestamp)
    assert (ret == {}) or ('rescanning' in ret.keys())
    
    
def test_list_confirmed_tx(liana):
    ret = liana.list_confirmed_tx()
    assert type(ret) is list
    
    
def test_fetch_tx(liana):
    tx = liana.list_confirmed_tx()[0]['tx']
    txid = rawtx_to_txid(tx, network='signet')
    tx2 = liana.fetch_tx(txid)['tx']
    txid2 = rawtx_to_txid(tx2, network='signet')
    assert txid == txid2
    
    
def test_create_recovery_psbt(liana):
    addr = liana.get_new_address()
    psbt = liana.create_recovery_psbt(addr, 1)
    liana.upate_psbt(psbt)
    
    
# def test_stop(liana):
#     ret = liana.stop_lianad()

