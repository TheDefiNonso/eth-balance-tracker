from dotenv import load_dotenv
import os
from pathlib import Path

WATCHED_ADDRESSES = [
    "0x28c6c06298d514db089934071355e5743bf21d60",  # Binance
    "0x21a31ee1afc51d94c2efccaa2092ad1028285549",  # Binance
    "0xdfd5293d8e347dfe59e90efd55b2956a1343963d",  # Binance
    "0x56eddb7aa87536c09ccc2793473599fd21a8b17f",  # Binance
    "0x9696f59e4d72e237be84ffd425dcad154bf96976",  # Binance
    "0x4976a4a02f38326660d17bf34b431dc6e2eb2327",  # Binance
    "0xd551234ae421e3bcba99a0da6d736074f22192ff",  # Binance
    "0x564286362092d8e7936f0549571a803b203aaced",  # Binance
    "0x0681d8db095565fe8a346fa0277bffde9c0edbbf",  # Binance
    "0xfe9e8709d3215310075d67e3ed32a380ccf451c8",  # Binance
    "0x4e9ce36e442e55ecd9025b9a6e0d88485d628a67",  # Binance
    "0x8894e0a0c962cb723c1976a4421c95949be2d4e3",  # Binance
    "0xbe0eb53f46cd790cd13851d5eff43d12404d33e8",  # Binance cold
    "0xf977814e90da44bfa03b6295a0616a897441acec",  # Binance
    "0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503",  # Binance whale
    "0x742d35cc6634c0532925a3b844bc454e4438f44e",  # Bitfinex
    "0x876eabf441b2ee5b5b0554fd502a8e0600950cfa",  # Bitfinex
    "0xd24400ae8bfebb18ca49be86258a3c749cf46853",  # Gemini
    "0x6cc5f688a315f3dc28a7781717a9a798a59fda7b",  # OKX
    "0x236f233dbf080b01cd88f809f68a0e0e7e73bf7d",  # OKX
    "0xa7efae728d2936e78bda97dc267687568dd593f3",  # OKX
    "0x1c4b70a3968436b9a0a9cf5205c787eb81bb558c",  # Gate.io
    "0x0d0707963952f2fba59dd06f2b425ace40b492fe",  # Gate.io
    "0x7793cd85c11a924478d358d49b05b37e91b5810f",  # Gate.io
    "0x2b5634c42055806a59e9107ed44d43c426e58258",  # KuCoin
    "0x689c56aef474df92d44a1b70850f808488f9769c",  # KuCoin
    "0xa1d8d972560c2f8144af871db508f0b0b10a3fbf",  # KuCoin
    "0x2910543af39aba0cd09dbb2d50200b3e800a63d2",  # Kraken
    "0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0",  # Kraken
    "0x0a869d79a7052c7f1b55a8ebabbea3420f0d1e13",  # Kraken
    "0xe853c56864a2ebe4576a807d26fdc4a0ada51919",  # Kraken
    "0x43984d578803891dfa9706bdeee6078d80cfc79e",  # Kraken
    "0x66c57bf505a85a74609d2c83e7f8b4a4645a5df6",  # Kraken
    "0x503828976d22510aad0201ac7ec88293211d23da",  # Coinbase
    "0xddfabcdc4d8ffc6d5beaf154f18b778f892a0740",  # Coinbase
    "0x3cd751e6b0078be393132286c442345e5dc49699",  # Coinbase
    "0xb5d85cbf7cb3ee0d56b3bb207d5fc4b82f43f511",  # Coinbase
    "0xeb2629a2734e272bcc07bda959863f316f4bd4cf",  # Coinbase
    "0x71660c4005ba85c37ccec55d0c4493e66fe775d3",  # Coinbase
    "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43",  # Coinbase
    "0x77696bb39917c91a0c3908d577d5e322095425ca",  # Coinbase
    "0x7c195d981abfdc3ddecd2ca0fed0958430488e34",  # Coinbase
    "0x95a9bd206ae52c4ba8eecfc93d18eebfafd7baa1",  # Coinbase
    "0xb739d0895772dbb71a89a3754a160269068f0d45",  # Coinbase
    "0xf6874c88757721a02f9b4f8b4b47af88f7da7be6",  # Coinbase
    # Ethereum Foundation / Core
    "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",  # EF
    "0x8ee7d9235e01e6b42345120b5d270bdB763624C7",  # EF
    "0xab5801a7d398351b8be11c439e05c5b3259aec9b",  # Vitalik
    "0xd8da6bf26964af9d7eed9e03e53415d37aa96045",  # Vitalik
    "0x220866b1a2219f40e72f5c628b65d54268ca3a9d",  # EF grants
    # Wrapped ETH / DeFi Protocols
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",  # Uniswap v2 router
    "0xe592427a0aece92de3edee1f18e0157c05861564",  # Uniswap v3 router
    "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45",  # Uniswap v3 router 2
    "0x1111111254eeb25477b68fb85ed929f73a960582",  # 1inch v5
    "0x881d40237659c251811cec9c364ef91dc08d300c",  # MetaMask swap
    "0xdef1c0ded9bec7f1a1670819833240f027b25eff",  # 0x Exchange
    "0x6b75d8af000000e20b7a7ddf000ba900b4009a80",  # Gnosis safe
    # Lending Protocols
    "0x3dfd23a6c5e8bbcfc9581d2e864a68feb6a076d3",  # Aave v1
    "0x398ec7346dcd622edc5ae82352f02be94c62d119",  # Aave lending pool
    "0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9",  # Aave v2
    "0x87870bca3f3fd6335c3f4ce8392d69350b4fa4e2",  # Aave v3
    "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b",  # Compound
    "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5",  # Compound cETH
    "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643",  # Compound cDAI
    # Staking / ETH2
    "0x00000000219ab540356cbb839cbe05303d7705fa",  # ETH2 deposit contract
    "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",  # wstETH
    "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",  # stETH Lido
    "0xdc24316b9ae028f1497c275eb9192a3ea0f67022",  # Lido curve pool
    # Bridges
    "0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf",  # Polygon bridge
    "0x99c9fc46f92e8a1c0dec1b1747d010903e884be1",  # Optimism bridge
    "0x8eb8a3b98659cce290402893d0123abb75e3ab28",  # Avalanche bridge
    "0xa3a7b6f88361f48403514059f1f16c8e78d60eec",  # Arbitrum bridge
    "0x4c36d2919e407f0cc2ee3c993ccf8ac26d9ce64e",  # Rainbow bridge
    # Known whale addresses
    "0x9bf4001d307dfd62b26a2f1307ee0c0307632d59",  # whale
    "0x189b9cbd4aff470af2c0102f365fc1823d857965",  # whale
    "0x6f231d5ba47ed43026cd5b99d7551b5450a3e01d",  # whale
    "0xf89d7b9c864f589bbf53a82105107622b35eaa40",  # whale
    "0x8484ef722627bf18ca5ae6bcf031c23e6e922b30",  # whale
    "0x8103683202aa8da10536036edef04cdd865c225e",  # whale
    "0x1b3cb81e51011b549d78bf720b0d924ac763a7c2",  # whale
    "0x220ca6ef4a65a5023e5f3021f0e4e8d7b55a0b75",  # whale
    "0xba18ded280a3b12c142f14b8c630c1b8c2bacb36",  # whale
    "0xcafe1a77e84698c83ca8931f54a755176ef75f2c",  # whale
    "0x1b3f7e3534c06d7a5e5f94f7f01d16e9d10f7a5d",  # whale
    "0x9845e1909dca337944a0272f1f9f7249833d2d19",  # whale
    "0x3bfc20f0b9afcace800d73d2191166ff16540258",  # Nexo
    "0xf35a6bd6e0459a4b53a27862c51a2a7292b383d1",  # whale
    "0x1fa848857b24b9416355f4b4668a84c842116bf4",  # whale
    "0xca436e14855323927d6e6264470ded36455fc8bd",  # whale
    "0x09f1e5b8cd2dd1865e2f1b15d6d64c0f73b0b79e",  # whale
    "0x98ec059dc3adfbdd63429454aeb0c990fba4a128",  # whale
    "0x4862733b5fddfd35f35ea8ccf08f5045e57388b3",  # whale
    "0xa29456c97a22de77e0a80e2f3dc5d4fa4a28b1f5",  # whale
    "0x09cabec1ead1c0ba254b09efb3ee13841712be14",  # whale
    "0xc61b9bb3a7a0767e3179713f3a5c7a9aedce193c",  # whale
    "0x4a3870699ce745a5b3440d1b41c089e16b2c4f71",  # whale
    "0x742d35cc6634c0532925a3b844bc454e4438f44f",  # whale
    "0x13f9c453e7a8a1e6b6d2f4cf46a3be4c24e78e50",  # whale
    "0x6262998ced04146fa42253a5c0af90ca02dfd2a3",  # whale
    "0x534da741361c7e0bd5d9b8da8b28cba6dab2e76b",  # whale
    "0xab7c74abc0c4d48d1bdad5dcb26153fc8780f83e",  # whale
    "0x910cbd523d972eb0a6f4cae4618ad62622b39dbf",  # Tornado cash
    "0xa160cdab225685da1d56aa342ad8841c3b53f291",  # Tornado cash
    "0xd90e2f925da726b50c4ed8d0fb90ad053324f31b",  # Tornado cash
    "0xd96f2b1c14db8458374d9aca76e26c3950113464",  # Tornado cash
    "0x4736dcf1b7a3d580672cce6e7c65cd5cc9cfba9d",  # Tornado cash
    "0x169ad27a470d064dede56a2d3ff727986b15d52b",  # Tornado cash
    "0x0836222f2b2b5a6430604607006e815cf60ac1f3",  # Tornado cash
    "0xf60dd140cff0706bae9cd734ac3ae76ad9ebc32a",  # Tornado cash
    "0x22aaa7720ddd5388a3c0a3333430953c68f1849b",  # Tornado cash
    "0xba214c1c1928a32bffe790263e38b4af9bfcd659",  # Tornado cash
    "0xb1c8094b234dce6e03f10a5b673c1d8c69739a00",  # Tornado cash
    "0x527653ea119f3e6a1f5bd18fbf4714081d7b31ce",  # Tornado cash
    "0x58e8dcc13be9780fc42e8723d8ead4cf46943df2",  # Tornado cash
    "0xd691f27f38b395864ea86cfc7253969b409c362d",  # Tornado cash
    "0xdf231d99ff8b6c6cbf4e9b9a945cbacef9339163",  # Tornado cash
    "0xdd4c48c0b24039969fc16d1cdf626eab821d3384",  # Tornado cash
    "0xd47438c816c9e7f2e2888a3c8cf2fe9b5b71b75b",  # Tornado cash
    "0x23773e65ed146a459667957743f1c39c32d3dc68",  # Tornado cash
    "0x2717c5e28cf931547b621a5dddb772ab6a35b701",  # Tornado cash
    "0xca0840578f57fe71599d29375e16783424023357",  # Tornado cash
    # NFT / Gaming
    "0x1e0049783f008a0085193e00003d00cd54003c71",  # OpenSea
    "0x7be8076f4ea4a4ad08075c2508e481d6c946d12b",  # OpenSea v1
    "0x7f268357a8c2552623316e2562d90e642bb538e5",  # OpenSea v2
    "0x00000000006c3852cbef3e08e8df289169ede581",  # Seaport
    "0x59728544b08ab483533076417fbbb2fd0b17ce3a",  # LooksRare
    "0x74312363e45dcaba76c59aa49cdbb069d9e7f3f1",  # X2Y2
    # Stablecoins
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
    "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
    "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI
    "0x4fabb145d64652a948d72533023f6e7a623c7c53",  # BUSD
    "0x8e870d67f660d95d5be530380d0ec0bd388289e1",  # USDP
    "0x0000000000085d4780b73119b644ae5ecd22b376",  # TUSD
    # Major token contracts
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",  # WBTC
    "0x514910771af9ca656af840dff83e8264ecf986ca",  # LINK
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",  # UNI
    "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9",  # AAVE
    "0xc00e94cb662c3520282e6f5717214004a7f26888",  # COMP
    "0xba100000625a3754423978a60c9317c58a424e3d",  # BAL
    "0xd533a949740bb3306d119cc777fa900ba034cd52",  # CRV
    "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",  # MKR
    "0x6810e776880c02933d47db1b9fc05908e5386b96",  # GNO
    "0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f",  # SNX
    # More exchanges
    "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208",  # IDEX
    "0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be",  # Binance
    "0xd551234ae421e3bcba99a0da6d736074f22192ff",  # Binance
    "0x0c37f7d5cb0bda4cff1e53c4218c8aa289d99b3e",  # Nexo
    "0xa910f92acdaf488fa6ef02174fb86208ad7722ba",  # Poloniex
    "0x32be343b94f860124dc4fee278fdcbd38c102d88",  # Poloniex
    "0x209c4784ab1e8183cf58ca33cb740efbf3fc18ef",  # Poloniex
    "0xfbb1b73c4f0bda4f67dca266ce6ef42f520fbb98",  # Bittrex
    "0xe94b04a0fed112f3664e45adb2b8915693dd5ff3",  # Bittrex
    "0x6fc82a5fe25a5cdb58bc74600a40a69c065263f8",  # Gemini
    "0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea",  # Gemini
    "0x5f65f7b609678448494de4c87521cdf6cef1e932",  # Gemini
    "0x04645af26836f96f9e8a1c69c0d8b5f31b8a9b7f",  # Huobi
    "0xab5c66752a9e8167967685f1450532fb96d5d24f",  # Huobi
    "0x6748f50f686bfbca6fe8ad62b22228b87f31ff2b",  # Huobi
    "0xfdb16996831753d5331ff813c29a93c76834a0ad",  # Huobi
    "0xeee28d484628d41a82d01e21d12e2e78d69920da",  # Huobi
    "0x46705dfff24256421a05d056c29e81bdc09723b8",  # Huobi
    "0xff7f9bdef7d85d10e7e3c0cf0a53a9aab65b0438",  # Huobi
    "0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be",  # Binance
    "0x77134cbc06cb00b66f4c7e623d5fdbf6777635ec",  # Bybit
    "0x1db92e2eebc8e0c075a02bea49a2935bcd2dfcf4",  # Bybit
    "0xf89d7b9c864f589bbf53a82105107622b35eaa40",  # Bybit
    # More DeFi
    "0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f",  # Uniswap v2 factory
    "0x1f98431c8ad98523631ae4a59f267346ea31f984",  # Uniswap v3 factory
    "0xc36442b4a4522e871399cd717abdd847ab11fe88",  # Uniswap v3 positions NFT
    "0xe66b31678d6c16e9ebf358268a790b763c133750",  # 0x proxy
    "0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f",  # SushiSwap router
    "0xc0aee478e3658e2610c5f7a4a2e1777ce9e4f2ac",  # SushiSwap factory
    "0x6dea81c8171d0ba574754ef6f8b412f2ed88c54d",  # Liquity LQTY
    "0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419",  # Chainlink ETH/USD
    "0x00000000000000adc04c56bf30ac9d3c0aaf14dc",  # Seaport 1.5
]

load_dotenv()
ALCHEMY_URL = os.getenv("ALCHEMY_URL")
if not ALCHEMY_URL:
    raise ValueError("ALCHEMY_URL is not set in .env")


DB_PATH = Path(os.getenv("DB_PATH", "balances.db"))
