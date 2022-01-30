from django.core.management.base import BaseCommand
from teams.models import TimeSlot, Student, PM, Team
from django.db.models import Count

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import os
import telebot


token = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(token)
print(bot.get_me())


def check_user(user):
    if user:
        return f"@{user}"


def gen_markup_time_pm1(timeslots: list[tuple]):
    markup = InlineKeyboardMarkup()
    markup.row_width = 4

    button_list = [
        InlineKeyboardButton(f"{ts}", callback_data=ts_id)
        for (ts_id, pm_name, ts) in timeslots
    ]
    markup.add(*button_list)
    return markup


# def gen_markup_time_pm2():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 4
#     button_list = [
#         InlineKeyboardButton(f"{i}", callback_data=f"{i}") for i in time_slot_pm2
#     ]
#     print(button_list)
#     markup.add(*button_list)
#     return markup


def gen_markup_pm():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Да", callback_data="yes"),
        InlineKeyboardButton("Нет", callback_data="no"),
    )
    return markup


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        f"Привет, я бот который поможет тебе записаться на проекты Devman, я подберу тебе подходящее время веди команду /enroll",
    )


@bot.message_handler(commands=["enroll"])
def start(message):
    bot.send_message(
        message.chat.id, "Готов записаться на проект?", reply_markup=gen_markup_pm()
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    tg_username = f"@{call.message.chat.username}"
    student = Student.objects.get(tg_username=tg_username)

    available_teams = (
        Team.objects.annotate(students_in_team=Count("students"))
        .filter(
            level=student.level,
            students_in_team__lt=3,
        )
        .all()
    )

    timeslots = [
        (team.timeslot.pk, team.pm.name, team.timeslot.timeslot)
        for team in available_teams
    ]

    if call.data == "yes":
        bot.send_message(
            call.message.chat.id,
            "У ПМов есть следующее свободное время, выбирай",
            reply_markup=gen_markup_time_pm1(timeslots),
        )
    elif call.data == "no":
        bot.send_message(
            call.message.chat.id,
            "Заходи когда будет удобно введи /start и подтверди выбор",
            reply_markup=None,
        )

    else:
        users_timeslot_pick = call.data

        users_team = available_teams.filter(timeslot=users_timeslot_pick).first()
        users_team.students.add(student)
        users_team.save()
        student.in_team = True
        student.save()

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Ты успешно записан на выбранное время, your team ID {users_team}, your team PM {users_team.pm} Students in your team: {[student.name for student in users_team.students.all()]}",
            reply_markup=None,
        )
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text=f"Ты успешно записан на выбранное время, your team ID {users_team}, your team PM {users_team.pm} Students in your team: {[student.name for student in users_team.students.all()]}",
        )


@bot.message_handler(commands=["help"])
def start(message):
    bot.send_message(message.chat.id, "просто введи /enroll")

    # end_time = 0
    # time_slot_pm1 = []
    # time_slot_pm2 = []

    # create Student instance
    # student = Student.objects.get(tg_username=input("Enter students tg_username "))
    # print(f"Hello, {student.name}!")

    # get all available teams filtered by level and capacity
    # available_teams = (
    #     Team.objects.annotate(students_in_team=Count("students"))
    #     .filter(
    #         level=student.level,
    #         students_in_team__lt=3,
    #     )
    #     .all()
    # )
    # print(f"Available teams IDs: {[team.pk for team in available_teams]}")

    # get available timeslots
    # timeslots = [
    #     (team.timeslot.pk, team.pm.name, team.timeslot.timeslot)
    #     for team in available_teams
    # ]
    # print(f"Available teams timeslots: {timeslots}")

    # # get user's timeslot choice primary key
    # users_ts_choice = input("Choose timeslot primary key ")

    # # get first team that fits by timeslot - from available teams
    # users_team = available_teams.filter(timeslot=users_ts_choice).first()
    # print(f"Your team ID is {users_team}")

    # # add student to team and save
    # users_team.students.add(student)
    # users_team.save()
    # student.in_team = True
    # student.save()

    # # get all team students
    # print(
    #     f"Students in your team: {[student.name for student in users_team.students.all()]}"
    # )

    # # check all populated teams
    # print("#" * 50)
    # print("ALL TEAMS")
    # get_populated_teams()


class Command(BaseCommand):
    help = "Some bot help information"

    def handle(self, *args, **kwargs):

        bot.enable_save_next_step_handlers(delay=5)
        bot.load_next_step_handlers()
        bot.infinity_polling()
