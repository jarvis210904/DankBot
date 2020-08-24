from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.dispatcher import run_async

from .drake import drake
from .helpers import helper_b, helper_despacito, helper_fry, helper_generate, helper_gif, helper_image, helper_text
from .utils.logs import log_command, log_error, log_message
from .utils.text import changes, chars, commands, cookbook, vaportext


@run_async
def error_handler(update: Update, context: CallbackContext):
	log_error(f'Update "{update}" caused error "{context.error}"')


@run_async
def start_handler(update: Update, context: CallbackContext):
	update.message.reply_markdown(f'*This is DankBot!*\n{commands}', quote=True)
	log_command(update, 'START')


@run_async
def help_handler(update: Update, context: CallbackContext):
	update.message.reply_markdown(commands, quote=True)
	log_command(update, 'HELP')


@run_async
def changes_handler(update: Update, context: CallbackContext):
	update.message.reply_markdown(changes, quote=True)
	log_command(update, 'CHANGES')


@run_async
def cookbook_handler(update: Update, context: CallbackContext):
	update.message.reply_markdown(cookbook, quote=True)
	log_command(update, 'COOKBOOK')


@run_async
def alt_handler(update: Update, context: CallbackContext):
	text = update.message.text[4:].lower()
	result, upper = [update.message.from_user.first_name, ':'], False
	for i in text:
		if i.lower() in chars:
			result.append(i.upper() if upper else i.lower())
			upper = not upper
		else:
			result.append(i)
	if update.message.reply_text("".join(result), quote=True):
		update.message.delete()
	log_command(update, 'ALT')


@run_async
def vaporize_handler(update: Update, context: CallbackContext):
	text = update.message.text[10:]
	result = [update.message.from_user.first_name, ':']
	for i in text:
		if i in vaportext:
			result.append(vaportext[i])
		else:
			result.append(i)
	if update.message.reply_text("".join(result)):
		update.message.delete()
	log_command(update, 'VAPORIZE')


@run_async
def reply_handler(update: Update, context: CallbackContext):
	if helper_fry(update, context):
		return

	if helper_generate(update, context):
		return

	main_handler(update, context)


@run_async
def main_handler(update: Update, context: CallbackContext):
	textn = update.message.text
	text = textn.lower()
	words = text.split()

	if ', not ' in text:
		drake(
			update,
			textn[text.find(', not ') + 6:],
			textn[:text.find(', not ')]
		)

	elif '🅱️' in text:
		helper_b(update, text)

	elif 'dankbot play despacito' in text or 'alexa play despacito' in text:
		helper_despacito(update, text)

	elif helper_gif(update, text, words):
		return

	elif helper_image(update, text, words):
		return

	elif helper_text(update, text, words):
		return

	else:
		log_message(update)


@run_async
def all_handler(update: Update, context: CallbackContext):
	log_message(update)
	# print(update.message)
	if update.message.chat.id != 623912829:
		return

	update.message.reply_text(
		update.message.animation.file_id if update.message.animation
		else update.message.audio.file_id if update.message.audio
		else update.message.document.file_id if update.message.document
		else update.message.photo[::-1][0].file_id if update.message.photo
		else update.message.video.file_id if update.message.video
		else update.message.video_note.file_id if update.message.video_note
		else update.message.voice.file_id if update.message.voice
		else update.message,
		quote=True
	)
