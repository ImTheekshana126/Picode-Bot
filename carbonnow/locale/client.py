from os.path import realpath
from io import BytesIO
from typing import Optional

import aiohttp
from aiohttp import client_exceptions

from .errors import HostDownError


class Carbon:
    def __init__(
            self,
            *,
            code: str,
            background: Optional[str] = None,
            drop_shadow: Optional[bool] = None,
            drop_shadow_blur: Optional[str] = None,
            drop_shadow_offset: Optional[str] = None,
            export_size: Optional[str] = None,
            font_size: Optional[str] = None,
            font_family: Optional[str] = None,
            first_line_number: Optional[int] = None,
            language: Optional[str] = None,
            line_height: Optional[str] = None,
            line_numbers: Optional[str] = None,
            padding_horizontal: Optional[str] = None,
            padding_vertical: Optional[str] = None,
            theme: Optional[str] = None,
            watermark: Optional[bool] = None,
            width_adjustment: Optional[bool] = None,
            window_controls: Optional[bool] = None,
            window_theme: Optional[str] = None,
    ) -> None:
        self.code = code
        self.background = background
        self.drop_shadow = drop_shadow
        self.drop_shadow_blur = drop_shadow_blur
        self.drop_shadow_offset = drop_shadow_offset
        self.export_size = export_size
        self.font_size = font_size
        self.font_family = font_family
        self.first_line_number = first_line_number
        self.language = language
        self.line_height = line_height
        self.line_numbers = line_numbers
        self.padding_horizontal = padding_horizontal
        self.padding_vertical = padding_vertical
        self.theme = theme
        self.watermark = watermark
        self.width_adjustment = width_adjustment
        self.window_controls = window_controls
        self.window_theme = window_theme

    async def req(self):
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'},) as ses:
            params = {'code': self.code, }
            if self.background:
                params['backgroundColor'] = self.background
            if self.drop_shadow:
                params['dropShadow'] = self.drop_shadow
            if self.drop_shadow_offset:
                params['dropShadowOffsetY'] = self.drop_shadow_offset
            if self.drop_shadow_blur:
                params['dropShadowBlurRadius'] = self.drop_shadow_blur
            if self.export_size:
                params['exportSize'] = self.export_size
            if self.font_size:
                params['fontSize'] = self.font_size
            if self.font_family:
                params['fontFamily'] = self.font_family
            if self.first_line_number:
                params['firstLineNumber'] = self.first_line_number
            if self.language:
                params['language'] = self.language
            if self.line_height:
                params['lineHeight'] = self.line_height
            if self.line_numbers:
                params['lineNumbers'] = self.line_numbers
            if self.padding_horizontal:
                params['paddingHorizontal'] = self.padding_horizontal
            if self.padding_vertical:
                params['paddingVertical'] = self.padding_vertical
            if self.theme:
                params['theme'] = self.theme
            if self.watermark:
                params['watermark'] = self.watermark
            if self.width_adjustment:
                params['widthAdjustment'] = self.width_adjustment
            if self.window_controls:
                params['windowControls'] = self.window_controls
            if self.window_theme:
                params['windowTheme'] = str(self.window_theme)
            try:
                request = await ses.post('https://carbonara.vercel.app/api/cook', json=params, )
            except client_exceptions.ClientConnectorError:
                raise HostDownError("Can not reach the Host!")
            return await request.read(), request

    async def memorize(self, file_name = str):
        resp, _ = await self.req()
        photo = BytesIO(resp)
        photo.name = f"{file_name}.jpg"
        return photo

    async def save(self, file_name = str):
        resp, _ = await self.req()
        with open(f"{file_name}.jpg", 'wb') as f:
            f.write(resp)
            return realpath(f.name)
