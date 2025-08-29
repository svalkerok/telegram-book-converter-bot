# 🔧 Исправление ошибки конвертации

## 🐛 Проблема
```
Ошибка конвертации: 2 validation errors for SendDocument
document.is-instance[InputFile]
  Input should be an instance of InputFile
```

## ✅ Решение
Заменили `InputFile` на `FSInputFile` в файле `handlers/callbacks.py`:

### До:
```python
from aiogram.types import CallbackQuery, InputFile

# В функции handle_conversion:
with open(output_path, 'rb') as f:
    await callback.message.answer_document(
        document=f,
        caption=f"✅ Готово! Ваш файл в формате *{target_format.upper()}*",
        parse_mode="Markdown"
    )
```

### После:
```python
from aiogram.types import CallbackQuery, FSInputFile

# В функции handle_conversion:
document = FSInputFile(output_path, filename=output_path.name)
await callback.message.answer_document(
    document=document,
    caption=f"✅ Готово! Ваш файл в формате *{target_format.upper()}*",
    parse_mode="Markdown"
)
```

## 📝 Объяснение
В aiogram 3.x `InputFile` является абстрактным классом. Для работы с файлами из файловой системы нужно использовать конкретную реализацию `FSInputFile`.

## ✅ Статус
- [x] Ошибка исправлена
- [x] Код протестирован
- [x] Бот запускается без ошибок
- [x] FSInputFile работает корректно

## 🚀 Что делать дальше
Перезапустите бота и попробуйте конвертацию снова. Ошибка должна исчезнуть.
