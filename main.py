import matplotlib.pyplot as plt
import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta


def get_currency_rates(date=None):

    base_url = 'https://www.cbr-xml-daily.ru'

    if date is None:
        url = f'{base_url}/daily_json.js'
    else:
        # Конвертируем дату из формата ДД/ММ/ГГГГ в ГГГГ/ММ/ДД
        date_obj = datetime.strptime(date, '%d/%m/%Y')
        formatted_date = date_obj.strftime('%Y/%m/%d')
        url = f'{base_url}/archive/{formatted_date}/daily_json.js'

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Данные на {date} не найдены")
        else:
            print(f"Ошибка HTTP: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return None


def print_currency_rates(rates_data):
    if not rates_data:
        print("Нет данных для отображения")
        return

    date = datetime.strptime(rates_data['Date'][:10], '%Y-%m-%d').strftime('%d.%m.%Y')
    print(f"\nКурсы валют на {date}:")
    print("-" * 40)
    names = []
    prices = []
    for currency_code, currency_info in rates_data.get('Valute', {}).items():
        name = currency_info['Name']
        value = currency_info['Value']
        nominal = currency_info['Nominal']
        rate = value / nominal
        print(f"{name} ({currency_code}): {rate:.4f} руб.")
        names.append(currency_code)
        prices.append(rate)
    plt.figure(figsize=(14, 8))
    plt.plot(names, prices, color='red', marker='x', markersize=4)
    plt.xlabel('Валюта')
    plt.ylabel('Курс')
    plt.xticks(rotation=90)
    plt.show()
def get_valid_date():
    while True:
        date_str = input("Введите дату в формате ДД/ММ/ГГГГ (или Enter для текущей даты): ").strip()

        if not date_str:
            return None

        try:
            date = datetime.strptime(date_str, '%d/%m/%Y')
            if date > datetime.now():
                print("Дата ещё не наступила")
                continue
            return date_str
        except ValueError:
            print("Неверный формат даты")




def main():
    print("Парсер курсов валют с API ЦБ РФ")
    print("=" * 40)
"""
    while True:
        print("\nМеню:")
        print("1. Текущие курсы валют")
        print("2. Курсы валют на определенную дату")
        print("3. Выход")

        choice = input("Выберите опцию (1-3): ")

        if choice == '1':
            rates = get_currency_rates()
            print_currency_rates(rates)
        elif choice == '2':
            date_str = get_valid_date()
            rates = get_currency_rates(date_str)
            print_currency_rates(rates)
        elif choice == '3':
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
"""

def current():
    rates = get_currency_rates()
    print_currency_rates(rates)

def history():
    date_str = get_valid_date()
    rates = get_currency_rates(date_str)
    print_currency_rates(rates)

def exit():
    print("До свидания!")
    root.destroy()

root = tk.Tk()
root.title("Меню курсов валют")
root.geometry("300x200")

label = tk.Label(root, text="Меню:", font=('Arial', 14))
label.pack(pady=10)
btn1 = tk.Button(root,text="1. Текущие курсы валют", command=current,padx = 25,pady = 5,bd = 0, fg = 'red', bg = 'blue', cursor = 'pencil')
btn1.pack(pady=5)
btn2 = tk.Button(root,text="2. Курсы валют на определенную дату", command=history,padx = 25,pady = 5,bd = 0, fg = 'red', bg = 'blue', cursor = 'clock')
btn2.pack(pady=5)
btn3 = tk.Button(root,text="3. Выход", command=exit,padx = 25,pady = 5,bd = 0, fg = 'red', bg = 'blue', cursor = 'spider')
btn3.pack(pady=5)

root.mainloop()


if __name__ == "__main__":
    main()