from pydantic import BaseModel

class CsrfSettings(BaseModel):
  cookie_key: str = "csrf-token"
  header_name: str = "XSRF-Token"
  secret_key: str = "set_secret_key_here"
  cookie_secure: bool = True
  cookie_samesite: str = "none"
  max_age: int = 3600