from typing import Annotated

from pydantic import HttpUrl, AfterValidator

HttpUrlStr = Annotated[HttpUrl, AfterValidator(str)]
