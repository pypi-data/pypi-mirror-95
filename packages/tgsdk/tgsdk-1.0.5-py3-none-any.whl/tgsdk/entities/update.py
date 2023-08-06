#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import (
	Optional,
	Union,
	Dict
)

from tgsdk import (
	Message,
	CallbackQuery
)
from .base import TelegramEntity


class Update(TelegramEntity):
	"""
	https://core.telegram.org/bots/api#update

	"""

	__slots__ = ("update_id", "message", "edited_message", "channel_post", "edited_channel_post", "callback_query")

	def __init__(
		self,
		update_id: int,
		message: Message = None,
		edited_message: Message = None,
		channel_post: Message = None,
		edited_channel_post: Message = None,
		# inline_query: InlineQuery = None,
		# chosen_inline_result: 	ChosenInlineResult = None,
		callback_query: CallbackQuery = None,
		# shipping_query: ShippingQuery = None,
		# pre_checkout_query: PreCheckoutQuery = None,
		# poll: Poll = None,
		# poll_answer: PollAnswer = None
	):
		self.update_id = update_id

		self.message = message
		self.edited_message = edited_message
		self.channel_post = channel_post
		self.edited_channel_post = edited_channel_post
		# self.inline_query = inline_query
		# self.chosen_inline_result = chosen_inline_result
		self.callback_query = callback_query

	# self.shipping_query = shipping_query
	# self.pre_checkout_query = pre_checkout_query
	# self.poll = poll
	# self.poll_answer = poll_answer

	@classmethod
	def de_json(cls, data: Optional[Dict] = None) -> Union["Update", None]:
		"""

		:param data:
		:return:
		"""
		if not data:
			return None

		data["message"] = Message.de_json(data.get("message"))
		data["edited_message"] = Message.de_json(data.get("edited_message"))
		# data["inline_query"] = InlineQuery.de_json(data.get("inline_query"))
		# data["chosen_inline_result"] = ChosenInlineResult.de_json(data.get("chosen_inline_result"))
		data["callback_query"] = CallbackQuery.de_json(data.get("callback_query"))
		# data["shipping_query"] = ShippingQuery.de_json(data.get("shipping_query"))
		# data["pre_checkout_query"] = PreCheckoutQuery.de_json(data.get("pre_checkout_query"))
		data["channel_post"] = Message.de_json(data.get("channel_post"))
		data["edited_channel_post"] = Message.de_json(data.get("edited_channel_post"))
		# data["poll"] = Poll.de_json(data.get("poll"))
		# data["poll_answer"] = PollAnswer.de_json(data.get("poll_answer"))

		return cls(**data)
