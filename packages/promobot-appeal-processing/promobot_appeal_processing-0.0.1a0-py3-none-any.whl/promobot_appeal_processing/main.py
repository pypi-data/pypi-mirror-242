import asyncio

from .model import model
from .structures import Prediction


def predict(text: str) -> Prediction:
    """
    Synchronously predict appeal classification

    Parameters:
        text: Appeal text

    Returns:
        Predicted classification
    """
    return model.predict(text)


async def predict_async(text: str) -> Prediction:
    """
    Asynchronous wrapper around the ``predict`` function

    Example:
        ```py hl_lines="8"
        from fastapi import FastAPI, Body
        from promobot_appeal_processing import predict_async

        app = FastAPI()

        @app.post("/api")
        async def api(text: str = Body(embed=True)):
            return await predict_async(text)
        ```

    Parameters:
        text: Appeal text

    Returns:
        Predicted classification
    """
    return await asyncio.to_thread(predict, text)
