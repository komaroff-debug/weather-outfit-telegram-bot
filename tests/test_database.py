import pytest
import app.database as db

@pytest.mark.asyncio
async def test_user(tmp_path,monkeypatch):
    monkeypatch.setattr(db,"DATABASE_PATH",str(tmp_path/"test.db"))
    await db.init_db()
    await db.create_user(123)
    user=await db.get_user(123)
    assert user["user_id"]==123
