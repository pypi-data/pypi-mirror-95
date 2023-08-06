"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os
import logging
import datetime
from decimal import Decimal
from web3 import Web3
from web3.types import BlockIdentifier
import math

from moneyonchain.contract import ContractBase
from moneyonchain.governance import ProxyAdmin


class MoCConnector(ContractBase):
    contract_name = 'MoCConnector'

    contract_abi = ContractBase.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCConnector.abi'))
    contract_bin = ContractBase.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCConnector.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self,
                 network_manager,
                 contract_name=None,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            config_network = network_manager.config_network
            contract_address = network_manager.options['networks'][config_network]['addresses']['MoCConnector']

        super().__init__(network_manager,
                         contract_name=contract_name,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Implementation of contract"""

        contract_admin = ProxyAdmin(self.network_manager).from_abi()
        contract_address = Web3.toChecksumAddress(self.contract_address)

        return contract_admin.implementation(contract_address, block_identifier=block_identifier)

    def contracts_addresses(self):

        d_addresses = dict()
        d_addresses['MoC'] = self.sc.moc()
        d_addresses['MoCState'] = self.sc.mocState()
        d_addresses['MoCConverter'] = self.sc.mocConverter()
        d_addresses['MoCSettlement'] = self.sc.mocSettlement()
        d_addresses['MoCExchange'] = self.sc.mocExchange()
        d_addresses['MoCInrate'] = self.sc.mocInrate()
        d_addresses['MoCBurnout'] = self.sc.mocBurnout()
        if self.mode == 'MoC':
            d_addresses['DoCToken'] = self.sc.docToken()
            d_addresses['BProToken'] = self.sc.bproToken()
            d_addresses['MoCBProxManager'] = self.sc.bproxManager()
        else:
            d_addresses['DoCToken'] = self.sc.stableToken()
            d_addresses['BProToken'] = self.sc.riskProToken()
            d_addresses['MoCBProxManager'] = self.sc.riskProxManager()
            d_addresses['ReserveToken'] = self.sc.reserveToken()

        return d_addresses
