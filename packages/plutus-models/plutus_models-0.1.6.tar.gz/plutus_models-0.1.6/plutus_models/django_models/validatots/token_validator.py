"""Telegram token validator module."""
import asyncio

import aiogram
from django.core.exceptions import ValidationError


async def token_validator(token_value: str):
    """Check if bot exists with specific token."""
    bot = aiogram.Bot(token=token_value)

    async with bot.context():
        try:
            await bot.get_me()
        except Exception as e:
            pass


def token_validator_runner(value: str):
    """Validator runner."""
    try:
        asyncio.run(token_validator(value))
    except Exception:
        raise ValidationError("Token is not valid!")


