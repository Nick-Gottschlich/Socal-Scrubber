import os
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import messagebox

from services import reddit, twitter

USER_HOME_PATH = os.path.expanduser('~')


def create_storage_folder():
    storage_folder_path = os.path.join(USER_HOME_PATH, '.SocialAmnesia')
    reddit_storage_folder_path = os.path.join(storage_folder_path, "reddit")

    if not os.path.exists(storage_folder_path):
        os.makedirs(storage_folder_path)
        os.makedirs(reddit_storage_folder_path)


def build_number_list(max_number):
    """
    Builds a list of numbers from 0 up to `max_number`.
    :param max_number: how many numbers to return
    :return: list
    """
    return [str(i) for i in range(max_number)]


def create_dropdown(master: tk.Frame, width: int, value_quantity: int,
                    element_state: str = 'readonly', current: int = 0):
    """
    Creates a set up dropdown
    :param master: parent element
    :param width: width of the element
    :param value_quantity: how many number to create in the dropdown list
    :param element_state: preferably set to 'readonly'
    :param current: current chosen value
    :return: Dropdown element
    """
    dropdown = ttk.Combobox(master, width=width)
    dropdown['values'] = build_number_list(value_quantity)
    dropdown['state'] = element_state
    dropdown.current(current)
    return dropdown


