import asyncio
import logging
import telethon
from hikkapyro import Client, errors, types
from .. import loader, utils
import psutil
import inspect
import platform
import math
from uptime import uptime
from typing import Union
logger = logging.getLogger(__name__)


@loader.tds
class Systeminfo(loader.Module):
    """Информация о системе."""

    strings_ru = {
        "name": "Systeminfo"
    }

    async def hostcmd(self, message):

        def get_plural(number: Union[int, float], one: str, few: str,
                       many: str, other: str = '') -> str:
            """`one`  = 1, 21, 31, 41, 51, 61...\n
            `few`  = 2-4, 22-24, 32-34...\n
            `many` = 0, 5-20, 25-30, 35-40...\n
            `other` = 1.31, 2.31, 5.31..."""
            if type(number) == float:
                if not number.is_integer():
                    return other
                else:
                    number = int(number)
            if number % 10 in {2, 3, 4}:
                if not 10 < number < 20:
                    return few
            number = str(number)
            if number[-1] == '1':
                return one
            return many

        def human_read_format(size):
            pwr = math.floor(math.log(size, 1024))
            suff = ["Б", "КБ", "МБ", "ГБ", "ТБ", "ПБ", "ЭБ", "ЗБ", "ЙБ"]
            if size > 1024 ** (len(suff) - 1):
                return "не знаю как назвать такое число :)"
            return f"{size / 1024 ** pwr:.0f} {suff[pwr]}"
        use_reply = False
        my_system = platform.uname()
        inet_received = psutil.net_io_counters().bytes_recv
        inet_sent = psutil.net_io_counters().bytes_sent
        totalsize = psutil.disk_usage('/').total
        freesize = psutil.disk_usage('/').free
        m, s = divmod(round(uptime()), 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        a = f"{d} {get_plural(d, 'день', 'дня', 'дней')} " \
            f"{h} {get_plural(h, 'час', 'часа', 'часов')} " \
            f"{m} {get_plural(m, 'минута', 'минуты', 'минут')} " \
            f"{s} {get_plural(s, 'секунда', 'секунды', 'секунд')}"

        text = f''' 🚀Информация о сервере🚀
            ├🖥 Система: {my_system.system}
            ├🐍 Версия питона: {platform.python_version()}
            ├📈 Нагрузка ЦП: {psutil.cpu_percent(1)}%
            ├📈 Количество ядер: {psutil.cpu_count()}
            ├📗 Загрузка ОЗУ: {psutil.virtual_memory()[2]}%
            ├📗 Кол-во ОЗУ: {human_read_format(size=psutil.virtual_memory().total)}
            ├📗 Доступно ОЗУ: {human_read_format(size=psutil.virtual_memory().available)}
            ├📗 Использовано ОЗУ: {human_read_format(size=psutil.virtual_memory().used)}
            ├💽 Диск: {human_read_format(size=freesize)}/{human_read_format(size=totalsize)}
            ├⚠ Отправлено: {human_read_format(size=inet_sent)} 
            ├⚠ Принято: {human_read_format(size=inet_received)}
            └⏰ Время работы сервера: {a}
            '''

        await utils.answer(message, inspect.cleandoc(text))