# 🏗️ PowerShell скрипт сборки Windows EXE файла
# Build script for Windows EXE file

param(
    [switch]$Clean = $false,
    [switch]$Verbose = $false
)

# Функции для вывода
function Write-BuildMessage {
    param($Message)
    Write-Host "[BUILD] $Message" -ForegroundColor Green
}

function Write-InfoMessage {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-WarningMessage {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-ErrorMessage {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

try {
    Write-BuildMessage "Начинаем сборку Windows EXE файла..."

    # Проверка виртуального окружения
    if (Test-Path "venv\Scripts\Activate.ps1") {
        Write-InfoMessage "Активация виртуального окружения..."
        & "venv\Scripts\Activate.ps1"
        Write-InfoMessage "✅ Виртуальное окружение активировано"
    } else {
        Write-ErrorMessage "Виртуальное окружение не найдено!"
        Write-InfoMessage "Создайте виртуальное окружение: python -m venv venv"
        exit 1
    }

    # Проверка зависимостей
    Write-BuildMessage "🔍 Проверка зависимостей..."

    # Проверяем PyInstaller
    try {
        python -c "import PyInstaller" 2>$null
        if ($LASTEXITCODE -ne 0) { throw }
    } catch {
        Write-InfoMessage "📦 Установка PyInstaller..."
        pip install pyinstaller
    }

    # Проверяем Pillow
    try {
        python -c "import PIL" 2>$null
        if ($LASTEXITCODE -ne 0) { throw }
    } catch {
        Write-InfoMessage "📦 Установка Pillow..."
        pip install Pillow
    }

    # Проверяем основные зависимости
    $dependencies = @(
        @{name="customtkinter"; import="customtkinter"},
        @{name="requests"; import="requests"},
        @{name="python-dotenv"; import="dotenv"},
        @{name="aiogram"; import="aiogram"},
        @{name="aiofiles"; import="aiofiles"}
    )

    foreach ($dep in $dependencies) {
        try {
            python -c "import $($dep.import)" 2>$null
            if ($LASTEXITCODE -ne 0) { throw }
        } catch {
            Write-ErrorMessage "❌ Зависимость $($dep.name) не найдена!"
            Write-InfoMessage "Установите: pip install $($dep.name)"
            exit 1
        }
    }

    Write-InfoMessage "✅ Все зависимости проверены"

    # Создание иконки
    Write-BuildMessage "🎨 Создание иконки..."
    if (-not (Test-Path "bot_icon.ico")) {
        python create_icon.py
    } else {
        Write-InfoMessage "✅ Иконка уже существует"
    }

    # Очистка предыдущих сборок
    Write-BuildMessage "🧹 Очистка предыдущих сборок..."
    
    $cleanDirs = @("build", "dist")
    foreach ($dir in $cleanDirs) {
        if (Test-Path $dir) {
            Remove-Item -Recurse -Force $dir
            Write-InfoMessage "✅ Директория $dir очищена"
        }
    }

    if (Test-Path "TelegramBotGUI.exe") {
        Remove-Item "TelegramBotGUI.exe"
        Write-InfoMessage "✅ Старый EXE файл удален"
    }

    # Сборка с PyInstaller
    Write-BuildMessage "🚀 Сборка исполняемого файла..."
    
    $buildArgs = @("bot_gui.spec", "--clean", "--noconfirm")
    if ($Verbose) {
        $buildArgs += "--log-level=DEBUG"
    }
    
    & pyinstaller @buildArgs
    
    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "❌ Ошибка при сборке!"
        exit 1
    }

    # Перемещение результата
    if (Test-Path "dist\TelegramBotGUI.exe") {
        Move-Item "dist\TelegramBotGUI.exe" "TelegramBotGUI.exe"
        Write-InfoMessage "✅ EXE файл перемещен в корневую директорию"
    } else {
        Write-ErrorMessage "❌ EXE файл не найден в dist/"
        exit 1
    }

    # Создание дистрибутива
    Write-BuildMessage "📦 Создание дистрибутива..."
    
    $distDir = "TelegramBotGUI_Distribution"
    if (Test-Path $distDir) {
        Remove-Item -Recurse -Force $distDir
    }
    
    New-Item -ItemType Directory -Path $distDir | Out-Null
    
    # Копирование файлов
    $filesToCopy = @(
        "TelegramBotGUI.exe",
        "README.md",
        "GUI_GUIDE.md", 
        "WINDOWS_SETUP.md"
    )
    
    foreach ($file in $filesToCopy) {
        if (Test-Path $file) {
            Copy-Item $file "$distDir\"
        }
    }

    # Создание start.bat
    $startBatContent = @"
@echo off
echo Запуск Telegram Bot GUI...
TelegramBotGUI.exe
pause
"@
    Set-Content -Path "$distDir\start.bat" -Value $startBatContent -Encoding ASCII

    Write-InfoMessage "✅ Дистрибутив создан в $distDir/"

    # Создание архива
    Write-BuildMessage "📁 Создание архива..."
    
    $zipPath = "TelegramBotGUI_Windows.zip"
    if (Test-Path $zipPath) {
        Remove-Item $zipPath
    }

    Compress-Archive -Path "$distDir\*" -DestinationPath $zipPath

    if (Test-Path $zipPath) {
        Write-InfoMessage "✅ Архив $zipPath создан"
    } else {
        Write-WarningMessage "⚠️ Не удалось создать архив"
    }

    # Очистка временных файлов
    if ($Clean) {
        Write-BuildMessage "🧹 Очистка временных файлов..."
        $cleanDirs = @("build", "dist")
        foreach ($dir in $cleanDirs) {
            if (Test-Path $dir) {
                Remove-Item -Recurse -Force $dir
            }
        }
    }

    # Результат
    Write-Host ""
    Write-BuildMessage "🎉 Сборка завершена успешно!"
    Write-Host ""
    Write-Host "📁 Результаты:" -ForegroundColor Cyan
    Write-Host "   - TelegramBotGUI.exe (исполняемый файл)" -ForegroundColor White
    Write-Host "   - $distDir/ (дистрибутив)" -ForegroundColor White
    Write-Host "   - $zipPath (архив для распространения)" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Для запуска: TelegramBotGUI.exe" -ForegroundColor Green
    Write-Host "📖 Инструкции: README.md в дистрибутиве" -ForegroundColor Green
    Write-Host ""

} catch {
    Write-ErrorMessage "❌ Произошла ошибка: $_"
    exit 1
}
