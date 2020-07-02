#!/usr/bin/env python3

import argparse
import asyncio
import logging
import os
from contextlib import contextmanager

from aioconsole import ainput

from joycontrol import logging_default as log, utils
from joycontrol.command_line_interface import ControllerCLI
from joycontrol.controller import Controller
from joycontrol.controller_state import ControllerState, button_push, ButtonState
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

from twitchio.ext import commands
from secretsio import TMI_TOKEN, CLIENT_ID, BOT_NICK, CHANNEL

import numpy


#@client.event
#async def on_ready():
#    print('We have logged in as {0.user}'.format(client))

logger = logging.getLogger(__name__)
bot = commands.Bot(
# set up the bot
irc_token=TMI_TOKEN,
client_id=CLIENT_ID,
nick=BOT_NICK,
initial_channels=[CHANNEL],
prefix="!"
)
async def _main(controller, reconnect_bt_addr=None, capture_file=None, spi_flash=None, device_id=None):

    factory = controller_protocol_factory(controller, spi_flash=spi_flash)
    ctl_psm, itr_psm = 17, 19
    transport, protocol = await create_hid_server(factory, reconnect_bt_addr=reconnect_bt_addr, ctl_psm=ctl_psm,
                                                  itr_psm=itr_psm, capture_file=capture_file, device_id=device_id)

    controller_state = protocol.get_controller_state()
    #await ButtonState.get_available_buttons(ControllerState)
    #await asyncio.sleep(5)
    #await button_push(controller_state, 'a')
    #await asyncio.sleep(0.3)
    await asyncio.sleep(5)
    controller_state.button_state.set_button('l')
    controller_state.button_state.set_button('r')
    await asyncio.sleep(0.5)
    controller_state.button_state.set_button('l', False)
    controller_state.button_state.set_button('r', False)
    await asyncio.sleep(0.5)
    await button_push(controller_state, 'a')

    #@bot.event
    async def event_ready():
        'Called once when the bot goes online.'
        print("bot is online!")
        ws = bot._ws  # this is only needed to send messages within event_ready
        await ws.send_privmsg(CHANNEL, f"/me has landed!")

    @bot.event
    async def event_message(message):
        ws = bot._ws
        print(message.content)
        if message.content.startswith('!twitchplays'):
            await ws.send_privmsg(CHANNEL, f"Twitch Plays Commands:")
            await ws.send_privmsg(CHANNEL, f"a/b/x/y/zl/zr/up/down/plus/minus:")
            await ws.send_privmsg(CHANNEL, f"presses those buttons")
            await ws.send_privmsg(CHANNEL, f"right/left/r/l:")
            await ws.send_privmsg(CHANNEL, f"run right/left for 5 seconds")
            await ws.send_privmsg(CHANNEL, f"ralk/lalk/wr/wl:")
            await ws.send_privmsg(CHANNEL, f"walk right/left for 5 seconds")
            await ws.send_privmsg(CHANNEL, f"stop/s: stops movement")
            await ws.send_privmsg(CHANNEL, f"jump/j: jumps")
        if message.author.name != BOT_NICK: 
            if message.content.startswith('a'):
                await button_push(controller_state, 'a')
            if message.content.startswith('b'):
                await button_push(controller_state, 'b')
            #if message.content.startswith('yon'):
                #await asyncio.sleep(0.3)
                #on = True
            #    controller_state.button_state.set_button('y')
                #await asyncio.sleep(5)
            #if message.content.startswith('yoff'):
                #await asyncio.sleep(0.3)
                #off = False
            #    controller_state.button_state.set_button('y', False)
                #await asyncio.sleep(5)
            if message.content.startswith('y'):
                await button_push(controller_state, 'y')
            if message.content.startswith('x'):
                await button_push(controller_state, 'x')
            if message.content.startswith('zr'):
                await button_push(controller_state, 'zr')
            if message.content.startswith('zl'):
                await button_push(controller_state, 'zl')
            if message.content.startswith('right') or message.content.startswith('r'):
                # await button_push(controller_state, 'right')
                controller_state.button_state.set_button('y')
                controller_state.button_state.set_button('right')
                await asyncio.sleep(5)
                controller_state.button_state.set_button('y', False)
                controller_state.button_state.set_button('right', False)
            if message.content.startswith('left') or message.content.startswith('l'):
                # await button_push(controller_state, 'left')
                controller_state.button_state.set_button('y')
                controller_state.button_state.set_button('left')
                await asyncio.sleep(5)
                controller_state.button_state.set_button('y', False)
                controller_state.button_state.set_button('left', False)
            if message.content.startswith('down'):
                await button_push(controller_state, 'down')
            if message.content.startswith('up'):
                await button_push(controller_state, 'up')
            if message.content.startswith('minus'):
                await button_push(controller_state, 'minus')
            if message.content.startswith('plus'):
                await button_push(controller_state, 'plus')
            if message.content.startswith('stop') or message.content.startswith('s'):
                await button_push(controller_state, 'right')
                await button_push(controller_state, 'left')
            # if message.content.startswith('rt'):
            #     controller_state.button_state.set_button('y')
            #     controller_state.button_state.set_button('right')
            #     await asyncio.sleep(5)
            #     controller_state.button_state.set_button('y', False)
            #     controller_state.button_state.set_button('right', False)
            if message.content.startswith('ralk') or message.content.startswith('wr'):
                controller_state.button_state.set_button('right')
                await asyncio.sleep(5)
                controller_state.button_state.set_button('right', False)
            # if message.content.startswith('lt'):
            #     controller_state.button_state.set_button('y')
            #     controller_state.button_state.set_button('left')
            #     await asyncio.sleep(5)
            #     controller_state.button_state.set_button('y', False)
            #     controller_state.button_state.set_button('left', False)
            if message.content.startswith('lalk') or message.content.startswith('wl'):
                controller_state.button_state.set_button('left')
                await asyncio.sleep(5)
                controller_state.button_state.set_button('left', False)
            if message.content.startswith('jump') or message.content.startswith('j'):
                controller_state.button_state.set_button('a')
                await asyncio.sleep(1.5)
                controller_state.button_state.set_button('a', False)
            if message.content.startswith('lr'):
                controller_state.button_state.set_button('l')
                controller_state.button_state.set_button('r')
                await asyncio.sleep(.5)
                controller_state.button_state.set_button('l', False)
                controller_state.button_state.set_button('r', False)






