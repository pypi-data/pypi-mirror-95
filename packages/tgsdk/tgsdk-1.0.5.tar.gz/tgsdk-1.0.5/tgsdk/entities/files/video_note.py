#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import (
	TYPE_CHECKING,
	Optional,
	Union,
	Dict
)

from tgsdk import TelegramEntity
from .photosize import PhotoSize

if TYPE_CHECKING:
	from tgsdk import (
		Bot,
		File
	)


class VideoNote(TelegramEntity):
	"""
	https://core.telegram.org/bots/api#videonote

	"""
	__slots__ = ("file_id", "file_unique_id", "length", "duration", "thumb", "file_size", "bot")

	def __init__(
		self,
		file_id: str,
		file_unique_id: str,
		length: int,
		duration: int,
		thumb: PhotoSize = None,
		file_size: int = None,

		bot: "Bot" = None
	):
		self.file_id = file_id
		self.file_unique_id = file_unique_id
		self.length = length
		self.duration = duration
		self.thumb = thumb
		self.file_size = file_size

		self.bot = bot

	@classmethod
	def de_json(cls, data: Optional[Dict] = None) -> Union["VideoNote", None]:
		"""

		:param data:
		:return:
		"""
		if not data:
			return None

		data["thumb"] = PhotoSize.de_json(data.get("thumb"))

		return cls(**data)

	def get_file(self, timeout: float = None, kwargs: Dict = None) -> "File":
		"""

		:param timeout:
		:param kwargs:
		:return:
		"""
		return self.bot.get_file(file_id=self.file_id, timeout=timeout, kwargs=kwargs)
