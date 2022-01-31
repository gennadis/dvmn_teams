from django.core.management.base import BaseCommand
from teams.models import TimeSlot, Student, PM, Team
from django.db.models import Count

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import os
import telebot


token = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(token)


def gen_markup_time_pm1(timeslots: list[tuple]):
    markup = InlineKeyboardMarkup()
    markup.row_width = 4

    button_list = [
        InlineKeyboardButton(f"{ts}", callback_data=ts_id)
        for (ts_id, pm_name, ts) in timeslots
    ]
    markup.add(*button_list)
    return markup


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
    tg_username = f"@{message.chat.username}"

    try:
        student = Student.objects.get(tg_username=tg_username)

        bot.send_message(
            message.chat.id,
            f"Привет, {student.name} я бот который поможет тебе записаться на проекты Devman, я подберу тебе подходящее время веди команду /enroll",
        )
    except:
        bot.send_message(
            message.chat.id,
            "Уходи.",
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


class Command(BaseCommand):
    help = "Some bot help information"

    def handle(self, *args, **kwargs):

        bot.enable_save_next_step_handlers(delay=5)
        bot.load_next_step_handlers()
        bot.infinity_polling()