class MainApp(tk.Frame):
    def __init__(self, master: tk.Tk, **kw):
        self.master = master
        super().__init__(self.master, **kw)
        self.configure_gui()

        self.tabs = ttk.Notebook(self.master)
        self.login_frame = self.build_login_tab()
        self.reddit_frame = self.build_reddit_tab()
        self.twitter_frame = self.build_twitter_tab()
        self.create_tabs()

    def configure_gui(self):
        self.master.title('Social Amnesia')
        self.master.protocol('WM_DELETE_WINDOW', self.master.withdraw)
        self.master.createcommand('tk::mac::ReopenApplication', self.master.deiconify)
        self.master.report_callback_exception = self.handle_callback_error

    def create_tabs(self):
        self.tabs.add(self.login_frame, text='Login to accounts')
        self.tabs.add(self.reddit_frame, text='Reddit')
        self.tabs.add(self.twitter_frame, text='Twitter')
        self.tabs.pack(expand=1, fill='both')

    def handle_callback_error(*args):
        """
        Informs the user of errors in a friendly manner
        :param args: list of errors
        :return: None
        """
        received_error = str(args[1])
        errors = {
            # reddit error, happens if you try to run `reddit.user.me()` and login fails
            'received 401 HTTP response': 'Failed to login to reddit!',
            "'user'": 'You are not logged into reddit!',
            "[{'code': 215, 'message': 'Bad Authentication data.'}]": 'Failed to login to twitter!',
            'list index out of range': 'No tweets or favorites found!',
            "'api'": 'You are not logged in to twitter!'
        }
        messagebox.showerror('Error', errors.get(received_error, received_error))

    def build_login_tab(self):
        """
        Builds the tab that lets the user log into their social media accounts
        :return: Login frame
        """
        frame = tk.Frame(self.tabs)
        frame.grid()
        self.build_reddit_frame(frame)
        self.build_twitter_frame(frame)
        return frame

    @staticmethod
    def build_twitter_frame(frame: tk.Frame):
        """
        Create and place elements in the twitter frame
        :param frame: frame to set up
        :return: set up Twitter frame
        """
        # Create elements
        title = tk.Label(frame, text='Twitter')
        title.config(font=('arial', 25))
        consumer_key_label = tk.Label(frame, text='Enter twitter consumer Key:')
        consumer_key_entry = tk.Entry(frame)
        consumer_secret_label = tk.Label(frame, text='Enter twitter consumer secret:')
        consumer_secret_entry = tk.Entry(frame)
        access_token_label = tk.Label(frame, text='Enter twitter Access Token:')
        access_token_entry = tk.Entry(frame)
        access_token_secret_label = tk.Label(frame, text='Enter Twitter access token secret:')
        access_token_secret_entry = tk.Entry(frame)
        login_confirm_text = tk.StringVar()
        login_confirm_text.set('Waiting for login')
        login_confirmed_label = tk.Label(frame, textvariable=login_confirm_text)
        login_button = tk.Button(
            frame, text='Login to Twitter',
            command=lambda: twitter.setTwitterLogin(
                consumer_key_entry.get(),
                consumer_secret_entry.get(),
                access_token_entry.get(),
                access_token_secret_entry.get(),
                login_confirm_text)
        )

        # Place elements
        title.grid(row=0, column=2, columnspan=2)
        consumer_key_label.grid(row=1, column=2)
        consumer_key_entry.grid(row=1, column=3)
        consumer_secret_label.grid(row=2, column=2)
        consumer_secret_entry.grid(row=2, column=3)
        access_token_label.grid(row=3, column=2)
        access_token_entry.grid(row=3, column=3)
        access_token_secret_label.grid(row=4, column=2)
        access_token_secret_entry.grid(row=4, column=3)
        login_button.grid(row=5, column=2)
        login_confirmed_label.grid(row=5, column=3)

    @staticmethod
    def build_reddit_frame(frame: tk.Frame):
        """
        Create and place elements in the frame
        :param frame: frame to set up
        :return: None
        """
        # Create elements
        title = tk.Label(frame, text='reddit')
        title.config(font=('arial', 25))
        username_label = tk.Label(frame, text='Enter reddit username:')
        username_entry = tk.Entry(frame)
        password_label = tk.Label(frame, text='Enter reddit password:')
        password_entry = tk.Entry(frame)
        client_id_label = tk.Label(frame, text='Enter reddit client ID:')
        client_id_entry = tk.Entry(frame)
        client_secret_label = tk.Label(frame, text='Enter reddit client secret:')
        client_secret_entry = tk.Entry(frame)
        login_confirm_text = tk.StringVar()
        login_confirm_text.set('Waiting for Login')
        login_confirmed_label = tk.Label(frame, textvariable=login_confirm_text)
        login_button = tk.Button(
            frame, text='Login to reddit',
            command=lambda: reddit.set_login(
                username_entry.get(),
                password_entry.get(),
                client_id_entry.get(),
                client_secret_entry.get(),
                login_confirm_text,
                False)
        )

        # Place elements
        title.grid(row=0, column=0, columnspan=2)
        username_label.grid(row=1, column=0)
        username_entry.grid(row=1, column=1)
        password_label.grid(row=2, column=0)
        password_entry.grid(row=2, column=1)
        client_id_label.grid(row=3, column=0)
        client_id_entry.grid(row=3, column=1)
        client_secret_label.grid(row=4, column=0)
        client_secret_entry.grid(row=4, column=1)
        login_button.grid(row=5, column=0)
        login_confirmed_label.grid(row=5, column=1)

        # If a praw.ini file exists, log in to reddit
        praw_config_file = Path(os.path.join(USER_HOME_PATH, '.config/praw.ini'))
        if praw_config_file.is_file():
            reddit.set_login('', '', '', '', login_confirm_text, True)

    def build_reddit_tab(self):
        """
        Build the tab that will handle Reddit configuration and actions
        :return: Set up Reddit frame
        """
        frame = tk.Frame(self.tabs)
        frame.grid()

        # Configuration section title
        configuration_label = tk.Label(frame, text='Configuration')
        configuration_label.config(font=('arial', 25))

        # Configuration to set total time of items to save
        current_time_to_save = tk.StringVar()
        current_time_to_save.set('Currently set to save: [nothing]')
        time_keep_label = tk.Label(frame, text='Keep comments/submissions younger than: ')

        # TODO: Fix hours
        hours_dropdown = create_dropdown(frame, 2, 24)
        days_dropdown = create_dropdown(frame, 2, 7)
        weeks_dropdown = create_dropdown(frame, 2, 52)
        years_dropdown = create_dropdown(frame, 2, 15)

        hours_label = tk.Label(frame, text='hours')
        days_label = tk.Label(frame, text='days')
        weeks_label = tk.Label(frame, text='weeks')
        years_label = tk.Label(frame, text='years')

        time_currently_set_label = tk.Label(frame, textvariable=current_time_to_save)
        set_time_button = tk.Button(
            frame, text='Set Total Time To Keep',
            command=lambda: reddit.set_reddit_time_to_save(
                hours_dropdown.get(), days_dropdown.get(),
                weeks_dropdown.get(), years_dropdown.get(),
                current_time_to_save)
        )

        # Configuration to set saving items with a certain amount of upvotes
        current_max_score = tk.StringVar()
        current_max_score.set('Currently set to: 0 upvotes')

        max_score_label = tk.Label(frame, text='Delete comments/submissions less than score:')
        max_score_entry_field = tk.Entry(frame, width=5)
        max_score_currently_set_label = tk.Label(frame, textvariable=current_max_score)

        set_max_score_button = tk.Button(
            frame, text='Set Max Score',
            command=lambda: reddit.set_reddix_max_score(max_score_entry_field.get(), current_max_score)
        )
        set_max_score_unlimited_button = tk.Button(
            frame, text='Set Unlimited',
            command=lambda: reddit.set_reddix_max_score('Unlimited', current_max_score)
        )

        # Configuration to let user skip over gilded comments
        gilded_skip_bool = tk.IntVar()
        # Skip gilded posts by default
        gilded_skip_bool.set(1)
        gilded_skip_label = tk.Label(frame, text='Skip Gilded comments:')
        gilded_skip_check_button = tk.Checkbutton(
            frame, variable=gilded_skip_bool,
            command=lambda: reddit.set_reddit_gilded_skip(gilded_skip_bool))

        # Allows the user to actually delete comments or submissions
        deletion_section_label = tk.Label(frame, text='Deletion')
        deletion_section_label.config(font=('arial', 25))

        currently_deleting_text = tk.StringVar()
        currently_deleting_text.set('')
        deletion_progress_label = tk.Label(frame, textvariable=currently_deleting_text)

        deletion_progress_bar = ttk.Progressbar(
            frame, orient='horizontal',
            length=100, mode='determinate')

        num_deleted_items_text = tk.StringVar()
        num_deleted_items_text.set('')
        num_deleted_items_label = tk.Label(frame, textvariable=num_deleted_items_text)

        delete_comments_button = tk.Button(
            frame, text='Delete comments',
            command=lambda: reddit.delete_reddit_items(
                root, True, currently_deleting_text,
                deletion_progress_bar, num_deleted_items_text)
        )

        delete_submissions_button = tk.Button(
            frame, text='Delete submissions',
            command=lambda: reddit.delete_reddit_items(
                root, False, currently_deleting_text,
                deletion_progress_bar, num_deleted_items_text)
        )

        test_run_bool = tk.IntVar()
        test_run_bool.set(1)
        test_run_text = 'TestRun - Checking this will show you what would be deleted, without deleting anything'
        test_run_check_button = tk.Checkbutton(
            frame, text=test_run_text,
            variable=test_run_bool,
            command=lambda: reddit.set_reddit_test_run(test_run_bool))

        # Allows the user to schedule runs
        scheduler_section_label = tk.Label(frame, text='Scheduler')
        scheduler_section_label.config(font=('arial', 25))

        scheduler_bool = tk.IntVar()
        scheduler_text = 'Select to delete reddit comments + submissions daily at'

        hours_dropdown = create_dropdown(frame, 2, 24)

        scheduler_check_button = tk.Checkbutton(
            frame, text=scheduler_text,
            variable=scheduler_bool,
            command=lambda: reddit.set_reddit_scheduler(
                root, scheduler_bool,
                int(hours_dropdown.get()),
                tk.StringVar(), ttk.Progressbar()))

        # This part actually builds the reddit tab
        configuration_label.grid(row=0, columnspan=11, sticky=(tk.N, tk.S), pady=5)
        time_keep_label.grid(row=1, column=0)
        hours_dropdown.grid(row=1, column=1, sticky=(tk.W,))
        hours_label.grid(row=1, column=2, sticky=(tk.W,))
        days_dropdown.grid(row=1, column=3, sticky=(tk.W,))
        days_label.grid(row=1, column=4, sticky=(tk.W,))
        weeks_dropdown.grid(row=1, column=5, sticky=(tk.W,))
        weeks_label.grid(row=1, column=6, sticky=(tk.W,))
        years_dropdown.grid(row=1, column=7, sticky=(tk.W,))
        years_label.grid(row=1, column=8, sticky=(tk.W,))
        set_time_button.grid(row=1, column=9, columnspan=2)
        time_currently_set_label.grid(row=1, column=11)

        max_score_label.grid(row=2, column=0)
        max_score_entry_field.grid(row=2, column=1, columnspan=8, sticky=(tk.W,))
        set_max_score_button.grid(row=2, column=9)
        set_max_score_unlimited_button.grid(row=2, column=10)
        max_score_currently_set_label.grid(row=2, column=11)

        gilded_skip_label.grid(row=3, column=0)
        gilded_skip_check_button.grid(row=3, column=1)

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=4, columnspan=13, sticky=(tk.E, tk.W), pady=5)

        deletion_section_label.grid(row=5, columnspan=11, sticky=(tk.N, tk.S), pady=5)

        delete_comments_button.grid(row=6, column=0, sticky=tk.W)
        delete_submissions_button.grid(row=6, column=0, sticky=(tk.E,))
        test_run_check_button.grid(row=6, column=1, columnspan=11)

        deletion_progress_label.grid(row=7, column=0)
        deletion_progress_bar.grid(row=8, column=0, sticky=(tk.W,))
        num_deleted_items_label.grid(row=8, column=0, sticky=(tk.E,))

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=9, columnspan=13, sticky=(tk.E, tk.W), pady=5)

        scheduler_section_label.grid(row=10, columnspan=11, sticky=(tk.N, tk.S), pady=5)
        scheduler_check_button.grid(row=11, column=0)
        hours_dropdown.grid(row=11, column=1)

        return frame

    def build_twitter_tab(self):
        """
        Builds tab that handles twitter config and actions
        :return: A set up Twitter tab
        """
        frame = tk.Frame(self.tabs)
        frame.grid()

        # Configuration section title
        configuration_label = tk.Label(frame, text='Configuration')
        configuration_label.config(font=('arial', 25))

        # Configuration to set total time of items to save
        current_time_to_save = tk.StringVar()
        current_time_to_save.set('Currently set to save: [nothing]')
        time_keep_label = tk.Label(frame, text='Keep items younger than: ')

        hours_dropdown = create_dropdown(frame, 2, 24)
        days_dropdown = create_dropdown(frame, 2, 7)
        weeks_dropdown = create_dropdown(frame, 2, 52)
        years_dropdown = create_dropdown(frame, 2, 15)

        hours_label = tk.Label(frame, text='hours')
        days_label = tk.Label(frame, text='days')
        weeks_label = tk.Label(frame, text='weeks')
        years_label = tk.Label(frame, text='years')

        time_currently_set_label = tk.Label(frame, textvariable=current_time_to_save)
        set_time_button = tk.Button(
            frame, text='Set Total Time To Keep',
            command=lambda: twitter.setTwitterTimeToSave(
                hours_dropdown.get(), days_dropdown.get(),
                weeks_dropdown.get(), years_dropdown.get(), current_time_to_save)
        )

        # Configuration to set saving items with a certain amount of favorites
        current_max_favorites = tk.StringVar()
        current_max_favorites.set('Currently set to: 0 Favorites')
        max_favorites_label = tk.Label(frame, text='Delete tweets that have fewer favorites than:')
        max_favorites_entry_field = tk.Entry(frame, width=5)
        max_favorites_currently_set_label = tk.Label(frame, textvariable=current_max_favorites)
        set_max_favorites_button = tk.Button(
            frame, text='Set Max Favorites',
            command=lambda: twitter.setTwitterMaxFavorites(
                max_favorites_entry_field.get(), current_max_favorites)
        )
        set_max_favorites_unlimited_button = tk.Button(
            frame, text='Set Unlimited',
            command=lambda: twitter.setTwitterMaxFavorites('Unlimited', current_max_favorites)
        )

        # Configuration to set saving items with a certain amount of retweets
        current_max_retweets = tk.StringVar()
        current_max_retweets.set('Currently set to: 0 Retweets')
        max_retweets_label = tk.Label(frame, text='Delete tweets that have fewer retweets than: ')
        max_retweets_entry_field = tk.Entry(frame, width=5)
        max_retweets_currently_set_label = tk.Label(frame, textvariable=current_max_retweets)
        set_max_retweets_button = tk.Button(
            frame, text='Set Max Retweets',
            command=lambda: twitter.setTwitterMaxRetweets(
                max_retweets_entry_field.get(), current_max_retweets)
        )
        set_max_retweets_unlimited_button = tk.Button(
            frame, text='Set Unlimited',
            command=lambda: twitter.setTwitterMaxRetweets(
                'Unlimited', current_max_retweets)
        )

        # Allows the user to delete tweets or remove favorites
        deletion_section_label = tk.Label(frame, text='Deletion')
        deletion_section_label.config(font=('arial', 25))

        currently_deleting_text = tk.StringVar()
        currently_deleting_text.set('')

        deletion_progress_label = tk.Label(frame, textvariable=currently_deleting_text)
        deletion_progress_bar = ttk.Progressbar(frame, orient='horizontal',
                                                length=100, mode='determinate')

        num_deleted_items_text = tk.StringVar()
        num_deleted_items_text.set('')
        num_deleted_items_label = tk.Label(frame, textvariable=num_deleted_items_text)

        delete_comments_button = tk.Button(
            frame, text='Delete tweets',
            command=lambda: twitter.deleteTwitterTweets(
                root, currently_deleting_text, deletion_progress_bar, num_deleted_items_text)
        )

        delete_submissions_button = tk.Button(
            frame, text='Remove Favorites',
            command=lambda: twitter.delete_twitter_favorites(
                root, currently_deleting_text, deletion_progress_bar, num_deleted_items_text)
        )

        test_run_bool = tk.IntVar()
        test_run_bool.set(1)
        test_run_text = 'TestRun - Checking this will show you what would ' \
                        'be deleted, without actually deleting anything'
        test_run_check_button = tk.Checkbutton(
            frame, text=test_run_text,
            variable=test_run_bool,
            command=lambda: twitter.setTwitterTestRun(test_run_bool))

        # Allows the user to schedule runs
        scheduler_section_label = tk.Label(frame, text='Scheduler')
        scheduler_section_label.config(font=('arial', 25))

        scheduler_bool = tk.IntVar()
        scheduler_text = 'Select to delete twitter comments + submissions daily at'

        hours_dropdown = create_dropdown(frame, 2, 24)

        scheduler_check_button = tk.Checkbutton(
            frame, text=scheduler_text,
            variable=scheduler_bool,
            command=lambda: twitter.setTwitterScheduler(
                root, scheduler_bool, int(hours_dropdown.get()),
                tk.StringVar(), ttk.Progressbar()))

        # Actually build the twitter tab
        configuration_label.grid(row=0, columnspan=11, sticky=(tk.N, tk.S), pady=5)
        time_keep_label.grid(row=1, column=0)
        hours_dropdown.grid(row=1, column=1, sticky=(tk.W,))
        hours_label.grid(row=1, column=2, sticky=(tk.W,))
        days_dropdown.grid(row=1, column=3, sticky=(tk.W,))
        days_label.grid(row=1, column=4, sticky=(tk.W,))
        weeks_dropdown.grid(row=1, column=5, sticky=(tk.W,))
        weeks_label.grid(row=1, column=6, sticky=(tk.W,))
        years_dropdown.grid(row=1, column=7, sticky=(tk.W,))
        years_label.grid(row=1, column=8, sticky=(tk.W,))
        set_time_button.grid(row=1, column=9, columnspan=2)
        time_currently_set_label.grid(row=1, column=11)

        max_favorites_label.grid(row=2, column=0)
        max_favorites_entry_field.grid(row=2, column=1, columnspan=8, sticky=(tk.W,))
        set_max_favorites_button.grid(row=2, column=9)
        set_max_favorites_unlimited_button.grid(row=2, column=10)
        max_favorites_currently_set_label.grid(row=2, column=11)

        max_retweets_label.grid(row=3, column=0)
        max_retweets_entry_field.grid(row=3, column=1, columnspan=8, sticky=(tk.W,))
        set_max_retweets_button.grid(row=3, column=9)
        set_max_retweets_unlimited_button.grid(row=3, column=10)
        max_retweets_currently_set_label.grid(row=3, column=11)

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=4, columnspan=13, sticky=(tk.E, tk.W), pady=5)

        deletion_section_label.grid(row=5, columnspan=11, sticky=(tk.N, tk.S), pady=5)

        delete_comments_button.grid(row=6, column=0, sticky=(tk.W,))
        delete_submissions_button.grid(row=6, column=0, sticky=(tk.E,))
        test_run_check_button.grid(row=6, column=1, columnspan=11)

        deletion_progress_label.grid(row=7, column=0)
        deletion_progress_bar.grid(row=8, column=0, sticky=(tk.W,))
        num_deleted_items_label.grid(row=8, column=0, sticky=(tk.E,))

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=9, columnspan=13, sticky=(tk.E, tk.W), pady=5)

        scheduler_section_label.grid(row=10, columnspan=11, sticky=(tk.N, tk.S), pady=5)
        scheduler_check_button.grid(row=11, column=0)
        hours_dropdown.grid(row=11, column=1)

        return frame


if __name__ == '__main__':
    create_storage_folder()

    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
