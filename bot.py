import pickle
from classes import AddressBook, Record


class Bot:
    ACTIONS = {}

    def __init__(self):
        self.contacts = {}
        self.file = 'contacts.txt'
        self.book = AddressBook()
        try:
            with open(self.file, 'rb') as f:
                contacts_dict = pickle.load(f)
                self.book.data = contacts_dict
        except:
            print('created new adress book')

    # def input_error(self, func = 0):
    #     def wrapper(self, *args, **kwargs):
    #         try:
    #             return func(self, *args, **kwargs)
    #         except (KeyError, ValueError, IndexError) as e:
    #             return str(e)
    #     return wrapper

    # @input_error
    def handle_hello(self, command):
        return "How can I help you?"

    # @input_error
    def handle_add(self, command):
        _, name, phone = command.split()
        if name not in self.book.data:
            record = Record(name)
            self.book.add_record(record)
        else:
            record = self.book.find(name)
        record.add_phone(phone)
        return f"Contact {name} added with phone {phone}"

    # @input_error
    def handle_change(self, command):
        _, name, phone_old, phone_new = command.split()
        if name not in self.book.data:
            raise ValueError(f"Contact {name} not found")
        record = self.book.find(name)
        record.edit_phone(phone_old, phone_new)

    # @input_error
    def handle_phone(self, command):
        _, name = command.split()
        return self.book.find(name)

    def handle_search(self, command):
        _, name = command.split()
        result = set()
        for record in self.book.data.values():
            if name in record.name.value:
                result.add(record)
            for phone in record.phones:
                if name in phone.value:
                    result.add(record)
        return '\n'.join([str(record) for record in result])

    # @input_error
    def handle_show_all(self, command):
        for key, value in self.book.data.items():
            print(value)
        return ''

    # @input_error
    def handle_end(self, command):
        with open(self.file, 'wb') as f:
            pickle.dump(self.contacts, f)
        return 'Good bye!'

    def bad_commands(self, *command):
        return 'Bad command'

    ACTIONS = {
        'hello ': handle_hello,
        'add ': handle_add,
        'change ': handle_change,
        'phone ': handle_phone,
        "show all ": handle_show_all,
        'good night ': handle_end,
        'exit ': handle_end,
        'close ': handle_end,
        'search ': handle_search,
    }

    def get_handler(self, user_input):
        for action in self.ACTIONS:
            if user_input.startswith(action):
                return self.ACTIONS[action]
        return self.bad_commands

    def run(self):
        while True:

            user_input = f"{input('Enter a command: ').lower()} "

            handler = self.get_handler(user_input)
            result = handler(self, user_input)
            with open(self.file, 'wb') as f:
                pickle.dump(self.book, f)
            print(result)
            if result == 'Good bye!':
                break


