#!/bin/bash

# Запускаємо першу команду
python predict_bot.py

# Перевірка на код виходу та виконання наступної команди
if [ $? -eq 0 ]; then
    # Запускаємо другу команду
    python autotask_cleaner.py

    # Перевірка на код виходу та виконання наступної команди
    if [ $? -eq 0 ]; then
        # Запускаємо третю команду
        python currency_stock_data/auto_task.py
    fi
fi
