#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telegram

START_BUTTONS = None


def __init__():
    global START_BUTTONS
    START_BUTTONS = [[
        telegram.KeyboardButton(text="/👩🍔"),
        telegram.KeyboardButton(text="/🚼🍔"),
        telegram.KeyboardButton(text="/🚼рост"),
        telegram.KeyboardButton(text="/🚼вес"),
    ],[
        telegram.KeyboardButton(text='/🚼🤒'),
        telegram.KeyboardButton(text='/🚼💊'),
        telegram.KeyboardButton(text='/👩🤒'),
        telegram.KeyboardButton(text='/👩💊'),
    ],[
        telegram.KeyboardButton(text="/🚼😴"),
        telegram.KeyboardButton(text="/🚼😜"),
        # telegram.KeyboardButton(text="/🌏", request_location=True),
    ]]
