import pytest

from controle_ativos.utils import security as security_utils


@pytest.fixture(autouse=True)
def reset_auth_rate_limits():
    security_utils.reset_auth_rate_limits()
    yield
    security_utils.reset_auth_rate_limits()
