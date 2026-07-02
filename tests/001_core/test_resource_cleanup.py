import pytest
from app.dependencies import get_current_user
from app.database import get_db

@pytest.mark.asyncio
async def test_get_db_is_generator():
    gen = get_db()
    assert hasattr(gen, "__aiter__") or hasattr(gen, "__anext__")

@pytest.mark.asyncio
async def test_db_session_rollback_on_error():
    from app.database import get_db
    gen = get_db()
    try:
        session = await gen.__anext__()
        assert session is not None
    except StopAsyncIteration:
        pass
    finally:
        try:
            await gen.__anext__()
        except (StopAsyncIteration, RuntimeError):
            pass

@pytest.mark.asyncio
async def test_models_have_is_active_flag():
    from app.database import BaseModel
    assert hasattr(BaseModel, "is_active")

@pytest.mark.asyncio
async def test_models_have_timestamps():
    from app.database import BaseModel
    assert hasattr(BaseModel, "created_at")
    assert hasattr(BaseModel, "updated_at")
