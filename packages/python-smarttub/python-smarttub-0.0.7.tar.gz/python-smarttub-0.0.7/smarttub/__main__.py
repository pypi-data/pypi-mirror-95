import asyncio
import datetime
import logging
from pprint import pprint
import sys

import aiohttp

from . import SmartTub

logging.basicConfig(level=logging.DEBUG)


async def main(args):
    async with aiohttp.ClientSession() as session:
        st = SmartTub(session)
        await st.login(*args[0:2])
        account = await st.get_account()
        print(account)
        spas = await account.get_spas()
        print(spas)
        for spa in spas:
            status = spa.get_status()
            pumps = spa.get_pumps()
            lights = spa.get_lights()
            errors = spa.get_errors()
            reminders = spa.get_reminders()

            pprint(await status)
            for pump in await pumps:
                print(pump)
            for light in await lights:
                print(light)
            for reminder in await reminders:
                print(reminder)
            pprint(await errors)

            if len(args) > 2:
                await light.set_mode(light.LightMode.RED, 25)
                lights = await spa.get_lights()
                print(lights[0])

        if len(args) > 3:
            debug_status = spa.get_debug_status()
            energy_usage_day = spa.get_energy_usage(spa.EnergyUsageInterval.DAY, end_date=datetime.date.today(), start_date=datetime.date.today() - datetime.timedelta(days=7))
            set_temp = spa.set_temperature(38.3)
            await set_temp
            pprint(await energy_usage_day)
            pprint(await debug_status)
            # await st._refresh_token()

asyncio.run(main(sys.argv[1:]))
