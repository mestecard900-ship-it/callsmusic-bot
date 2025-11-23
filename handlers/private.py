from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant

from config import FORCE_CHANNEL
from ..helpers.filters import other_filters2


# فحص الاشتراك الإجباري
async def check_force_sub(client: Client, message: Message) -> bool:
    if not FORCE_CHANNEL:
        return True

    try:
        member = await client.get_chat_member(FORCE_CHANNEL, message.from_user.id)

        if member.status in ("left", "kicked"):
            raise UserNotParticipant

        return True

    except UserNotParticipant:
        text = (
            "⚠️︙عذراً عزيزي\n"
            "⚠️︙عليك الانضمام إلى قناة البوت أولاً\n"
            f"⚠️︙قناة البوت : @{FORCE_CHANNEL}"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ الانضمام الى القناة",
                        url=f"https://t.me/{FORCE_CHANNEL}",
                    )
                ]
            ]
        )

        await message.reply_text(
            text,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )
        return False

    except Exception:
        return True


@Client.on_message(other_filters2)
async def start(client: Client, message: Message):

    # فحص الاشتراك الإجباري
    if not await check_force_sub(client, message):
        return

    # رسالة الترحيب العربية بالأيقونات
    await message.reply_text(
        f"👋🏻 أهلـين فيك يا غالي <b>{message.from_user.mention}</b> ❤️\n\n"
        "✨ هذه أوامر تشغيل الموسيقى:\n\n"
        "🎵 <b>تشغيل / شغلي</b>\n"
        "› اكتب اسم الأغنية، أو ضع رابط يوتيوب، أو رد على ملف صوتي.\n\n"
        "⏹ <b>إيقاف</b>\n"
        "› لإنهاء التشغيل وخروج المساعد من المكالمة الصوتية.\n\n"
        "⏭ <b>تخطي</b>\n"
        "› الانتقال إلى المقطع التالي في قائمة الانتظار.\n\n"
        "⏩ <b>تقديم</b>\n"
        "› اكتب الأمر + عدد الثواني لتقديم المقطع.\n\n"
        "⏪ <b>رجوع</b>\n"
        "› اكتب الأمر + عدد الثواني للرجوع.\n\n"
        "🔎 <b>بحث / يوت</b>\n"
        "› للبحث عن أغنية وتحميلها من اليوتيوب.\n\n"
        "📞 <b>انضم</b>\n"
        "› لإدخال حساب المساعد للمكالمة الصوتية.\n\n"
        "✨ سعيدين بوجودك! استمتع ❤️",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔈 قناة البوت", url="https://t.me/xx_aa_i"),
                    InlineKeyboardButton("💬 جروب الدعم", url="https://t.me/zzmaa"),
                ]
            ]
        ),
        disable_web_page_preview=True,
    )