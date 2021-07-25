from enum import Enum


class ConfigKeys(Enum):
    CLIENT_ID= 'egtax.client_id'
    CLIENT_SECRET= 'egtax.client_secret'
    CLIENT_TOKEN = 'egtax.client_token'
    CLIENT_TOKEN_TYPE = 'egtax.client_token_type'
    CLIENT_TOKEN_EXPIRE_IN = 'egtax.client_token_expire_in'
    CLIENT_TOKEN_LAST_DATE = 'egtax.client_token_last_date'

    ACTIVITY_ID= 'egtax.activity_id'
    SCOPE = 'egtax.scope'
    API_BASE_URL = 'egtax.apiBaseUrl'
    ID_SRV_BASE_URL = 'egtax.idSrvBaseUrl'
    AUTO_POST = 'egtax.auto_post'
    AUTO_RECEIVE = 'egtax.auto_receive'
    ENABLE_SIGNATURE = 'egtax.enable_signature'
    SIGNATURE_API_URL = 'egtax.signature_api_url'
    START_DATE ='egtax.start_date'
    ACTIVITY_CODE = 'egtax.activity_code'
    PRODUCT_CODING_SCHEMA = 'egtax.product_coding_schema'
    SIGNATURE_TYPE = 'egtax.signature_type'
    SIGNATURE_VALUE = 'egtax.signature_value'
    GRANT_TYPE= 'egtax.grant_type'

