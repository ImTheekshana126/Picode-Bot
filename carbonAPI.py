from carbonnow.locale import Carbon
import db_connector


async def carbonPhoto(user_text, user_id):
    carbon = Carbon(
        code=user_text,
        theme=db_connector.themeANDcolor(user_id)['theme'],
        background=db_connector.themeANDcolor(user_id)['color'],
        language="auto",
        drop_shadow=True,
        drop_shadow_blur='68px',
        drop_shadow_offset='20px',
        font_family='JetBrains Mono',
        width_adjustment=True,
        watermark=False,
    )

    await carbon.save(f'carboned_{user_id}')
