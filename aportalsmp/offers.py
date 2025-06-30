from .utils.functions import cap
from .utils.other import API_URL, HEADERS_MAIN
from .utils.collections_ids import collections_ids
from .classes.Exceptions import authDataError, offerError
from .classes.Objects import CollectionOffer, GiftOffer
from .handlers import fetch, requestExceptionHandler

#######################################################################
#     Module for working with offers on Portals Gift Marketplace.     #
#######################################################################

# =================== Gifts offers ===================

async def makeOffer(nft_id: str = "", offer_price: int | float = 0, expiration_days: int = 7, authData: str = "") -> None:
    """
    Creates an offer for a specified NFT.
    Args:
        nft_id (str): The unique identifier of the NFT to make an offer on.
        offer_price (int | float): The price of the offer.
        expiration_days (int): The number of days until the offer expires. Must be either 7 or 0 (no expiration). Default is 7.
        authData (str): The authentication data required for the API request.
    Returns:
        None: If the request is successful and the offer is created.
    Raises:
        offerError: If nft_id is not provided.
        offerError: If offer_price is not provided or is 0.
        offerError: If expiration_days is not 7 or 0.
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "offers"

    if not nft_id:
        raise offerError("aportalsmp: makeOffer(): Error: nft_id is required")
    if offer_price == 0:
        raise offerError("aportalsmp: makeOffer(): Error: offer_price is required")
    if expiration_days not in [7, 0]:
        raise offerError("aportalsmp: makeOffer(): Error: expiration_days must be 7 or 0")
    if not authData:
        raise authDataError("aportalsmp: makeOffer(): authData is required.")


    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    PAYLOAD = {
        "offer": {
            "nft_id": nft_id,
            "offer_price": str(offer_price)
            }
    }

    if expiration_days == 7:
        PAYLOAD["offer"].update({"expiration_days": expiration_days})
    
    response = await fetch(method="POST", url=URL, json=PAYLOAD, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "makeOffer")
    
    return None

async def cancelOffer(offer_id: str = "", authData: str = "") -> None:
    """
    Cancels an offer with the given offer_id.

    Args:
        offer_id (str): The unique identifier of the offer to be canceled.
        authData (str): The authentication data required for the API request.

    Returns:
        None: If the request is successful and the offer is canceled.

    Raises:
        offerError: If offer_id is not provided.
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "offers/" + f"{offer_id}" + "/cancel"

    if not offer_id:
        raise offerError("aportalsmp: cancelOffer(): Error: offer_id is required")
    if authData == "":
        raise authDataError("aportalsmp: cancelOffer(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="POST", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "cancelOffer")

    return None

async def editOffer(offer_id: str = "", new_price: int | float = 0, authData: str = "") -> None:
    """
    Edit existing offer price.
    Args:
        offer_id (str): The unique identifier of the offer to be edited.
        new_price (int | float): The new price to set for the offer.
        authData (str): The authentication data required for the API request.
    Returns:
        None: If the request is successful and the offer is edited.
    Raises:
        offerError: If offer_id is not provided.
        offerError: If new_price is not provided or is less than 0.5.
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "offers/" + f"{offer_id}"

    if not offer_id:
        raise offerError("aportalsmp: editOffer(): Error: offer_id is required")
    if type(new_price) not in [float, int] or new_price < 0.5:
        raise offerError("aportalsmp: editOffer(): Error: new_price must be a number >= 0.5")
    if not authData:
        raise authDataError("aportalsmp: editOffer(): Error: authData is required")

    PAYLOAD = {
        "amount": str(float(new_price))
    }

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="PATCH", url=URL, json=PAYLOAD, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "editOffer")
   
    return None

# =================== Collection offers ===================

async def collectionOffer(gift_name: str = "", amount: float | int = 0, expiration_days: int = 7, max_nfts: int = 1, authData: str = "") -> None:
    """
    Make an offer for collection.
    Args:
        gift_name (str): The name of the gift collection.
        amount (float | int): Price in TON you want to offer.
        expiration_days (int): The number of days until the offer expires. Must be either 7 or 0 (no expiration). Default is 7.
        max_nfts (int): The maximum number of NFTs that can be purchased with this offer. Default is 1.
        authData (str): The authentication data required for the API request.
    Returns:
        None: If the request is successful and the offer is created.
    Raises:
        offerError: If gift_name is not provided.
        offerError: If amount is not provided or is less than or equal to 0.
        offerError: If max_nfts is not provided or is less than or equal to 0.
        authDataError: If authData is not provided.
        offerError: If expiration_days is not 0 or 7.
        requestError: If the API request fails.
    """

    URL = API_URL + "collection-offers/"

    if not gift_name:
        raise offerError("aportalsmp: collectionOffer(): Error: gift_name is required")
    if amount <= 0.0:
        raise offerError("aportalsmp: collectionOffer(): Error: amount is required")
    if max_nfts <= 0:
        raise offerError("aportalsmp: collectionOffer(): Error: max_nfts is required")
    if not authData:
        raise authDataError("aportalsmp: collectionOffer(): Error: authData is required")
    if expiration_days not in [0,7]:
        raise offerError("aportalsmp: collectionOffer(): Error: expiration_days must be 0 (no expiration) or 7 (7 days)")

    gift_name = cap(gift_name)

    ID = collections_ids.get(gift_name, None)

    if ID is None:
        raise offerError("aportalsmp: collectionOffer(): Error: gift_name is invalid")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    PAYLOAD = {
        "amount": str(amount),
        "collection_id": ID,
        "expiration_days": expiration_days,
        "max_nfts": max_nfts
    }

    response = await fetch(method="POST", url=URL, headers=HEADERS, json=PAYLOAD, impersonate="chrome110")

    requestExceptionHandler(response, "collectionOffer")
    
    return None

async def editCollectionOffer(amount: float | int = 0, offer_id: str = "", max_nfts: int = 1, authData: str = "") -> None:
    """
    Edit existing collection offer's price.
    Args:
        amount (float | int): The new price to set for the collection offer.
        offer_id (str): The unique identifier of the collection offer to be edited.
        max_nfts (int): The maximum number of NFTs that can be purchased with this offer. Default is 1.
        authData (str): The authentication data required for the API request.
    Returns:
        None: If the request is successful and the collection offer is edited.
    Raises:
        offerError: If amount is not provided or is less than 0.5.
        offerError: If offer_id is not provided.
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "collection-offers/update"

    if not offer_id:
        raise offerError("aportalsmp: editCollectionOffer(): Error: offer_id is required")
    if type(amount) not in [float, int] or amount < 0.5:
        raise offerError("aportalsmp: editCollectionOffer(): Error: amount must be number >= 0.5")
    if not authData:
        raise authDataError("aportalsmp: editCollectionOffer(): Error: authData is required")

    PAYLOAD = {
        "amount": str(float(amount)),
        "id": offer_id,
        "max_nfts": max_nfts
    }

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="POST", url=URL, headers=HEADERS, json=PAYLOAD, impersonate="chrome110")

    requestExceptionHandler(response, "editCollectionOffer")

    return None

