#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload
import json
import vk_config

vk_session = VkApi(token=vk_config.TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=vk_config.GROUP_ID)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.message['text'] == '/start':
            if event.obj.message['from_id']:
                vk_session.method("messages.send", {"user_id":event.obj.message['from_id'], "message":vk_config.WELCOME_MESSAGE,"random_id":get_random_id()})
        elif event.obj.message['text'] == '/stop':
            if event.obj.message['from_id']:
                vk_session.method("messages.send", {"user_id":event.obj.message['from_id'], "message":vk_config.STOP_MESSAGE,"random_id":get_random_id()})
        elif event.obj.message['text'] == '/help':
            if event.obj.message['from_id']:
                vk_session.method("messages.send", {"user_id":event.obj.message['from_id'], "message":vk_config.COMMAND_LIST,"random_id":get_random_id()})
        elif event.obj.message['text'] == '/instruction':
            if event.obj.message['from_id']:
                vk_session.method("messages.send", {"user_id":event.obj.message['from_id'], "message":vk_config.INSTRUCTION_MESSAGE,"random_id":get_random_id()})
        elif event.obj.message['text'] == '/instruction':
            if event.obj.message['from_id']:
                vk_session.method("messages.send", {"user_id":event.obj.message['from_id'], "message":vk_config.INSTRUCTION_MESSAGE,"random_id":get_random_id()})
        elif event.obj.message['text'] == '/feedback':
            if event.obj.message['from_id']:
                vk_session.method("messages.send", {"user_id":event.obj.message['from_id'], "message":'''Введите свой отзыв (пока не работает)''',"random_id":get_random_id(), 'payload':'feedback'})
        elif event.obj.message['text'] == '/test':
            if event.obj.message['from_id']:
                settings = dict(one_time=False, inline=True)
                keyboard_1 = VkKeyboard(**settings)
                keyboard_1.add_callback_button(label='Да', payload={"type": "test_resident"})
                keyboard_1.add_callback_button(label='Нет', payload={"type": "test_not_resident"})
                vk.messages.send(user_id=event.obj.message['from_id'], random_id=get_random_id(), peer_id=event.obj.message['from_id'], keyboard=keyboard_1.get_keyboard(), message=vk_config.IS_RESIDENT)
        else:
            vk_session.method("messages.send", {"user_id":event.obj.message['from_id'], "message":vk_config.IDK,"random_id":get_random_id()})
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('type') == 'test_resident':
            settings = dict(one_time=False, inline=True)
            empty_keyboard = VkKeyboard(**settings)
            empty_keyboard.add_callback_button(label='Да', payload={"type": "empty"})
            last_id = vk.messages.edit(peer_id=event.obj.peer_id, message=vk_config.IS_RESIDENT, conversation_message_id=event.obj.conversation_message_id, keyboard=empty_keyboard.get_keyboard())

            income_keyboard = VkKeyboard(**settings)
            income_keyboard.add_callback_button(label='Да', payload={"type": "test_has_income"})
            income_keyboard.add_callback_button(label='Нет', payload={"type": "test_not_income"})
            vk.messages.send(user_id=event.obj.peer_id, random_id=get_random_id(), peer_id=event.obj.peer_id, keyboard=income_keyboard.get_keyboard(), message=vk_config.INCOME_MESSAGE)
        elif event.object.payload.get('type') == 'test_not_resident':
            settings = dict(one_time=False, inline=True)
            empty_keyboard = VkKeyboard(**settings)
            empty_keyboard.add_callback_button(label='Нет', payload={"type": "empty"})
            last_id = vk.messages.edit(peer_id=event.obj.peer_id, message=vk_config.IS_RESIDENT, conversation_message_id=event.obj.conversation_message_id, keyboard=empty_keyboard.get_keyboard())
            vk.messages.send(user_id=event.obj.peer_id, random_id=get_random_id(), peer_id=event.obj.peer_id, message=vk_config.REJECT_MESSAGE_1)
        elif event.object.payload.get('type') == 'test_has_income':
            settings = dict(one_time=False, inline=True)
            empty_keyboard = VkKeyboard(**settings)
            empty_keyboard.add_callback_button(label='Да', payload={"type": "empty"})
            last_id = vk.messages.edit(peer_id=event.obj.peer_id, message=vk_config.INCOME_MESSAGE, conversation_message_id=event.obj.conversation_message_id, keyboard=empty_keyboard.get_keyboard())
            vk.messages.send(user_id=event.obj.peer_id, random_id=get_random_id(), peer_id=event.obj.peer_id, message=vk_config.REFUND_MESSAGE_INFO)
        elif event.object.payload.get('type') == 'test_not_income':
            settings = dict(one_time=False, inline=True)
            empty_keyboard = VkKeyboard(**settings)
            empty_keyboard.add_callback_button(label='Нет', payload={"type": "empty"})
            last_id = vk.messages.edit(peer_id=event.obj.peer_id, message=vk_config.INCOME_MESSAGE, conversation_message_id=event.obj.conversation_message_id, keyboard=empty_keyboard.get_keyboard())
            vk.messages.send(user_id=event.obj.peer_id, random_id=get_random_id(), peer_id=event.obj.peer_id, message=vk_config.REJECT_MESSAGE_2)
        elif event.object.payload.get('type') == 'test_not_income':
            vk.messages.send(user_id=event.obj.peer_id, random_id=get_random_id(), peer_id=event.obj.peer_id, message='''Фидбек отправлен''')
        else:
            pass