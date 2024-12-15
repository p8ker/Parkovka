__all__ =  ("router",)

from .command_start import router as router_commands

from aiogram import Router

router = Router(name=__name__)

router.include_router(router=router_commands)