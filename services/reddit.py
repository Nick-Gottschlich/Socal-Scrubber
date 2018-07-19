import os
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

import arrow
import praw

USER_AGENT = 'Social Amnesia: v0.2.0 (by /u/JavaOffScript)'
EDIT_OVERWRITE = 'Wiped by Social Amnesia'

praw_config_file_path = Path(f'{os.path.expanduser("~")}/.config/praw.ini')

# The reddit state object
# Handles the actual praw object that manipulates the reddit account
# as well as any configuration options about how to act.
reddit_state = {}


# Logs into reddit using PRAW, gives user an error on failure
def set_login(username, password, client_id, client_secret, login_confirm_text, init):
    if init:
        try:
            reddit = praw.Reddit('user', user_agent=USER_AGENT)
            reddit.user.me()
        except:
            # praw.ini is broken, delete it
            os.remove(praw_config_file_path)
            return
    else:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=USER_AGENT,
            username=username,
            password=password
        )

        if praw_config_file_path.is_file():
            os.remove(praw_config_file_path)

        praw_config_string = f'''[user]
client_id={client_id}
client_secret={client_secret}
password={password}
username={username}'''

        with open(praw_config_file_path, 'a') as out:
            out.write(praw_config_string)

    reddit_username = str(reddit.user.me())

    login_confirm_text.set(f'Logged in to Reddit as {reddit_username}')

    # initialize state
    reddit_state['user'] = reddit.redditor(reddit_username)
    reddit_state['timeToSave'] = arrow.now().replace(hours=0)
    reddit_state['maxScore'] = 0
    reddit_state['testRun'] = 0
    reddit_state['gildedSkip'] = 0


def set_reddit_time_to_save(hours_to_save, days_to_save, weeks_to_save, years_to_save, current_time_to_save):
    """
    Sets the time of comments or submissions to save, stores it in redditState
    and updates the UI to show what its currently set to.
    :param hours_to_save: input received from the UI
    :param days_to_save: input received from the UI
    :param weeks_to_save: input received from the UI
    :param years_to_save: input received from the UI
    :param current_time_to_save: input received from the UI
    :return: None
    """
    total_hours = int(hours_to_save) + (int(days_to_save) * 24) + \
                  (int(weeks_to_save) * 168) + (int(years_to_save) * 8736)

    reddit_state['timeToSave'] = arrow.now().replace(
        hours=-total_hours)

    def get_text(time, text):
        return '' if time == '0' else time + text

    hours_text = get_text(hours_to_save, 'hours')
    days_text = get_text(days_to_save, 'days')
    weeks_text = get_text(weeks_to_save, 'weeks')
    years_text = get_text(years_to_save, 'years')

    if hours_to_save == '0' and days_to_save == '0' and weeks_to_save == '0' and years_to_save == '0':
        current_time_to_save.set(f'Currently set to save: [nothing]')
    else:
        current_time_to_save.set(
            f'Currently set to save: [{years_text} {weeks_text} {days_text} {hours_text}] of items')


def set_reddix_max_score(max_score, current_max_score):
    """
    Sets the maximum score level, any posts above this store will be skipped over
    updates the UI to show what its currently set to.
    :param max_score: the input received from the UI
    :param current_max_score: what is stored for the user in the UI
    :return:
    """
    if max_score == '':
        max_score = 0
    elif max_score == 'Unlimited':
        reddit_state['maxScore'] = 9999999999
    else:
        max_score = int(max_score)
        reddit_state['maxScore'] = max_score

    current_max_score.set(f'Currently set to: {str(max_score)} upvotes')


# Set whether to skip gilded comments or not (stored in redditState)
#   gildedSkipBool - 0 to delete gilded comments, 1 to skip gilded comments
def set_reddit_gilded_skip(gilded_skip_bool):
    skip_gild = gilded_skip_bool.get()
    if skip_gild:
        reddit_state['gildedSkip'] = skip_gild