if __name__ == '__main__':
    # check if root
    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')

    # setup logging
    #log.configure(console_level=logging.ERROR)
    log.configure()

    parser = argparse.ArgumentParser()
    parser.add_argument('controller', help='JOYCON_R, JOYCON_L or PRO_CONTROLLER')
    parser.add_argument('-l', '--log')
    parser.add_argument('-d', '--device_id')
    parser.add_argument('--spi_flash')
    parser.add_argument('-r', '--reconnect_bt_addr', type=str, default=None,
                        help='The Switch console Bluetooth address, for reconnecting as an already paired controller')
    args = parser.parse_args()

    if args.controller == 'JOYCON_R':
        controller = Controller.JOYCON_R
    elif args.controller == 'JOYCON_L':
        controller = Controller.JOYCON_L
    elif args.controller == 'PRO_CONTROLLER':
        controller = Controller.PRO_CONTROLLER
    else:
        raise ValueError(f'Unknown controller "{args.controller}".')

    spi_flash = None
    if args.spi_flash:
        with open(args.spi_flash, 'rb') as spi_flash_file:
            spi_flash = FlashMemory(spi_flash_file.read())

    with utils.get_output(path=args.log, default=None) as capture_file:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            _main(controller,
                  reconnect_bt_addr=args.reconnect_bt_addr,
                  capture_file=capture_file,
                  spi_flash=spi_flash,
                  device_id=args.device_id
                  )
        )
    bot.run()
