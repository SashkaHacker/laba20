#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

import click

from validation import ListWorkers


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename")
@click.argument("surname")
@click.argument("name")
@click.argument("phone")
@click.argument("date")
def add(filename, surname, name, phone, date):
    lst = load_workers(filename)
    add_worker(lst, surname, name, phone, date)
    save_workers(filename, lst)


@cli.command()
@click.argument("filename")
def display(filename):
    lst = load_workers(filename)
    show_workers(lst)


@cli.command()
@click.argument("filename")
@click.argument("phone")
def select(filename, phone):
    lst = load_workers(filename)
    select_phone(lst, phone)


def add_worker(lst, surname, name, phone, date):
    dct = {
        "surname": surname,
        "name": name,
        "phone": phone,
        "date": date.split(":"),
    }
    lst.append(dct)


def select_phone(lst, numbers_phone):
    numbers_phone = int(numbers_phone)
    fl = True
    for i in lst:
        if i["phone"] == numbers_phone:
            print(
                f"Фамилия: {i['surname']}\n"
                f"Имя: {i['name']}\n"
                f"Номер телефона: {i['phone']}\n"
                f"Дата рождения: {':'.join(i['date'])}"
            )
            fl = False
            break
    if fl:
        print("Человека с таким номером телефона нет в списке.")


def instruction():
    print(
        "add - добавление нового работника\n"
        "phone - данные о работнике по его номеру телефона\n"
        "exit - завершение программ\n"
        "list - список работников\n"
        "save filename - сохранить данные в json файл\n"
    )


def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        data = json.load(fin)
    try:
        ListWorkers(lst=data)
        data.sort(
            key=lambda x: datetime.strptime("-".join(x["date"]), "%d-%m-%Y")
        )
        return data
    except Exception:
        print("Invalid JSON")


def show_workers(lst):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if lst:
        # Блок заголовка таблицы
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 15, "-" * 15
        )
        print(line)
        print(
            f'| {"№":^4} | {"Фамилия":^30} | {"Имя":^20} | '
            f'{"Номер телефона":^15} | {"Дата рождения":^15} |'
        )

        print(line)
        # Вывести данные о всех сотрудниках.
        for idx, worker in enumerate(lst, 1):
            print(
                f'| {idx:>4} | {worker.get("surname", ""):<30} | '
                f'{worker.get("name", ""):<20}'
                f' | {worker.get("phone", 0):>15}'
                f' | {":".join(worker.get("date", 0)):>15} |'
            )

        print(line)
    else:
        print("Список работников пуст.")


if __name__ == "__main__":
    cli()
