# 🌟 Contributing to Telegram Book Converter Bot

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/telegram-book-converter-bot.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## 💻 Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/telegram-book-converter-bot.git
cd telegram-book-converter-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your bot token

# Install Calibre (for book conversion)
# Ubuntu/Debian:
sudo apt install calibre
# macOS:
brew install calibre
# Windows: Download from https://calibre-ebook.com/

# Run the bot
python bot.py
```

## 🧪 Testing

```bash
# Run converter tests
python test_converter.py

# Check deployment readiness
./check_deploy.sh

# Test Docker build (optional)
docker build -t telegram-bot-test .
```

## 📝 Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions small and focused
- Use meaningful variable names

## 🐛 Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs/error messages

## ✨ Feature Requests

- Check existing issues first
- Describe the use case clearly
- Explain why the feature would be useful
- Consider implementation complexity

## 📋 Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Include tests for new functionality
- Update documentation if needed
- Ensure CI checks pass
- Write clear commit messages

## 🔒 Security

Report security vulnerabilities privately to the maintainers.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
