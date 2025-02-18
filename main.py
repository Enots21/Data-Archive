from gspread import Client, Spreadsheet, Worksheet, service_account
import matplotlib.pyplot as plt
import pandas as pd


table_link = 'https://docs.google.com/spreadsheets/d/15xrQdG2kQcYiUwjLyloppOjZwoUtKn-bOFOKPTEOWYU/edit?usp=sharing'
table_id = '15xrQdG2kQcYiUwjLyloppOjZwoUtKn-bOFOKPTEOWYU'

def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename='apikeygg-451208-1b175f90ccc4.json')

def get_table_by_url(client: Client, table_url):
    """Получение таблицы из Google Sheets по ссылке."""
    return client.open_by_url(table_url)


def get_table_by_id(client: Client, table_url):
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_url)


#==============

def get_worksheet_info(table: Spreadsheet) -> dict:
    """Возвращает количество листов в таблице и их названия."""
    worksheets = table.worksheets()
    worksheet_info = {
        "count": len(worksheets),
        "names": [worksheet.title for worksheet in worksheets]
    }
    return worksheet_info

spisok = []

def main():
    # Создаем клиента и открываем таблицу
    client = client_init_json()
    table = get_table_by_id(client, table_id)

    # Получаем информацию о листах
    info = get_worksheet_info(table)
    print(info)  # Выводим информацию о листах

    # Выбор листа "data"
    sheet = table.worksheet("data")  # Исправлено: используем table вместо spreadsheet

    # Получение всех значений из столбца Б (индекс 2)
    column_b_values = sheet.col_values(2)[1:]  # Пропускаем заголовок
    group = sheet.col_values(5)[1:]  # Пропускаем заголовок

    istem = 0

    ss = 0

    for date, group in zip(column_b_values, group):
        spisok.append(f'{date} | {group}')

        # Проверяем, является ли group числом (float или int)
        sde = int(group)  # Преобразуем в int
        if isinstance(sde, (int, float)):
            try:
                # Преобразуем дату в числовое представление (timestamp)
                date_numeric = pd.to_datetime(date).timestamp()  # Требуется import pandas as pd

                plt.plot(date_numeric, sde, marker='o', linestyle='--')  # Добавляем маркеры для лучшей видимости
                plt.xlabel("Date")
                plt.ylabel("Group Value")
                plt.title(f"График зависимости Group от Date ({date})")
                plt.xticks(rotation=45)  # Поворачиваем метки оси X для читаемости
                plt.tight_layout()  # Предотвращает обрезание меток
                ss += 1

                # Показываем график каждые 7 итераций (или чаще)
                if ss % 7 == 0:
                    plt.show()
                    plt.clf()  # Очищаем текущую фигуру для следующего графика

            except ValueError:
                print(f"Не удалось преобразовать дату '{date}' в числовой формат.")

        else:
            print(f"Значение group '{group}' не является числом.")

    # Финальный показ для отображения оставшихся графиков
    if ss > 0:  # Показывать только если что-то было нарисовано
        plt.autoscale()  # Автоматическое масштабирование
        plt.show()
        plt.clf()  # Очищаем фигуру после последнего показа


if __name__ == '__main__':  # Исправлено: правильное условие для запуска main
    main()