import requests
from datetime import datetime, timedelta
from vnstock3.core.utils.user_agent import get_headers
from vnstock3.explorer.msn.const import _CURRENCY_ID_MAP, _CRYPTO_ID_MAP, _GLOBAL_INDICES
from vnstock3.core.utils.logger import get_logger

logger = get_logger(__name__)

def msn_apikey (headers, random_agent=False, show_log=False):
    """
    Lấy apikey của MSN để sử dụng cho các truy vấn dữ liệu
    """
    scope = """{"audienceMode":"adult",
                        "browser":{"browserType":"chrome","version":"0","ismobile":"false"},
                        "deviceFormFactor":"desktop","domain":"www.msn.com",
                        "locale":{"content":{"language":"vi","market":"vn"},"display":{"language":"vi","market":"vn"}},
                        "ocid":"hpmsn","os":"macos","platform":"web",
                        "pageType":"financestockdetails"}
                        """
    today = (datetime.now()-timedelta(hours=7)).strftime("%Y%m%d")
    
    url = f"https://assets.msn.com/resolver/api/resolve/v3/config/?expType=AppConfig&expInstance=default&apptype=finance&v={today}.130&targetScope={scope}"
    if show_log:
        logger.info(f"Requesting apikey from {url}")
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    if show_log:
        logger.info(f"Response: {data}")
    apikey = data['configs']["shared/msn-ns/HoroscopeAnswerCardWC/default"]["properties"]["horoscopeAnswerServiceClientSettings"]["apikey"]
    return apikey

def get_asset_type(symbol_id):
    if symbol_id in _CURRENCY_ID_MAP.values():
        return "currency"
    elif symbol_id in _CRYPTO_ID_MAP.values():
        return "crypto"
    elif symbol_id in _GLOBAL_INDICES.values():
        return "index"
    else:
        return "Unknown"
    
