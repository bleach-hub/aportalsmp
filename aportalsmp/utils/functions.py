from urllib.parse import quote_plus
import re

def cap(text) -> str:
    words = re.findall(r"\w+(?:'\w+)?", text)
    for word in words:
        if len(word) > 0:
            cap = word[0].upper() + word[1:]
            text = text.replace(word, cap, 1)
    return text

def listToURL(gifts: list) -> str:
    return '%2C'.join(quote_plus(cap(gift)) for gift in gifts)

def activityListToURL(activity: list) -> str:
    return '%2C'.join(activity)

def toShortName(gift_name: str) -> str:
    return gift_name.replace(" ", "").replace("'", "").replace("’", "").replace("-", "").lower()

def convertForListing(nft_id: str = "", price: float = 0):
    return {"nft_id": nft_id, "price": str(price)}

def convertForBuying(nft_id: str = "", price: float = 0):
    return {"id": nft_id, "price": str(price)}