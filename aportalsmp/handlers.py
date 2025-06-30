from .classes.Exceptions import requestError, connectionError
from curl_cffi.requests import AsyncSession

###########################
#     Handlers module     #
###########################

async def fetch(method: str = "GET", url: str = "", headers: dict = None, json: dict = None, timeout: int = 15, impersonate: str = "chrome110"):
    """
    Fetches a URL with optional headers and JSON payload.
    
    Args:
        url (str): The URL to fetch.
        headers (dict, optional): Headers to include in the request.
        json (dict, optional): JSON payload to include in the request.
        method (str, optional): HTTP method to use. Defaults to "GET".
        impersonate (str, optional): User agent to impersonate. Defaults to "chrome110".

    Returns:
        Response object from the requests library.
    """
    async with AsyncSession(impersonate=impersonate, timeout=timeout) as session:
        try:
            response = await session.request(method=method, url=url, headers=headers, json=json)
            return response
        except:
            raise connectionError(f"aportalsmp: fetch(): Error: Connection reset after {timeout} seconds. Please check your internet connection or try again later.")

def requestExceptionHandler(response, func_name):
    if not (200 <= response.status_code < 300):
        try:
            responseJson = response.json()
            message = responseJson.get("message")
            if message:
                raise requestError(f"aportalsmp: {func_name}(): Error: status_code: {response.status_code}, message: {message}")
            else:
                raise requestError(f"aportalsmp: {func_name}(): Error: status_code: {response.status_code}, json: {responseJson}")
        except ValueError:
            if len(response.text) > 300:
                raise requestError(f"aportalsmp: {func_name}(): Error: status_code: {response.status_code}. Response text is too long to display (likely raw HTML).")
            else:
                raise requestError(f"aportalsmp: {func_name}(): Error: status_code: {response.status_code}, response_text: {response.text}")