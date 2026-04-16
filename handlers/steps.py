from aiogram import types, F
import json
import os
from loader import bot, dp, user_data  

@dp.message()
async def handle_steps(message: types.Message):
    user_id = message.from_user.id
    step = user_data.get(user_id, {}).get("step")

    if step == "amount":
        try:
            amount = float(message.text.strip())

            user_data[user_id]["amount"] = amount
            user_data[user_id]["step"] = "description"

            await bot.send_message(
                user_id,
                "📝 <b>Укажите, что вы предлагаете в этой сделке:</b>\n\n"
                "Пример: <i>10 кепок и 5 пепе...</i>",
                reply_markup=back_button,
                parse_mode="HTML"
            )
        except ValueError:
            await bot.send_message(
                user_id,
                "❌ Пожалуйста, введите сумму в правильном формате (например, <code>100.5</code>).",
                reply_markup=back_button,
                parse_mode="HTML"
            )

    elif step == "description":
        description = message.text.strip()
        user_data[user_id]["description"] = description

        random_start = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        user_data[user_id]["link"] = f"https://t.me/giftselfsrobot?start={random_start}"

        deal_data = {
            "user_id": user_id,
            "amount": user_data[user_id]["amount"],
            "description": user_data[user_id]["description"],
            "link": user_data[user_id]["link"],
            "seller_id": user_id,
            "random_start": random_start
        }
        deal_file_path = f"deals/{random_start}.json"
        with open(deal_file_path, "w", encoding="utf-8") as file:
            json.dump(deal_data, file, ensure_ascii=False, indent=4)

        await bot.send_message(
            user_id,
            "✅ <b>Сделка успешно создана!</b>\n\n"
            f"💰 <b>Сумма:</b> {deal_data['amount']} TON\n"
            f"📜 <b>Описание:</b> {deal_data['description']}\n"
            f"🔗 <b>Ссылка для покупателя:</b> {deal_data['link']}",
            reply_markup=cancel_deal_button,
            parse_mode="HTML"
        )

        user_data.pop(user_id, None)