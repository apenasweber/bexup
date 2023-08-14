import httpx
import logging
import asyncio

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://parallelum.com.br/fipe/api/v1"


async def get_brands():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/carros/marcas", timeout=10)
        if response.status_code != 200:
            logging.error("Failed to fetch car marcas from FIPE service.")
            raise Exception("Failed to fetch car marcas from FIPE service.")
        return response.json()


async def get_brands_with_retry(retries=3, delay=5):
    for _ in range(retries):
        try:
            return await get_brands()
        except Exception as e:
            logging.warning(f"Error fetching brands: {e}")
            await asyncio.sleep(delay)
    logging.error("Max retries reached. Failed to fetch brands.")
    raise Exception("Max retries reached. Failed to fetch brands.")


async def get_models(brand_code):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/carros/marcas/{brand_code}/modelos", timeout=10
        )
        if response.status_code != 200:
            logging.error(response.text)
            logging.error("Failed to fetch car modelos from FIPE service.")
            raise Exception("Failed to fetch car modelos from FIPE service.")
        return response.json()


async def get_models_with_retry(brand_code, retries=3, delay=5):
    for _ in range(retries):
        try:
            return await get_models(brand_code)
        except Exception as e:
            logging.warning(f"Error fetching models: {e}")
            await asyncio.sleep(delay)
    logging.error("Max retries reached. Failed to fetch models.")
    raise Exception("Max retries reached. Failed to fetch models.")


async def get_years(brand_code, model_code):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/carros/marcas/{brand_code}/modelos/{model_code}/anos",
            timeout=10,
        )
        if response.status_code != 200:
            logging.error(response.text)
            logging.error("Failed to fetch car anos from FIPE service.")
            raise Exception("Failed to fetch car anos from FIPE service.")
        return response.json()


async def get_years_with_retry(brand_code, model_code, retries=3, delay=5):
    for _ in range(retries):
        try:
            return await get_years(brand_code, model_code)
        except Exception as e:
            logging.warning(f"Error fetching years: {e}")
            await asyncio.sleep(delay)
    logging.error("Max retries reached. Failed to fetch years.")
    raise Exception("Max retries reached. Failed to fetch years.")


async def get_vehicle_value(brand_code, model_code, year_code):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/carros/marcas/{brand_code}/modelos/{model_code}/anos/{year_code}",
            timeout=10,
        )
        if response.status_code != 200:
            logging.error(response.text)
            logging.error("Failed to fetch car value from FIPE service.")
            raise Exception("Failed to fetch car value from FIPE service.")
        return response.json()


async def get_vehicle_value_with_retry(
    brand_code, model_code, year_code, retries=3, delay=5
):
    for _ in range(retries):
        try:
            return await get_vehicle_value(brand_code, model_code, year_code)
        except Exception as e:
            logging.warning(f"Error fetching vehicle value: {e}")
            await asyncio.sleep(delay)
    logging.error("Max retries reached. Failed to fetch vehicle value.")
    raise Exception("Max retries reached. Failed to fetch vehicle value.")


async def get_vehicle_details_by_brand(brand: str):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{brand}/modelos"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        return data


async def get_vehicle_details_by_brand_with_retry(brand: str, retries=3, delay=5):
    for _ in range(retries):
        try:
            return await get_vehicle_details_by_brand(brand)
        except Exception as e:
            logging.warning(f"Error fetching vehicle details: {e}")
            await asyncio.sleep(delay)
    logging.error("Max retries reached. Failed to fetch vehicle details.")
    raise Exception("Max retries reached. Failed to fetch vehicle details.")
