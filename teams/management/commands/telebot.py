import os

import telebot
from django.core.management.base import BaseCommand
from django.db.models import Count
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from teams.models import TimeSlot, Student, PM, Team


token = os.environ["TELEGRAM_TOKEN"]
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start_message(message) -> Message:
    tg_username = f"@{message.chat.username}"

    try:
        student = Student.objects.get(tg_username=tg_username)

        if not student.in_team:
            bot.send_message(
                chat_id=message.chat.id,
                text=f"""Привет, {student.name}!\n
                Я помогу тебе записаться на текущий командный проект Devman.\n
                Для продолжения введи команду /enroll""",
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=f"""{student.name}, ты уже записан на командный проект.\n
                Время созвона: {student.timeslot.timeslot.first()}.""",
            )
    except:
        bot.send_message(
            chat_id=message.chat.id,
            text="""Вероятно, ты не являешься студентом Devman.\n
            Вступай в наши ряды по ссылке: https://dvmn.org/""",
        )


@bot.message_handler(commands=["enroll"])
def start(message) -> Message:
    bot.send_message(
        chat_id=message.chat.id,
        text="Ты готов записаться на командный проект?",
        reply_markup=draw_yes_no_buttons(),
    )


def draw_yes_no_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Да", callback_data="yes"),
        InlineKeyboardButton("Нет", callback_data="no"),
    )

    return markup


def draw_timeslots(timeslots: list[tuple]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    button_list = [
        InlineKeyboardButton(f"{pm_name}:\n{timeslot}", callback_data=timeslot_pk)
        for (timeslot_pk, pm_name, timeslot) in timeslots
    ]
    markup.add(*button_list)

    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    tg_username = f"@{call.message.chat.username}"
    student = Student.objects.get(tg_username=tg_username)

    if not student.in_team:
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
                chat_id=call.message.chat.id,
                text="Выбери продакт менеджера и удобное время для ежедневного созвона с командой.",
                reply_markup=draw_timeslots(timeslots),
            )
        elif call.data == "no":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Когда будешь готов - введи /start",
                reply_markup=None,
            )

        else:
            user_timeslot_pick = call.data

            user_team = available_teams.filter(timeslot=user_timeslot_pick).first()
            user_team.students.add(student)
            user_team.save()

            student.in_team = True
            student.timeslot.add(int(user_timeslot_pick))
            student.save()

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"""Отлично!\n
                Ты записан к {user_team.pm}: {user_team.pm.tg_username} на {user_team.timeslot.timeslot}.\n
                Студенты в твоей команде:\n
                {', '.join([f'{student.name}: {student.tg_username}' for student in user_team.students.all()])}""",
                reply_markup=None,
            )

    else:
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"""{student.name}, ты уже записан на командный проект.\n
                Время созвона: {student.timeslot.timeslot.first()}.""",
        )


class Command(BaseCommand):
    help = "Some bot help information"

    def handle(self, *args, **kwargs):

        bot.enable_save_next_step_handlers(delay=5)
        bot.load_next_step_handlers()
        bot.infinity_polling()
