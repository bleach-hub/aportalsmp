from .utils.other import API_URL, HEADERS_MAIN, SORTS
from .utils.functions import toShortName, cap, listToURL, activityListToURL
from .handlers import requestExceptionHandler, fetch
from .classes.Exceptions import authDataError, floorsError, giftsError, tradingError
from .classes.Objects import GiftsFloors, Filters, Collections, PortalsGift, Activity, MyActivity, SaleResult
from urllib.parse import quote_plus

######################################################################
#     Module for working with gifts on Portals Gift Marketplace.     #
######################################################################

# ================ Floors ================

async def giftsFloors(authData: str = "") -> GiftsFloors:
    """
    Retrieves the floor prices for all gift collections (short names only).

    Args:
        authData (str): The authentication data required for the API request.

    Returns:
        GiftsFloors: An instance of GiftsFloors containing the floor prices of collections if the request is successful.

    Raises:
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "collections/floors"

    if authData == "":
        raise authDataError("aportalsmp: giftsFloors(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "giftsFloors")

    return GiftsFloors(response.json()['floorPrices'])

async def filterFloors(gift_name: str = "", authData: str = "") -> Filters:
    """
    Retrieves the floor prices of models/backdrops/symbols for a specific gift collection.
    Args:
        gift_name (str): The name of the gift collection.
        authData (str): The authentication data required for the API request.
    Returns:
        Filters: An instance of Filters containing the floor prices of models/backdrops/symbols for the specified gift collection if the request is successful.
    Raises:
        authDataError: If authData is not provided.
        floorsError: If gift_name is not provided or is not a string.
        floorsError: If gift_name is not a valid string.
        requestError: If the API request fails or returns a non-200 status code.
    """
    URL = API_URL + "collections/filters"

    if not authData:
        raise authDataError("aportalsmp: filters(): Error: authData is required")
    if not gift_name:
        raise floorsError("aportalsmp: filters(): Error: gift_name is required")
    if type(gift_name) == str:
        gift_name = toShortName(gift_name)
    if type(gift_name) != str:
        raise floorsError("aportalsmp: filters(): Error: gift_name must be a string")

    URL += f"?short_names={gift_name}"

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "filterFloors")

    return Filters(response.json()['floor_prices'][gift_name]) if "floor_prices" in response.json() and response.json()['floor_prices'].get(gift_name, None) is not None else None

async def collections(limit: int = 100, authData: str = "") -> Collections:
    """
    Retrieves a list of collections and their floors, supply, daily volume etc from the marketplace.

    Args:
        limit (int): The maximum number of results to return. Defaults to 100.
        authData (str): The authentication data required for the API request.

    Returns:
        Collections: An instance of Collections containing the list of collections and their details if the request is successful.

    Raises:
        authDataError: If authData is not provided.
        requestError: If the API request fails or returns a non-200 status code.
    """
    URL = API_URL + "collections" + f"?limit={limit}"

    if authData == "":
        raise authDataError("aportalsmp: collections(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "collections")

    return Collections(response.json()['collections'])

# ================ Gifts ================

async def search(sort: str = "price_asc", offset: int = 0, limit: int = 20, gift_name: str | list = "", model: str | list = "", backdrop: str | list = "", symbol: str | list = "", min_price: int = 0, max_price: int = 100000, authData: str = "") -> list[PortalsGift]:
    """
    Search for gifts with various filters and sorting options.

    Args:
        sort (str): The sorting method for the results. Options include "latest", "price_asc", "price_desc", 
            "gift_id_asc", "gift_id_desc", "model_rarity_asc", "model_rarity_desc". Defaults to "price_asc".
        offset (int): The pagination offset (limit*page). Defaults to 0.
        limit (int): The maximum number of results to return. Defaults to 20.
        gift_name (str | list): The name or list of names of gifts to filter.
        model (str | list): The model or list of models to filter.
        backdrop (str | list): The backdrop or list of backdrops to filter.
        symbol (str | list): The symbol or list of symbols to filter.
        min_price (int): The minimum price of the gifts to filter. Defaults to 0.
        max_price (int): The maximum price of the gifts to filter. Defaults to 100000.
        authData (str): The authentication data required for the API request.
    Returns:
        list[PortalsGift]: A list of PortalsGift objects containing the search results.
    Raises:
        authDataError: If authData is not provided.
        giftsError: If max_price is less than min_price or if min_price and max_price are not integers.
        giftsError: If gift_name, model, backdrop, or symbol are not strings or lists.
        giftsError: If sort is not one of the valid options.
        requestError: If the API request fails.
    """

    if sort not in SORTS:
        raise giftsError(f"aportalsmp: search(): Error: sort must be one of these options: {list(SORTS.keys())}")

    URL = API_URL + "nfts/" + "search?" + f"offset={offset}" + f"&limit={limit}" + f"{SORTS[sort]}" 

    try:
        min_price = int(min_price)
        max_price = int(max_price)
    except:
        raise giftsError("aportalsmp: search(): Error: min_price and max_price must be integers")
    
    if max_price < 100000:
        URL += f"&min_price={min_price}&max_price={max_price}"

    if authData == "":
        raise authDataError("aportalsmp: search(): Error: authData is required")
    if max_price < min_price:
        raise giftsError("aportalsmp: search(): Error: max_price must be greater than min_price")

    if gift_name:
        if type(gift_name) == str:
            URL += f"&filter_by_collections={quote_plus(cap(gift_name))}"
        elif type(gift_name) == list:
            URL += f"&filter_by_collections={listToURL(gift_name)}"
        else:
            raise giftsError("aportalsmp: search(): Error: gift_name must be a string or list")
    if model:
        if type(model) == str:
            URL += f"&filter_by_models={quote_plus(cap(model))}"
        elif type(model) == list:
            URL += f"&filter_by_models={listToURL(model)}"
        else:
            raise giftsError("aportalsmp: search(): Error: model must be a string or list")
    if backdrop:
        if type(backdrop) == str:
            URL += f"&filter_by_backdrops={quote_plus(cap(backdrop))}"
        elif type(backdrop) == list:
            URL += f"&filter_by_backdrops={listToURL(backdrop)}"
        else:
            raise giftsError("aportalsmp: search(): Error: backdrop must be a string or list")
    if symbol:
        if type(symbol) == str:
            URL += f"&filter_by_symbols={quote_plus(cap(symbol))}"
        elif type(symbol) == list:
            URL += f"&filter_by_symbols={listToURL(symbol)}"
        else:
            raise giftsError("aportalsmp: search(): Error: symbol must be a string or list")

    URL += "&status=listed"

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "search")

    return [PortalsGift(gift) for gift in response.json()["results"]]

async def marketActivity(sort: str = "latest", offset: int = 0, limit: int = 20, activityType: str | list = "", gift_name: str | list= "", model: str | list = "", backdrop: str | list = "", symbol: str | list = "", min_price: int = 0, max_price: int = 100000, authData: str = "") -> list[Activity]:
    """
    Retrieves market activity with various filters and sorting options.

    Args:
        sort (str): The sorting method for the results. Options include "latest", "price_asc", "price_desc", 
            "gift_id_asc", "gift_id_desc", "model_rarity_asc", "model_rarity_desc". Defaults to "latest".
        offset (int): The pagination offset (limit*page). Defaults to 0.
        limit (int): The maximum number of results to return. Defaults to 20.
        activityType (str): The type of activity to filter by. Options are "buy", "listing", "price_update", 
            "offer", or an empty string for no filter.
        gift_name (str | list): The name or list of names of gifts to filter.
        model (str | list): The model or list of models to filter.
        backdrop (str | list): The backdrop or list of backdrops to filter.
        symbol (str | list): The symbol or list of symbols to filter.
        min_price (int): The minimum price of the gifts to filter. Defaults to 0.
        max_price (int): The maximum price of the gifts to filter. Defaults to 100000.
        authData (str): The authentication data required for the API request.

    Returns:
        list[Activity]: A list of Activity objects containing the market activity results.

    Raises:
        authDataError: If authData is not provided.
        giftsError: If max_price is less than min_price or if min_price and max_price are not integers.
        giftsError: If activityType is not a valid string or list.
        giftsError: If gift_name, model, backdrop, or symbol are not strings or lists.
        requestError: If the API request fails.
    """

    URL = API_URL + "market/actions/" + f"?offset={offset}" + f"&limit={limit}" + f"{SORTS[sort]}"

    try:
        min_price = int(min_price)
        max_price = int(max_price)
    except:
        raise giftsError("aportalsmp: marketActivity(): Error: min_price and max_price must be integers")

    if max_price < 100000:
        URL += f"&min_price={min_price}&max_price={max_price}"

    if authData == "":
        raise authDataError("aportalsmp: marketActivity(): Error: authData is required")
    if max_price < min_price:
        raise giftsError("aportalsmp: marketActivity(): Error: max_price must be greater than min_price")
    if type(activityType) == str and activityType.lower() not in ["", "buy", "listing", "price_update", "offer"]:
        raise giftsError("aportalsmp: marketActivity(): Error: activityType may be empty, buy, listing, offer or price_update only.")
    if type(activityType) == list:
        activityType = activityListToURL(activityType)

    if gift_name:
        if type(gift_name) == str:
            URL += f"&filter_by_collections={quote_plus(cap(gift_name))}"
        elif type(gift_name) == list:
            URL += f"&filter_by_collections={listToURL(gift_name)}"
        else:
            raise giftsError("aportalsmp: marketActivity(): Error: gift_name must be a string or list")
    if model:
        if type(model) == str:
            URL += f"&filter_by_models={quote_plus(cap(model))}"
        elif type(model) == list:
            URL += f"&filter_by_models={listToURL(model)}"
        else:
            raise giftsError("aportalsmp: marketActivity(): Error: model must be a string or list")
    if backdrop:
        if type(backdrop) == str:
            URL += f"&filter_by_backdrops={quote_plus(cap(backdrop))}"
        elif type(backdrop) == list:
            URL += f"&filter_by_backdrops={listToURL(backdrop)}"
        else:
            raise giftsError("aportalsmp: marketActivity(): Error: backdrop must be a string or list")
    if symbol:
        if type(symbol) == str:
            URL += f"&filter_by_symbols={quote_plus(cap(symbol))}"
        elif type(symbol) == list:
            URL += f"&filter_by_symbols={listToURL(symbol)}"
        else:
            raise giftsError("aportalsmp: marketActivity(): Error: symbol must be a string or list")
        
    if activityType:
        URL += f"&action_types={activityType}"

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "marketActivity")

    return [Activity(activity) for activity in response.json()['actions']]

# ================ My ================


async def myPortalsGifts(offset: int = 0, limit: int = 20, listed: bool = True, authData: str = "") -> list[PortalsGift]:
    """
    Retrieves a list of the user's owned Portal gifts.

    Args:
        offset (int): The offset for pagination.
        limit (int): The maximum number of items to return.
        listed (bool): If True, only gifts listed for sale are shown. Defaults to True.
        authData (str): The authentication data required for the API request.

    Returns:
        list[PortalsGift]: A list of PortalsGift objects representing the user's owned gifts.
    Raises:
        authDataError: If authData is not provided.
        requestError: If the API request fails or returns a non-200 status code.
    """
    URL = API_URL + "nfts/" + "owned?" + f"offset={offset}" + f"&limit={limit}"

    if authData == "":
        raise authDataError("aportalsmp: myPortalsGifts(): Error: authData is required")
    if listed == True:
        URL += "&status=listed"
    else:
        URL += "&status=unlisted"
    
    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "myPortalsGifts")

    return [PortalsGift(nft) for nft in response.json()['nfts']] if "nfts" in response.json() else []

async def myActivity(offset: int = 0, limit: int = 20, authData: str = "") -> list[MyActivity]:
    """
    Retrieves the user's activity on the marketplace.

    Args:
        offset (int): The pagination offset (limit*page). Defaults to 0.
        limit (int): The maximum number of results to return. Defaults to 20.
        authData (str): The authentication data required for the API request.

    Returns:
        list[MyActivity]: A list of MyActivity objects containing the user's activity results.

    Raises:
        authDataError: If authData is not provided.
        requestError: If the API request fails or returns a non-200 status code.
    """
    URL = API_URL + "users/actions/" + f"?offset={offset}" + f"&limit={limit}"

    if authData == "":
        raise authDataError("aportalsmp: myActivity(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "myActivity")

    return [MyActivity(action) for action in response.json()['actions']]

# ================ Trading ================


async def buy(nft_id: str = "", price: int|float = 0, authData: str = "") -> None:
    """
    Buys a gift with the given nft_id at the given price.

    Args:
        nft_id (str): The unique identifier of the NFT to be bought.
        price (int|float): The price at which the NFT should be bought.
        authData (str): The authentication data required for the API request.

    Returns:
        None: if the request is successful
    Raises:
        authDataError: If authData is not provided.
        tradingError: If nft_id is not provided or price is not a positive number.
        requestError: If the API request fails or returns a non-200 status code.
    """
    URL = API_URL + "nfts"

    if authData == "":
        raise authDataError("aportalsmp: buy(): Error: authData is required")
    if not nft_id:
        raise tradingError("aportalsmp: buy(): Error: nft_id is required")
    if type(price) not in [int, float] or price <= 0:
        raise tradingError("aportalsmp: buy(): Error: price error")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    nfts = [{"id": nft_id, "price": str(price)}]
    '''
    {"nft_details":[{"id":"aaaa8eb4-deac-4ba2-aa5c-ea79c73f0d5b","price":"1.85"}]}
    '''

    PAYLOAD = {
        "nft_details": nfts
    }

    response = await fetch(method="POST", url=URL, json=PAYLOAD, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "buy")

    return None

async def changePrice(nft_id: str = "", price: float = 0, authData: str = "") -> None:
    """
    Updates the price of a specified NFT.

    Args:
        nft_id (str): The unique identifier of the NFT for which the price is being updated.
        price (float): The new price to set for the NFT.
        authData (str): The authentication data required for the API request.

    Returns:
        None: if the request is successful, likely a 204 no content response from the API.

    Raises:
        authDataError: If authData is not provided.
        tradingError: If nft_id is not provided or price is not a positive number.
        requestError: If the API request fails or returns a non-200 status code.
    """

    URL = API_URL + "nfts/" + f"{nft_id}/" + "list"

    if not nft_id:
        raise tradingError("aportalsmp: changePrice(): Error: nft_id is required")
    if type(price) not in [int, float] or price <= 0:
        raise tradingError("aportalsmp: changePrice(): Error: price is required")
    if authData == "":
        raise authDataError("aportalsmp: changePrice(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    PAYLOAD = {
        "price": str(price)
    }

    response = await fetch(method="POST", url=URL, json=PAYLOAD, headers=HEADERS, impersonate="chrome110")
    
    requestExceptionHandler(response, "changePrice")

    return None


async def bulkList(nfts: list = [], authData: str = "") -> SaleResult:
    """
    Lists multiple NFTs for sale in bulk.

    Args:
        nfts (list): A non-empty list of dictionaries, each containing 'nft_id', and 'price' as keys.
        authData (str): The authentication data required for the API request.

    Returns:
        SaleResult: An instance of SaleResult containing the response from the API if the request is successful.

    Raises:
        authDataError: If authData is not provided.
        tradingError: If nfts is not a non-empty list.
        requestError: If the API request fails or returns a non-200 status code.
    """

    URL = API_URL + "nfts/bulk-list"

    if authData == "":
        raise authDataError("aportalsmp: bulkList(): Error: authData is required")
    if type(nfts) != list or len(nfts) == 0:
        raise tradingError("aportalsmp: bulkList(): Error: nfts must be a non-empty list")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    PAYLOAD = {
        "nft_prices": nfts
    }

    response = await fetch(method="POST", url=URL, json=PAYLOAD, headers=HEADERS, impersonate="chrome110")
    
    requestExceptionHandler(response, "bulkList")

    return SaleResult(response.json())

async def sale(nft_id: str = "", price: int|float = 0,authData: str = "") -> SaleResult:
    """
    Lists a single NFT for sale.

    Args:
        nft_id (str): The unique identifier of the NFT to be listed.
        price (int|float): The price at which the NFT should be listed for sale.
        authData (str): The authentication data required for the API request.

    Returns:
        SaleResult: An instance of SaleResult containing the response from the API if the request is successful.

    Raises:
        authDataError: If authData is not provided.
        tradingError: If nft_id is not provided or price is not a positive number.
        requestError: If the API request fails or returns a non-200 status code.
    """

    URL = API_URL + "nfts/bulk-list"

    if authData == "":
        raise authDataError("aportalsmp: sale(): Error: authData is required")
    if not nft_id:
        raise tradingError("aportalsmp: sale(): Error: nft_id is required")
    if price == 0 or type(price) not in [int, float]:
        raise tradingError("aportalsmp: sale(): Error: price error")

    nfts = [{"nft_id": nft_id, "price": str(price)}]

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    PAYLOAD = {
        "nft_prices": nfts
    }

    response = await fetch(method="POST", url=URL, json=PAYLOAD, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "sale")

    return SaleResult(response.json())