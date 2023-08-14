import pytest
import httpx
from app.api_1.v1.endpoints.car_brands import get_car_brands as get_cars_router
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_get_car_brands(httpx_mock):
    # Mocking the external service
    mock_data = [
        {"nome": "Brand A"},
        {"nome": "Brand B"},
        {"nome": "Brand C"},
    ]
    httpx_mock.add_response(json=mock_data)

    response = get_cars_router.get("/car-brands")()
    assert response == ["Brand A", "Brand B", "Brand C"]


@pytest.mark.asyncio
async def test_get_car_brands_failure(httpx_mock):
    httpx_mock.add_response(status_code=500)

    with pytest.raises(HTTPException) as exception_info:
        get_cars_router.get("/car-brands")()

    assert (
        str(exception_info.value.detail)
        == "Failed to fetch car brands from FIPE service."
    )


@pytest.mark.asyncio
async def test_enqueue_brand(mocker):
    mock_enqueue = mocker.patch("app.queue_utils.enqueue_message", return_value=None)

    brand_name = "Test Brand"
    response = get_cars_router.post("/enqueue-brand/")(brand_name=brand_name)

    mock_enqueue.assert_called_once_with(brand_name)
    assert response == {"message": "Brand enqueued successfully!"}