def delete_reddit_items(root, comment_bool, currently_deleting_text, deletion_progress_bar, num_deleted_items_text):
    """
    Deletes the items according to user configurations.
    :param root: the reference to the actual tkinter GUI window
    :param comment_bool: true if deleting comments, false if deleting submissions
    :param currently_deleting_text: Describes the item that is currently being deleted.
    :param deletion_progress_bar: updates as the items are looped through
    :param num_deleted_items_text: updates as X out of Y comments are looped through
    :return:
    """
    if comment_bool:
        total_items = sum(1 for _ in reddit_state['user'].comments.new(limit=None))
        item_array = reddit_state['user'].comments.new(limit=None)
    else:
        total_items = sum(1 for _ in reddit_state['user'].submissions.new(limit=None))
        item_array = reddit_state['user'].submissions.new(limit=None)

    num_deleted_items_text.set(f'0/{str(total_items)} items processed so far')

    count = 1
    for item in item_array:
        if comment_bool:
            item_string = 'Comment'
            item_snippet = item.body[0:15]
            if len(item.body) > 15:
                item_snippet = item_snippet + '...'
            for char in item_snippet:
                # tkinter can't handle certain unicode characters,
                # so we strip them
                if ord(char) > 65535:
                    item_snippet = item_snippet.replace(char, '')
        else:
            item_string = 'Submission'
            item_snippet = item.title[0:50]
            if len(item.title) > 50:
                item_snippet = item_snippet + '...'
            for char in item_snippet:
                # tkinter can't handle certain unicode characters,
                # so we strip them
                if ord(char) > 65535:
                    item_snippet = item_snippet.replace(char, '')

        time_created = arrow.get(item.created_utc)

        if time_created > reddit_state['timeToSave']:
            currently_deleting_text.set(
                f'{item_string} `{item_snippet}` more recent than cutoff, skipping.')
        elif item.score > reddit_state['maxScore']:
            currently_deleting_text.set(
                f'{item_string} `{item_snippet}` is higher than max score, skipping.')
        elif item.gilded and reddit_state['gildedSkip']:
            currently_deleting_text.set(
                f'{item_string} `{item_snippet}` is gilded, skipping.')
        else:
            if reddit_state['testRun'] == 0:
                # Need the try/except here as it will crash on
                #  link submissions otherwise
                try:
                    item.edit(EDIT_OVERWRITE)
                except:
                    pass

                item.delete()

                currently_deleting_text.set(
                    f'Deleting {item_string} `{item_snippet}`')
            else:
                currently_deleting_text.set(
                    f'TEST RUN: Would delete {item_string} `{item_snippet}`')

        num_deleted_items_text.set(
            f'{str(count)}/{str(total_items)} items processed.')
        deletion_progress_bar['value'] = round(
            (count / total_items) * 100, 1)

        root.update()
        count += 1


# Set whether to run a test run or not (stored in redditState)
# testRunBool - 0 for real run, 1 for test run
def set_reddit_test_run(test_run_bool):
    reddit_state['testRun'] = test_run_bool.get()


# neccesary global bool for the scheduler
alreadyRanBool = False


# reddit scheduler
#   root: tkinkter window
#   schedulerBool: true if set to run, false otherwise
#   hourOfDay: int 0-23, sets hour of day to run on
#   stringVar, progressVar - empty Vars needed to run the deleteRedditItems function
def set_reddit_scheduler(root, scheduler_bool, hour_of_day, string_var, progress_var):
    global alreadyRanBool
    if not scheduler_bool.get():
        alreadyRanBool = False
        return

    current_time = datetime.now().time().hour

    if current_time == hour_of_day and not alreadyRanBool:
        messagebox.showinfo('Scheduler', 'Social Amnesia is now erasing your past on reddit.')

        delete_reddit_items(root, True, string_var, progress_var, string_var)
        delete_reddit_items(root, False, string_var, progress_var, string_var)

        alreadyRanBool = True
    if current_time < 23 and current_time == hour_of_day + 1:
        alreadyRanBool = False
    elif current_time == 0:
        alreadyRanBool = False

    root.after(1000, lambda: set_reddit_scheduler(
        root, scheduler_bool, hour_of_day, string_var, progress_var))
