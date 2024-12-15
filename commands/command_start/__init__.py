__all__ =  ("router",)

from .start import router as router_start_command

from aiogram import Router

router = Router(name=__name__)

router.include_router(router=router_start_command)