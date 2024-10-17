import vk_api
from aiogram import Bot
from aiogram.types import InputMediaPhoto
import asyncio
from models import Post
import time

str = """https://oauth.vk.com/blank.html#access_token=vk1.a.IfQxGJxytk1Ubr3IPlEQptSzD6jRDZ0rJ2eKTfhIQ8tZ-forg99JWIBpABaEj34-QYl1GwsBjeVmMHPB33g2dfcWEM8h7fuTaGhzZC0I67V9E92M9CkGE-uZiqi6Nx6YmmwE6Yu-pxnWZ5GCcYGVXmII9C08MnGQBsDx8K5wpZwQjQXUjXGf7Puf2NmwUTevlfI-rkGi8BBDvFKERMrF8w&expires_in=0&user_id=465645993&email=mdolgov322@gmail.com"""

ACCESS_TOKEN = str.split("access_token=")[1].split("&")[0]
BOT_TOKEN = "7598265103:AAH3-9TIPBx1HbyGLxLOPM9us3oL91-BPCA"
CHANNEL_ID = -1002386815104
GROUP_ID= "depressedprince"

session = vk_api.VkApi(token=ACCESS_TOKEN)
vk = session.get_api()


def get_posts_from_group(group_id):
    posts = vk.wall.get(owner_id=group_id, count=15)
    return posts


def get_post_photo_urls(post: dict) -> list[str] | None:
    try:
        photos = post.get('attachments')
        urls = []
        for photo in photos:
            urls.append(photo.get('photo').get('sizes')[-1].get('url'))
        return urls
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_all_posts_from_group(group_id: str) -> dict:
    posts = get_posts_from_group(group_id)
    posts = posts.get('items')
    return posts


bot = Bot(token=BOT_TOKEN)


async def send_photos_to_channel(photos: list, channel_id: str = CHANNEL_ID):
    if len(photos) > 9:
        photos = photos[:9]

    media_group = []

    for photo in photos:
        media_group.append(InputMediaPhoto(media=photo))

    await bot.send_media_group(chat_id=channel_id, media=media_group)


def loop():
    posts = get_posts_from_group(GROUP_ID)
    posts = posts.get('items')
    for post in posts:
        p = Post.get_or_none(post_id=post.get('id'))
        print(post.get('id'))
        if p: continue
        p = Post.create(post_id=post.get('id'))
        p.save()
        links = get_post_photo_urls(post)
        if not links: continue
        asyncio.run(send_photos_to_channel(links))
        break
    time.sleep(60*60)

    # print(posts.get('items')[1].get('id'))
    # print(posts.get('items')[0])
    # links = get_post_photo_urls(posts.get('items')[1])
    # asyncio.run(send_photos_to_channel(links))
    # attachments = posts.get('items')[0].get('attachments')
    # print(len(attachments))
    # print(attachments[0].get('photo').get('sizes')[-1].get('url'))


def main():
    while True:
        try:
            loop()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60*5)


if __name__ == "__main__":
    main()