async def cancelCollectionOffer(offer_id: str = "", authData: str = "") -> None:
    """
    Cancels a collection offer with the given offer_id.

    Args:
        offer_id (str): The unique identifier of the collection offer to be canceled.
        authData (str): The authentication data required for the API request.
    Returns:
        None: If the request is successful and the collection offer is canceled.
    Raises:
        offerError: If offer_id is not provided.
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "collection-offers/cancel"

    if not offer_id:
        raise offerError("aportalsmp: cancelCollectionOffer(): Error: offer_id is required")

    if not authData:
        raise authDataError("aportalsmp: cancelCollectionOffer(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    PAYLOAD = {
        "id": offer_id
    }

    response = await fetch(method="POST", url=URL, headers=HEADERS, json=PAYLOAD, impersonate="chrome110")

    requestExceptionHandler(response, "cancelCollectionOffer")

    return None

async def allCollectionOffers(gift_name: str = "", authData: str = "") -> list[CollectionOffer]:
    """
    Retrieves all collection offers for a specific gift collection.
    Args:
        gift_name (str): The name of the gift collection.
        authData (str): The authentication data required for the API request.
    Returns:
        list: A list of CollectionOffer objects if the request is successful.
    Raises:
        offerError: If gift_name is not provided.
        offerError: If gift_name is invalid.
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "collection-offers/"

    if not gift_name:
        raise offerError("aportalsmp: allCollectionOffers(): Error: gift_name is required")
    
    gift_name = cap(gift_name)
    ID = collections_ids.get(gift_name, None)

    if ID is None:
        raise offerError("aportalsmp: allCollectionOffers(): Error: gift_name is invalid")
    if not authData:
        raise authDataError("aportalsmp: allCollectionOffers(): Error: authData is required")
    
    URL += f"{ID}/all"
    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "allCollectionOffers")

    return [CollectionOffer(offer) for offer in response.json()] if len(response.json()) > 0 else []

