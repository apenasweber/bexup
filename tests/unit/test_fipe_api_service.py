import pytest
import httpx
from app.services.fipe_service import get_brands, get_brands_with_retry


@pytest.mark.asyncio
async def test_get_brands_success(httpx_mock):
    mock_data = [{"name": "Brand A"}, {"name": "Brand B"}]
    httpx_mock.add_response(json=mock_data)
    result = await get_brands()
    assert result == mock_data


@pytest.mark.asyncio
async def test_get_brands_failure(httpx_mock):
    httpx_mock.add_response(status_code=400)
    with pytest.raises(
        Exception, match="Failed to fetch car marcas from FIPE service."
    ):
        await get_brands()


@pytest.mark.asyncio
async def test_get_brands_with_retry_success(httpx_mock):
    mock_data = [{"name": "Brand A"}, {"name": "Brand B"}]
    httpx_mock.add_response(json=mock_data)
    result = await get_brands_with_retry()
    assert result == mock_data


@pytest.mark.asyncio
async def test_get_brands_with_retry_failure_all_attempts(httpx_mock):
    httpx_mock.add_response(status_code=400)
    httpx_mock.add_response(status_code=400)
    httpx_mock.add_response(status_code=400)
    with pytest.raises(Exception, match="Max retries reached. Failed to fetch brands."):
        await get_brands_with_retry()
