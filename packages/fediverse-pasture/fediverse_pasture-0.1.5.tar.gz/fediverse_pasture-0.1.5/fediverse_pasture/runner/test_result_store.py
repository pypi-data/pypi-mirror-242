from .result_store import with_store


async def test_with_store():
    async with with_store(db_url="sqlite://:memory:") as store:
        await store.add_result("test", "app1", {})
        await store.add_result("test", "app1", {"a": "b"})
        await store.add_result("test", "app2", {})
        await store.add_result("other", "app1", {})

        result = await store.results_for_test("test")

        assert len(result) == 2


async def test_delete():
    async with with_store(db_url="sqlite://:memory:") as store:
        await store.add_result("test", "app1", {})
        await store.delete_record("test", "app1")

        result = await store.results_for_test("test")

        assert len(result) == 0