async def topOffer(gift_name: str = "", authData: str = "") -> CollectionOffer | None:
    """
    Retrieves the top offer for a specified gift collection.

    Args:
        gift_name (str): The name of the gift collection.
        authData (str): The authentication data required for the API request.
    Returns:
        CollectionOffer | None: A CollectionOffer object if the request is successful and a top offer exists.
    Raises:
        offerError: If gift_name is not provided or is invalid.
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "collection-offers/"

    try:
        ID = collections_ids[cap(gift_name)]
    except:
        raise offerError("aportalsmp: topOffer(): Error: gift_name is invalid")

    if authData == "":
        raise authDataError("aportalsmp: topOffer(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    URL += f"{ID}/top"

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "topOffer")

    return CollectionOffer(response.json()) if response.status_code == 200 and len(response.json()) > 0 else None

# ==================== My offers ===================

async def myReceivedOffers(offset: int = 0, limit: int = 20, authData: str = "") -> list[GiftOffer]:
    """
    Retrieves the offers received by the user.

    Args:
        offset (int): The pagination offset. Defaults to 0.
        limit (int): The maximum number of results to return. Defaults to 20.
        authData (str): The authentication data required for the API request.
    Returns:
        list: A list of GiftOffer objects if the request is successful.
    Raises:
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + f"offers/received?offset={offset}&limit={limit}"

    if authData == "":
        raise authDataError("aportalsmp: myReceivedOffers(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "myReceivedOffers")

    return [GiftOffer(offer["offer"]) for offer in response.json()["top_offers"]] if "top_offers" in response.json() and len(response.json()["top_offers"]) > 0 else []

async def myCollectionOffers(authData: str = "") -> list[CollectionOffer]:
    """
    Retrieves the collection offers placed by the user.

    Args:
        authData (str): The authentication data required for the API request.
    Returns:
        list: A list of CollectionOffer objects if the request is successful.
    Raises:
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + "collection-offers/"
    if authData == "":
        raise authDataError("aportalsmp: myCollectionOffers(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "myCollectionOffers")

    return [CollectionOffer(offer) for offer in response.json()] if len(response.json()) > 0 else []

async def myPlacedOffers(offset: int = 0, limit: int = 20, authData: str = "") -> list[GiftOffer]:
    """
    Retrieves the offers placed by the user.

    Args:
        offset (int): The pagination offset. Defaults to 0.
        limit (int): The maximum number of results to return. Defaults to 20.
        authData (str): The authentication data required for the API request.

    Returns:
        list: A list of GiftOffer objects if the request is successful.

    Raises:
        authDataError: If authData is not provided.
        requestError: If the API request fails.
    """

    URL = API_URL + f"offers/placed?offset={offset}&limit={limit}"

    if authData == "":
        raise authDataError("aportalsmp: myPlacedOffers(): Error: authData is required")

    HEADERS = {**HEADERS_MAIN, "Authorization": authData}

    response = await fetch(method="GET", url=URL, headers=HEADERS, impersonate="chrome110")

    requestExceptionHandler(response, "myPlacedOffers")

    return [GiftOffer(offer) for offer in response.json()["offers"]] if "offers" in response.json() and len(response.json()["offers"]) > 0 else []