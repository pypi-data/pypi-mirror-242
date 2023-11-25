import json
from enum import Enum
from fastapi import FastAPI, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import nameguard.context
from nameguard.nameguard import NameGuard
from nameguard.utils import validate_namehash, namehash_from_labelhash, validate_token_id, validate_ethereum_address
from nameguard.models import (
    NameGuardReport,
    BulkNameGuardBulkReport,
    SecurePrimaryNameResult,
    NetworkName,
    GraphemeGuardReport,
    FakeEthNameCheckResult
)
from nameguard.endpoints import Endpoints
from nameguard.logging import logger
from nameguard.exceptions import (
    InvalidNameHash,
    ENSSubgraphUnavailable,
    NamehashMismatchError,
    NamehashNotFoundInSubgraph,
    InvalidEthereumAddress,
    ProviderUnavailable,
    InvalidTokenID,
    NotAGrapheme,
    MissingTitle,
)


class ApiVersion(str, Enum):
    V08_BETA = 'v0.8-beta'


app = FastAPI(
    title='NameGuard API',
    version=ApiVersion.V08_BETA.value,
    description=
'''Welcome to NameGuard, a powerful tool developed by [NameHash Labs](https://namehashlabs.org) to identify and prevent malicious use of Ethereum Name Service (ENS) names.

## Important Notes
⚠️ Beta Version: Please be aware that NameGuard is currently in beta. We appreciate your feedback as we work towards a stable v1 release. Expect changes to the API to address community feedback and improve functionality.

## Documentation
These documentation pages focus specifically on the NameGuard API. For information on the NameGuard Library, SDK, and UI Kit, please refer to the [NameGuard GitHub repository](https://github.com/namehash/nameguard).''',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ng = NameGuard()


# -- inspect-name --


class InspectNameRequest(BaseModel):
    name: str = Field(
        description='Name to inspect.',
        examples=['vitalìk.eth'],
    )
    network_name: NetworkName


@app.get(
    '/inspect-name/{network_name}/{name:path}',
    tags=['name'],
    summary='Inspect Name',
    responses={
        **ENSSubgraphUnavailable.get_responses_spec(),
    },
)
@app.get('/inspect-name/{network_name}', include_in_schema=False)
async def inspect_name_get(
        
        network_name: NetworkName,
        name: str = Path(default_factory=lambda: '',
                         description='**Name should be url-encoded (except when using the Swagger UI).**',
                         examples=['vitalìk.eth']),
) -> NameGuardReport:
    logger.debug(
        f"{json.dumps({'endpoint': Endpoints.INSPECT_NAME, 'method': 'GET', 'network_name': network_name, 'name': name})}")
    nameguard.context.endpoint_name.set(Endpoints.INSPECT_NAME)
    return await ng.inspect_name(network_name, name)


@app.post(
    '/inspect-name',
    tags=['name'],
    summary='Inspect Name',
    responses={
        **ENSSubgraphUnavailable.get_responses_spec(),
    },
)
async def inspect_name_post( request: InspectNameRequest) -> NameGuardReport:
    logger.debug(f"{json.dumps({'endpoint': Endpoints.INSPECT_NAME, 'method': 'POST', 'network_name': request.network_name, 'name': request.name})}")
    nameguard.context.endpoint_name.set(Endpoints.INSPECT_NAME)
    return await ng.inspect_name(request.network_name, request.name)


# -- bulk-inspect-names --


class BulkInspectNamesRequest(BaseModel):
    names: list[str] = Field(max_length=250, examples=[['vitalìk.eth', 'nick.eth']])
    network_name: NetworkName


@app.post(
    '/bulk-inspect-names',
    tags=['name'],
    summary='Inspect Multiple Names',
    responses={
        **ENSSubgraphUnavailable.get_responses_spec(),
    },
)
async def bulk_inspect_names( request: BulkInspectNamesRequest) -> BulkNameGuardBulkReport:
    logger.debug(f"{json.dumps({'endpoint': Endpoints.BULK_INSPECT_NAMES, 'method': 'POST', 'network_name': request.network_name, 'names': request.names})}")
    nameguard.context.endpoint_name.set(Endpoints.BULK_INSPECT_NAMES)
    return await ng.bulk_inspect_names(request.network_name, request.names)


# -- inspect-namehash --


class InspectNamehashRequest(BaseModel):
    namehash: str = Field(description='Namehash should be a decimal or a hex (prefixed with 0x) string.',
                          examples=['0xd48fd5598e605861cbd8e45419b41b83739bff52eaef0e283181bbe0a43a5b32'])
    network_name: NetworkName


@app.get(
    '/inspect-namehash/{network_name}/{namehash}',
    tags=['namehash'],
    summary='Inspect Namehash GET',
    responses={
        **InvalidNameHash.get_responses_spec(),
        **ENSSubgraphUnavailable.get_responses_spec(),
        **NamehashMismatchError.get_responses_spec(),
        **NamehashNotFoundInSubgraph.get_responses_spec(),
    },
)
async def inspect_namehash_get(
        
        network_name: NetworkName,
        namehash: str = Path(examples=['0xd48fd5598e605861cbd8e45419b41b83739bff52eaef0e283181bbe0a43a5b32'],
                             description='Namehash should be a decimal or a hex (prefixed with 0x) string.')
) -> NameGuardReport:
    logger.debug(f"{json.dumps({'endpoint': Endpoints.INSPECT_NAMEHASH, 'method': 'GET', 'network_name': network_name, 'namehash': namehash})}")
    nameguard.context.endpoint_name.set(Endpoints.INSPECT_NAMEHASH)
    return await ng.inspect_namehash(network_name=network_name,
                                     namehash=validate_namehash(namehash=namehash),
                                     )


@app.post(
    '/inspect-namehash',
    tags=['namehash'],
    summary='Inspect Namehash',
    responses={
        **InvalidNameHash.get_responses_spec(),
        **ENSSubgraphUnavailable.get_responses_spec(),
        **NamehashMismatchError.get_responses_spec(),
        **NamehashNotFoundInSubgraph.get_responses_spec(),
    },
)
async def inspect_namehash_post( request: InspectNamehashRequest) -> NameGuardReport:
    logger.debug(f"{json.dumps({'endpoint': Endpoints.INSPECT_NAMEHASH, 'method': 'POST', 'network_name': request.network_name, 'namehash': request.namehash})}")
    nameguard.context.endpoint_name.set(Endpoints.INSPECT_NAMEHASH)
    return await ng.inspect_namehash(network_name=request.network_name,
                                     namehash=validate_namehash(namehash=request.namehash),
                                     )


# -- inspect-labelhash --


class InspectLabelhashRequest(BaseModel):
    labelhash: str = Field(description='Labelhash should be a decimal or a hex (prefixed with 0x) string.',
                           examples=['0x3276e4878615389906712b876ce1455b8f5d1c5ea3ffcf7a705e0d32fafae9c5'])
    network_name: NetworkName
    parent_name: str = Field('eth')


@app.get(
    '/inspect-labelhash/{network_name}/{labelhash}/{parent_name:path}',
    tags=['labelhash'],
    summary='Inspect Labelhash GET',
    responses={
        **InvalidNameHash.get_responses_spec(),
        **ENSSubgraphUnavailable.get_responses_spec(),
        **NamehashMismatchError.get_responses_spec(),
        **NamehashNotFoundInSubgraph.get_responses_spec(),
    },
)
@app.get('/inspect-labelhash/{network_name}/{labelhash}', include_in_schema=False)
async def inspect_labelhash_get(
        
        network_name: NetworkName,
        labelhash: str = Path(examples=['0x3276e4878615389906712b876ce1455b8f5d1c5ea3ffcf7a705e0d32fafae9c5'],
                              description='Labelhash should be a decimal or a hex (prefixed with 0x) string.'),
        parent_name: str = Path(default_factory=lambda: '', examples=['eth'])
) -> NameGuardReport:
    logger.debug(f"{json.dumps({'endpoint': Endpoints.INSPECT_LABELHASH, 'method': 'GET', 'network_name': network_name, 'labelhash': labelhash, 'parent_name': parent_name})}")
    nameguard.context.endpoint_name.set(Endpoints.INSPECT_LABELHASH)
    valid_labelhash = validate_namehash(namehash=labelhash)
    namehash = namehash_from_labelhash(valid_labelhash, parent_name=parent_name)
    return await ng.inspect_namehash(network_name=network_name, namehash=namehash)


@app.post(
    '/inspect-labelhash',
    tags=['labelhash'],
    summary='Inspect Labelhash',
    responses={
        **InvalidNameHash.get_responses_spec(),
        **ENSSubgraphUnavailable.get_responses_spec(),
        **NamehashMismatchError.get_responses_spec(),
        **NamehashNotFoundInSubgraph.get_responses_spec(),
    },
)
async def inspect_labelhash_post( request: InspectLabelhashRequest) -> NameGuardReport:
    logger.debug(
        f"{json.dumps({'endpoint': Endpoints.INSPECT_LABELHASH, 'method': 'POST', 'network_name': request.network_name, 'labelhash': request.labelhash, 'parent_name': request.parent_name})}")
    nameguard.context.endpoint_name.set(Endpoints.INSPECT_LABELHASH)
    valid_labelhash = validate_namehash(namehash=request.labelhash)
    namehash = namehash_from_labelhash(valid_labelhash, parent_name=request.parent_name)
    return await ng.inspect_namehash(network_name=request.network_name, namehash=namehash)


# -- secure-primary-name --


@app.get(
    '/secure-primary-name/{network_name}/{address}',
    tags=['secure_primary_name'],
    summary='Reverse lookup of Ethereum address to primary name',
    responses={
        **InvalidEthereumAddress.get_responses_spec(),
        **ProviderUnavailable.get_responses_spec(),
    },
)
async def secure_primary_name_get( address: str,
                                  network_name: NetworkName) -> SecurePrimaryNameResult:
    logger.debug(
        f"{json.dumps({'endpoint': Endpoints.SECURE_PRIMARY_NAME, 'method': 'GET', 'network_name': network_name, 'address': address})}")
    nameguard.context.endpoint_name.set(Endpoints.SECURE_PRIMARY_NAME)
    address = validate_ethereum_address(address)
    return await ng.secure_primary_name(address, network_name)


# -- fake-ens-name-check --


@app.get(
    '/fake-eth-name-check/{network_name}/{contract_address}/{token_id}',
    tags=['fake-eth-name-check'],
    summary='Fake .eth ENS name check GET',
    responses={
        **InvalidTokenID.get_responses_spec(),
        **InvalidEthereumAddress.get_responses_spec(),
        **ProviderUnavailable.get_responses_spec(),
    },
)
async def fake_eth_name_check_get(
        
        network_name: NetworkName,
        contract_address: str = Path(examples=['0x495f947276749ce646f68ac8c248420045cb7b5e'],
                                     description='Contract address for the NFT contract (ERC721 and ERC1155 supported).'),
        token_id: str = Path(examples=['61995921128521442959106650131462633744885269624153038309795231243542768648193'],
                             description='The ID of the token (in hex or decimal format).')
) -> FakeEthNameCheckResult:
    logger.debug(
        f"{json.dumps({'endpoint': Endpoints.FAKE_ETH_NAME_CHECK, 'method': 'GET', 'network_name': network_name, 'contract_address': contract_address, 'token_id': token_id})}")
    nameguard.context.endpoint_name.set(Endpoints.FAKE_ETH_NAME_CHECK)
    contract_address = validate_ethereum_address(contract_address)
    token_id = validate_token_id(token_id)
    return await ng.fake_eth_name_check(network_name=network_name, contract_address=contract_address, token_id=token_id)

class FakeETHNameCheckFieldsRequest(BaseModel):
    network_name: NetworkName
    contract_address: str = Path(examples=['0x495f947276749ce646f68ac8c248420045cb7b5e'],
                                 description='Contract address for the NFT contract (ERC721 and ERC1155 supported).')
    token_id: str = Path(examples=['61995921128521442959106650131462633744885269624153038309795231243542768648193'],
                         description='The ID of the token (in hex or decimal format).')
    fields: dict[str, str] = Field(
        description='Fields with values which will be investigated (e.g. title, collection name, metadata) whether they look like fake .eth ENS name. `title` key is mandatory, for ENS contracts it should be the ENS name.')


@app.post(
    '/fake-eth-name-check-fields',
    tags=['fake-eth-name-check'],
    summary='Fake .eth ENS name check with fields',
    responses={
        **InvalidTokenID.get_responses_spec(),
        **InvalidEthereumAddress.get_responses_spec(),
        **MissingTitle.get_responses_spec(),
    },
)
async def fake_eth_name_check_fields_post(
         
        request: FakeETHNameCheckFieldsRequest
        ) -> FakeEthNameCheckResult:
    logger.debug(
        f"{json.dumps({'endpoint': Endpoints.FAKE_ETH_NAME_CHECK, 'method': 'POST', 'network_name': request.network_name, 'contract_address': request.contract_address, 'token_id': request.token_id})}")
    nameguard.context.endpoint_name.set(Endpoints.FAKE_ETH_NAME_CHECK)
    contract_address = validate_ethereum_address(request.contract_address)
    token_id = validate_token_id(request.token_id)
    return await ng.fake_eth_name_check_fields(network_name=request.network_name, contract_address=contract_address, token_id=token_id, investigated_fields=request.fields)



# -- inspect-grapheme --


@app.get(
    '/inspect-grapheme/{grapheme}',
    tags=['grapheme'],
    summary='Inspect Grapheme GET',
    responses={
        **NotAGrapheme.get_responses_spec(),
    },
)
async def inspect_grapheme_get(
        grapheme: str = Path(
            description='Grapheme to inspect. Should be url-encoded (except when using the Swagger UI).',
            examples=['v', 'ń', '%F0%9F%98%B5'])
) -> GraphemeGuardReport:
    logger.debug(
        f"{json.dumps({'endpoint': Endpoints.INSPECT_GRAPHEME, 'method': 'GET', 'grapheme': grapheme})}")
    nameguard.context.endpoint_name.set(Endpoints.INSPECT_GRAPHEME)
    return ng.inspect_grapheme(grapheme)


if __name__ == '__main__':
    import asyncio

    asyncio.run(ng.inspect_name('mainnet', 'nick.eth'))
