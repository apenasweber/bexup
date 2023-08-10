import pytest
import httpx
from app.api_1.v1.endpoints import vehicles as router
from app.models.vehicle import Brand, Model, Year, VehicleValue


@pytest.mark.asyncio
async def test_trigger_load_vehicles(httpx_mock, mocker):
    # Mocking the external service
    mock_data = [{"nome": "Brand A"}]
    httpx_mock.add_response(json=mock_data)

    # Mocking the database
    mock_db = mocker.MagicMock()

    # Mocking the queue
    mocker.patch("app.queue_manager.brand_queue.put", return_value=None)

    response = router.post("/trigger-load-vehicles")(db=mock_db)
    assert response == {"status": "Data loading has started!"}


@pytest.mark.asyncio
async def test_load_vehicles(httpx_mock, mocker):
    # Mocking the external service
    brand_data = [{"nome": "Brand A", "codigo": "B1"}]
    model_data = {"modelos": [{"nome": "Model A", "codigo": "M1"}]}
    year_data = [{"nome": "Year A", "codigo": "Y1"}]
    vehicle_value_data = {
        "TipoVeiculo": 1,
        "Valor": "20000",
        "Marca": "Brand A",
        "Modelo": "Model A",
        "AnoModelo": 2022,
        "Combustivel": "Diesel",
        "CodigoFipe": "ABC1234",
        "MesReferencia": "08/2023",
        "SiglaCombustivel": "D",
    }

    httpx_mock.add_response(json=brand_data)
    httpx_mock.add_response(json=model_data)
    httpx_mock.add_response(json=year_data)
    httpx_mock.add_response(json=vehicle_value_data)

    # Mocking the database
    mock_db = mocker.MagicMock()

    # Mocking models to mimic id retrieval after db.flush()
    mock_brand = Brand(id=1)
    mock_model = Model(id=2)
    mock_year = Year(id=3)
    mock_vehicle_value = VehicleValue(id=4)

    mock_db.add.side_effect = [mock_brand, mock_model, mock_year, mock_vehicle_value]
    mock_db.flush.side_effect = [None, None, None, None]

    response = await router.post("/load-vehicles")(db=mock_db)
    assert response == {"status": "Data loaded successfully!"}


@pytest.mark.asyncio
async def test_external_service_failure(httpx_mock, mocker):
    httpx_mock.add_response(status_code=500)

    mock_db = mocker.MagicMock()

    response = await router.post("/load-vehicles")(db=mock_db)
    assert response == {"status": "Failed to load data: HTTP response not successful."}


@pytest.mark.asyncio
async def test_database_insertion_error(httpx_mock, mocker):
    mock_data = [{"nome": "Brand A"}]
    httpx_mock.add_response(json=mock_data)

    mock_db = mocker.MagicMock()
    mock_db.add.side_effect = Exception("Database error")

    response = await router.post("/load-vehicles")(db=mock_db)
    assert response == {"status": "Failed to load data: Database error"}


@pytest.mark.asyncio
async def test_queue_processing_error(httpx_mock, mocker):
    mock_data = [{"nome": "Brand A"}]
    httpx_mock.add_response(json=mock_data)

    mock_db = mocker.MagicMock()

    mocker.patch(
        "app.queue_manager.brand_queue.put",
        side_effect=Exception("Queue processing error"),
    )

    response = router.post("/trigger-load-vehicles")(db=mock_db)
    assert response == {"status": "Failed to load data: Queue processing error"}
