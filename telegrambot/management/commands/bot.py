import asyncio
from django.core.management.base import BaseCommand
from ...managebot import main


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
