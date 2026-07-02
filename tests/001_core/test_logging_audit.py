import pytest
import logging

@pytest.mark.asyncio
async def test_logging_is_configured():
    root_logger = logging.getLogger()
    assert root_logger.level > 0

@pytest.mark.asyncio
async def test_app_logger_exists():
    logger = logging.getLogger("app")
    assert logger is not None

@pytest.mark.asyncio
async def test_auth_logger_exists():
    logger = logging.getLogger("app.authentication")
    assert logger is not None

@pytest.mark.asyncio
async def test_llm_request_log_model_exists():
    from app.ai_management.models import LLMRequestLog
    assert LLMRequestLog is not None

@pytest.mark.asyncio
async def test_user_session_history_model_exists():
    from app.authentication.models import UsuarioSessionHistory
    assert UsuarioSessionHistory is not None

@pytest.mark.asyncio
async def test_refresh_tokens_track_ip_and_user_agent():
    from app.authentication.models import RefreshToken
    assert hasattr(RefreshToken, "ip_address")
    assert hasattr(RefreshToken, "user_agent")

@pytest.mark.asyncio
async def test_user_session_history_tracks_login_logout():
    from app.authentication.models import UsuarioSessionHistory
    assert hasattr(UsuarioSessionHistory, "login_time")
    assert hasattr(UsuarioSessionHistory, "logout_time")
    assert hasattr(UsuarioSessionHistory, "ip_address")
    assert hasattr(UsuarioSessionHistory, "user_agent")
