from aiogram import types, F
import json
import os
from loader import bot, dp, user_data  # Импортируем объекты

print("wallet.py загружен!")  # Проверка загрузки файла

@dp.message(F.text)  # Фильтр только текстовых сообщений
async def handle_wallet(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, ожидает ли бот кошелек от пользователя
    print(f"user_data[{user_id}] = {user_data.get(user_id)}")  # Отладка
    if user_data.get(user_id, {}).get("step") == "wallet":
        wallet_address = message.text.strip()
        print(f"Получен кошелек: {wallet_address}")  # Отладка

        if len(wallet_address) >= 34:  # Проверка только по длине
            user_file = f"users/{user_id}.json"
            os.makedirs("users", exist_ok=True)  # Создаём папку, если её нет

            with open(user_file, "w", encoding="utf-8") as file:
                json.dump({"user_id": user_id, "wallet": wallet_address}, file, indent=4)

            print(f"Файл {user_file} создан, записаны данные: {wallet_address}")  # Отладка

            await bot.send_message(
                user_id,
                f"✅ Кошелек успешно добавлен/изменен: <code>{wallet_address}</code>",
                parse_mode="HTML"
            )
            user_data.pop(user_id, None)  # Удаляем шаг
        else:
            await bot.send_message(
                user_id,
                "❌ Неверный формат кошелька. Пожалуйста, отправьте правильный адрес TON-кошелька.",
                parse_mode="HTML"
            )