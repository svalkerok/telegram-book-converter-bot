"""
🎨 Генератор иконки для GUI приложения
Icon generator for GUI application
"""

def create_simple_icon():
    """Создает простую иконку в формате ICO"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Создаем изображение 64x64
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Рисуем круглый фон
        margin = 4
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill=(33, 150, 243, 255))  # Синий цвет
        
        # Добавляем текст "BOT"
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        text = "🤖"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Центрируем текст
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        # Сохраняем как ICO
        img.save('bot_icon.ico', format='ICO', sizes=[(64, 64), (32, 32), (16, 16)])
        print("✅ Иконка bot_icon.ico создана")
        return True
        
    except ImportError:
        print("⚠️ PIL не установлен, создаем простую иконку")
        return False
    except Exception as e:
        print(f"❌ Ошибка создания иконки: {e}")
        return False

def create_fallback_icon():
    """Создает простую иконку без PIL"""
    # Создаем простой файл иконки (placeholder)
    icon_data = b'''
    Simple icon placeholder
    This will be replaced with proper icon generation
    '''
    
    with open('bot_icon.txt', 'w') as f:
        f.write("🤖 Bot Icon Placeholder\n")
        f.write("For proper icon, install PIL: pip install Pillow\n")
    
    print("📝 Создан placeholder для иконки")

if __name__ == "__main__":
    print("🎨 Создание иконки для GUI приложения...")
    
    if not create_simple_icon():
        create_fallback_icon()
    
    print("✅ Иконка готова!")
