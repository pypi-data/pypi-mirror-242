import os
from time import sleep
from datetime import datetime, timedelta, date
from collections import UserList
import pickle
import re
import shutil
import os.path
import numexpr
from abc import ABC, abstractmethod
from colorama import init, Fore, Style


class AddressBook(UserList):

    def __init__(self):
        super().__init__()
        self.data = []

    def __str__(self):
        result = []
        for contact in self.data:
            result.append(f"name: {contact['name']}"
                          f"phone: {contact['phone']}"
                          f"birthday: {contact['birthday']}"
                          f"email: {contact['email']}"
                          f"status: {contact['status']}"
                          f"note: {contact['note']}")
        return '\n '.join(result)

    def __setitem__(self, key, value):
        self.data[key] = {'name': value.name,
                          'phone': value.phone,
                          'birthday': value.birthday,
                          'status': value.status,
                          'note': value.note
                          }

    def __getitem__(self, key):
        return self.data[key]

    def add(self, record):
        contact = {'name': record.name,
                   'phone': record.phone,
                   'birthday': record.birthday,
                   'email': record.email,
                   'status': record.status,
                   'note': record.note
                   }
        self.data.append(contact)
        print(Fore.RED + f'  contact {record.name} added')
        log(f'contact {record.name} added')

    def iterator(self, n):
        index = 0
        temp = []
        for record in self.data:
            temp.append(record)
            index += 1
            if index >= n:
                yield temp
                temp.clear()
                index = 0
        if temp:
            yield temp

    def get_page(self, n):
        gen = self.iterator(n)
        for i in range(len(self.data)):
            try:
                result = next(gen)
                for record in result:
                    print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN +
                          '\n  name: ' + Fore.WHITE + f"{record['name']}",
                          Fore.GREEN + '\n  phone: ' + Fore.WHITE + f"{record['phone']}",
                          Fore.GREEN + '\n  birthday: ' + Fore.WHITE + f"{record['birthday']}",
                          Fore.GREEN + '\n  status: ' + Fore.WHITE + f"{record['status']}",
                          Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{record['note']}\n"
                          + Fore.WHITE + ' ' + '*' * 25)
                print(Fore.RED + f'  page {i + 1}')
                input(Fore.YELLOW + '  press enter for next page>')

            except StopIteration:
                break

    def find_info(self, parameter, pattern):
        result = []
        for key in self.data:
            if pattern in key[parameter]:
                result.append(key)

        if result:
            for record in result:
                print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN +
                      '\n  name: ' + Fore.WHITE + f"{record['name']}",
                      Fore.GREEN + '\n  phone: ' + Fore.WHITE + f"{record['phone']}",
                      Fore.GREEN + '\n  birthday: ' + Fore.WHITE + f"{record['birthday']}",
                      Fore.GREEN + '\n  status: ' + Fore.WHITE + f"{record['status']}",
                      Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{record['note']}\n"
                      + Fore.WHITE + ' ' + '*' * 25)

        else:
            print(Fore.RED + '  no matches found for pattern')

    def edit(self, name, parameter, new_value):
        for contact in self.data:
            if contact['name'] == name:
                contact[parameter] = new_value
                print(Fore.RED + f'  contact {name} edited')
                log(f'contact {name} edited')
                break
            else:
                continue

    def __get_current_week(self):
        now = datetime.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=0 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 4)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def congratulate(self):
        result = []
        WEEKDAYS = ['', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        congratulate = {'monday': [], 'tuesday': [], 'wednesday': [], 'thursday': [], 'friday': []}
        for contact in self.data:
            if contact['birthday']:
                birthday = contact['birthday']
                birth_day = datetime.strptime(birthday, '%d.%m.%Y')
                birth_day = date(birth_day.year, birth_day.month, birth_day.day)
                current_date = date.today()
                new_birthday = birth_day.replace(year=current_date.year)
                birthday_weekday = new_birthday.weekday() + 1
                if self.__get_current_week()[0] <= new_birthday < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(contact['name'])
                    else:
                        congratulate['monday'].append(contact['name'])
        for k, v in congratulate.items():
            if len(v):
                result.append(Fore.GREEN + f"{k}:" + Fore.WHITE + f" {', '.join(v)}")

        if not result:
            print(Fore.RED + "  contacts not found")

        return '  ' + '\n  '.join(result)

    def days_to_birthday(self, name):
        for contact in self.data:
            if name == contact['name']:
                birthday = contact['birthday']
                birth_day = datetime.strptime(birthday, '%d.%m.%Y')
                birth_day = date(birth_day.year, birth_day.month, birth_day.day)
                current_date = date.today()
                user_date = birth_day.replace(year=current_date.year)
                delta_days = user_date - current_date
                if delta_days.days >= 0:
                    print(Fore.MAGENTA + f"  {delta_days.days} days left until {name}'s birthday")
                else:
                    user_date = user_date.replace(year=user_date.year + 1)
                    delta_days = user_date - current_date
                    print(Fore.MAGENTA + f"  {delta_days.days} days left until {name}'s birthday")
                break
        else:
            log('contact not found')
            print(Fore.RED + '  contact not found')

    def delete(self, name):
        for key in self.data:
            if key['name'] == name:
                print(Fore.GREEN + '  are you sure for delete contact? (y/n)')
                del_contact = input(Fore.BLUE + '  >>>: ')
                if del_contact == 'y':
                    self.data.remove(key)
                    print(Fore.RED + f'  contact {key["name"]} deleted')
                    log(f'contact {key["name"]} deleted')
                    break
                else:
                    break
        else:
            log('contact not found')
            print(Fore.RED + '  contact not found')

    def clear_book(self):
        self.data.clear()

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)
        log('address_book_vad_1.0.01 saved')

    def load(self, file_name):
        empty_ness = os.stat(file_name)
        if empty_ness.st_size != 0:
            with open(file_name, 'rb') as file:
                self.data = pickle.load(file)
            log('address_book_vad_1.0.01 loaded')
        else:
            print(Fore.RED + '\n  address_book_vad_1.0.01 created')
            log('address_book_vad_1.0.01 created')
        return self.data


class RecordAddressbook:
    def __init__(self, name, phone='', birthday='', email='', status='', note=''):
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email
        self.status = status
        self.note = note


class FieldAddressbook(ABC):
    @abstractmethod
    def __getitem__(self):
        pass


class NameAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  name >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !_-]{1,20}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):
        return self.value


class PhoneAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  phone(+380xxxxxxxxx) >>>: ')
            try:
                if re.match(r'^\+380\d{9}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  number')
                print(Fore.RED + '  incorrect number, try again')

    def __getitem__(self):
        return self.value


class BirthdayAddressbook(FieldAddressbook):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  birthday(dd.mm.YYYY) >>>: ')
            try:
                if re.match(r'^\d{2}.\d{2}.\d{4}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  birthday')
                print(Fore.RED + '  incorrect birthday, try again')

    def __getitem__(self):
        return self.value


class EmailAddressbook(FieldAddressbook):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  email >>>: ')
            try:
                if re.match(r'^(\w|\.|_|-)+@(\w|_|-|\.)+[.]\w{2,3}$', self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  email')
                print(Fore.RED + '  incorrect email, try again')

    def __getitem__(self):
        return self.value


class StatusAddressbook(FieldAddressbook):

    def __init__(self, value=''):
        while True:
            self.status_types = ['', 'family', 'friend', 'work']
            if value:
                self.value = value
            else:
                print(Fore.GREEN + '  status(family, friend, work)')
                self.value = input(Fore.GREEN + '  >>>: ')
            try:
                if self.value in self.status_types:
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'there is no such status')
                print(Fore.RED + '  incorrect status, try again')

    def __getitem__(self):
        return self.value


class NoteAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  note >>>: ')
            try:
                if self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):
        return self.value


class BotAddressbook:
    def __init__(self):
        self.book = AddressBook()

    def handle(self, command):
        try:
            if command == '1':
                while True:
                    print(Fore.GREEN + '  number of note per page')
                    try:
                        n = int(input(Fore.BLUE + '  >>>: '))
                    except Exception:
                        print(Fore.RED + '  incorrect number of note, try again')
                        continue
                    else:
                        if self.book:
                            self.book.get_page(n)
                            break
                        else:
                            print(Fore.RED + '  note_book_vad empty')
                            break

            elif command == '2':
                name = NameAddressbook().value.strip().lower()
                if name:
                    if self.book:
                        for item in self.book:
                            if name == item['name']:
                                print(Fore.RED + '\n  this name already exists\n'
                                                 '  enter command to edit')
                                break
                        else:
                            phone = PhoneAddressbook().value.strip()
                            birth = BirthdayAddressbook().value.strip()
                            email = EmailAddressbook().value.strip()
                            status = StatusAddressbook().value.strip()
                            note = NoteAddressbook().value.strip()
                            record = RecordAddressbook(name, phone, birth, email, status, note)
                            self.book.add(record)
                    else:
                        phone = PhoneAddressbook().value.strip()
                        birth = BirthdayAddressbook().value.strip()
                        email = EmailAddressbook().value.strip()
                        status = StatusAddressbook().value.strip()
                        note = NoteAddressbook().value.strip()
                        record = RecordAddressbook(name, phone, birth, email, status, note)
                        self.book.add(record)
                else:
                    print(Fore.RED + '  please enter a title')

            elif command == '3':
                print(Fore.GREEN + '  parameter to find (name, phone, birthday, status, note)')
                parameter = input(Fore.BLUE + '  >>>: ')
                pattern = input(Fore.GREEN + '  pattern >>>: ').strip().lower()
                if pattern:
                    self.book.find_info(parameter, pattern)
                else:
                    print(Fore.RED + '  please enter a pattern')

            elif command == '4':
                all_records = []
                for key in self.book:
                    all_records.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_records}')
                print(Fore.GREEN + '  enter the name to edit')
                name = input(Fore.BLUE + '  >>>: ')
                print(Fore.GREEN + '  enter the parameter to edit(name, phone, birthday, status, note)')
                parameter = input(Fore.BLUE + '  >>>: ')
                if name in all_records:
                    print(Fore.GREEN + '  enter new value')
                    new_value = input(Fore.BLUE + '  >>>: ')
                    self.book.edit(name, parameter, new_value)
                else:
                    log('record not found')
                    print(Fore.RED + '  record not found')

            elif command == '5':
                print(self.book.congratulate())

            elif command == '6':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_titles}')
                print(Fore.GREEN + '  enter the name for birthday')
                name = input(Fore.BLUE + '  >>>: ')
                if name:
                    self.book.days_to_birthday(name)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '7':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_titles}')
                print(Fore.GREEN + '  enter the name to which you want to delete')
                name = input(Fore.BLUE + '  >>>: ')
                if name:
                    self.book.delete(name)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '8':
                while True:
                    print(Fore.GREEN + '  are you sure for delete all? (y/n)')
                    clear_all = input(Fore.BLUE + '  >>>: ')
                    if clear_all == 'y':
                        self.book.clear_book()
                        print(Fore.RED + '  address_book_vad_1.0.01 cleared')
                        log('address_book_vad_1.0.01 cleared')
                        break
                    else:
                        break

            elif command == '9':
                print(Fore.GREEN + '  save file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.save(file_name)
                    print(Fore.RED + f'  address_book_vad_1.0.01 {file_name} saved')
                else:
                    print(Fore.RED + f'  please enter file name')

            elif command == '10':
                print(Fore.GREEN + '  load file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.load(file_name)
                    print(Fore.RED + f'  address_book_vad_1.0.01 {file_name} loaded')
                else:
                    print(Fore.RED + f'  please enter file name')

        except Exception as e:
            print(f'{e} invalid input, try again')


def log(command):
    current_time = datetime.strftime(datetime.now(), '[%Y-%m-%d] [%H:%M:%S]')
    message = f'{current_time} - {command}'
    with open('logs.txt', 'a') as file:
        file.write(f'{message}\n')


def menu_addressbook():
    print(Fore.RED + f" {' ' * 9}CLI ASSISTANT BOT")
    print(Style.RESET_ALL + ' ************** ADDRESSBOOK **************\n',
          Fore.GREEN + ' 1. show all contacts\n',
          ' 2. add new contact\n',
          ' 3. find contacts by pattern\n',
          ' 4. edit contact\n',
          ' 5. congratulate contacts\n',
          ' 6. days to birthday\n',
          ' 7. delete contact\n',
          ' 8. clear Addressbook\n',
          ' 9. save Addressbook\n',
          ' 10. load Addressbook\n',
          ' 11. exit\n',
          Style.RESET_ALL + '******************************************\n')


def addressbook():
    init()
    file_name = 'save/address_book_save.bin'
    bot = BotAddressbook()
    bot.book.load(file_name)

    while True:
        os.system('cls')
        menu_addressbook()
        user_input = input(Fore.BLUE + '  your choose >>>: ')
        if user_input == '11':
            bot.book.save(file_name)
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            return 'exit'

        bot.handle(user_input)
        input(Fore.YELLOW + '\n  press Enter to continue')

        if user_input in ['2', '4', '7', '8']:
            bot.book.save(file_name)


class NoteBook(UserList):

    def __init__(self):
        super().__init__()
        self.data = []

    def __str__(self):
        result = []
        for contact in self.data:
            result.append(f"title: {contact['title']}"
                          f"note: {contact['note']}"
                          f"tag: {contact['tag']}")
        return '\n '.join(result)

    def __setitem__(self, key, value):
        self.data[key] = {'title': value.title,
                          'note': value.note,
                          'tag': value.tag
                          }

    def __getitem__(self, key):
        return self.data[key]

    def add(self, record):
        contact = {'title': record.title,
                   'note': record.note,
                   'tag': record.tag
                   }
        self.data.append(contact)
        print(Fore.RED + f'  record {record.title} added')
        log(f'record {record.title} added')

    def iterator(self, n):
        index = 0
        temp = []
        for record in self.data:
            temp.append(record)
            index += 1
            if index >= n:
                yield temp
                temp.clear()
                index = 0
        if temp:
            yield temp

    def get_page(self, n):
        gen = self.iterator(n)
        for i in range(len(self.data)):
            try:
                result = next(gen)
                for record in result:
                    print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN +
                          '\n  title: ' + Fore.WHITE + f"{record['title']}",
                          Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{record['note']}",
                          Fore.GREEN + '\n  tag: ' + Fore.WHITE + f"{record['tag']}\n"
                          + Fore.WHITE + ' ' + '*' * 25)

                print(Fore.RED + f'  page {i + 1}')
                input(Fore.YELLOW + '\n  press enter for next page>')

            except StopIteration:
                break

    def add_tag(self, new_tag, title):
        for key in self.data:
            if key['title'] == title:
                if new_tag in key['tag']:
                    print(Fore.RED + f'  tag {new_tag} already exist')
                    break
                key['tag'].append(new_tag)
                print(Fore.RED + f' the new tag {new_tag} saved')
                break

    def find_note_by_word(self, word):
        notes = []
        for key in self.data:
            if word in key['note']:
                notes.append(key)
        if notes:
            for key in notes:
                print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN + '\n  title: ' + Fore.WHITE + f"{key['title']}",
                      Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{key['note']}",
                      Fore.GREEN + '\n  tag: ' + Fore.WHITE + f"{key['tag']}\n" + Fore.WHITE + ' ' + '*' * 25)
        else:
            print(Fore.RED + '  no matches found for the keyword')

    def find_note_by_tag(self, tag):
        tags = []
        for key in self.data:
            if tag in key['tag']:
                tags.append(key)
        if tags:
            for key in tags:
                print(' ' + Fore.WHITE + '*' * 25 + Fore.GREEN + '\n  title: ' + Fore.WHITE + f"{key['title']}",
                      Fore.GREEN + '\n  note: ' + Fore.WHITE + f"{key['note']}",
                      Fore.GREEN + '\n  tag: ' + Fore.WHITE + f"{key['tag']}\n" + Fore.WHITE + ' ' + '*' * 25)
        else:
            print(Fore.RED + '  no matches found for the tags')

    def edit_note(self, title, parameter, new_value):
        for key in self.data:
            if key['title'] == title:
                key[parameter] = new_value
                print(Fore.RED + f'  contact {title} edited')
                log(f'contact {title} edited')
                break
            else:
                continue

    def delete(self, name):
        for key in self.data:
            if key['title'] == name:
                print(Fore.GREEN + '  are you sure for delete note? (y/n)')
                del_contact = input(Fore.BLUE + '  >>>: ')
                if del_contact == 'y':
                    self.data.remove(key)
                    print(Fore.RED + f'  note {key["title"]} deleted')
                    log(f'record {key["title"]} deleted')
                    break
                else:
                    break
        else:
            log('record not found')
            print(Fore.RED + '  record not found')

    def clear_book(self):
        self.data.clear()

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)
        log('note_book_vad saved')

    def load(self, file_name):
        empty_ness = os.stat(file_name)
        if empty_ness.st_size != 0:
            with open(file_name, 'rb') as file:
                self.data = pickle.load(file)
            log('note_book_vad loaded')
        else:
            print(Fore.RED + '\n  note_book_vad created')
            log('note_book_vad created')
        return self.data


class RecordNotebook:
    def __init__(self, title='', note='', tag=None):
        self.title = title
        self.note = note
        self.tag = [tag]


class FieldNotebook(ABC):
    @abstractmethod
    def __getitem__(self):
        pass


class TitleNotebook(FieldNotebook):

    def __init__(self, value=''):

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  title >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !_-]{1,50}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):
        return self.value


class NoteNotebook(FieldNotebook):

    def __init__(self, value=''):

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  note >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !]{1,250}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):
        return self.value


class TagNotebook(FieldNotebook):

    def __init__(self, value=''):

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  tag >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !]{1,20}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):
        return self.value


class BotNotebook:
    def __init__(self):
        self.book = NoteBook()

    def handle(self, command):
        try:
            if command == '1':
                while True:
                    print(Fore.GREEN + '  number of note per page')
                    try:
                        n = int(input(Fore.BLUE + '  >>>: '))
                    except Exception:
                        print(Fore.RED + '  incorrect number of note, try again')
                        continue
                    else:
                        if self.book:
                            self.book.get_page(n)
                            break
                        else:
                            print(Fore.RED + '  note_book_vad empty')
                            break

            elif command == '2':
                title = TitleNotebook().value.strip().lower()
                if title:
                    if self.book:
                        for item in self.book:
                            if title == item['title']:
                                print(Fore.RED + '\n  this title already exists\n'
                                                 '  enter command to edit')
                                break
                        else:
                            note = NoteNotebook().value.strip().lower()
                            tag = TagNotebook().value.strip().lower()
                            record = RecordNotebook(title, note, tag)
                            self.book.add(record)
                    else:
                        note = NoteNotebook().value.strip().lower()
                        tag = TagNotebook().value.strip().lower()
                        record = RecordNotebook(title, note, tag)
                        self.book.add(record)

                else:
                    print(Fore.RED + '  please enter a title')

            elif command == '3':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title')
                title = input(Fore.BLUE + '  >>>: ')
                if title in all_titles:
                    print(Fore.GREEN + '  add new tag')
                    new_tag = input(Fore.BLUE + '  >>>: ')
                    self.book.add_tag(new_tag, title)
                else:
                    log('record not found')
                    print(Fore.RED + '  record not found')

            elif command == '4':
                print(Fore.GREEN + '  enter the word to find note')
                word = input(Fore.BLUE + '  >>>: ')
                self.book.find_note_by_word(word)

            elif command == '5':
                print(Fore.GREEN + '  enter the tag to find note')
                tag = input(Fore.BLUE + '  >>>: ')
                self.book.find_note_by_tag(tag)

            elif command == '6':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title to edit')
                title = input(Fore.BLUE + '  >>>: ')
                print(Fore.GREEN + '  enter the parameter to edit(title, note, tag)')
                parameter = input(Fore.BLUE + '  >>>: ')
                if title in all_titles:
                    print(Fore.GREEN + '  enter new value')
                    new_value = input(Fore.BLUE + '  >>>: ')
                    self.book.edit_note(title, parameter, new_value)
                else:
                    log('record not found')
                    print(Fore.RED + '  record not found')

            elif command == '7':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title to which you want to delete')
                name = input(Fore.BLUE + '  >>>: ')
                if name:
                    self.book.delete(name)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '8':
                while True:
                    print(Fore.GREEN + '  are you sure for delete all? (y/n)')
                    clear_all = input(Fore.BLUE + '  >>>: ')
                    if clear_all == 'y':
                        self.book.clear_book()
                        print(Fore.RED + '  note_book_vad cleared')
                        log('note_book_vad cleared')
                        break
                    else:
                        break

            elif command == '9':
                print(Fore.GREEN + '  save file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.save(file_name)
                    print(Fore.RED + f'  note_book_vad {file_name} saved')
                else:
                    print(Fore.RED + '  please enter file name')

            elif command == '10':
                print(Fore.GREEN + '  load file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.load(file_name)
                    print(Fore.RED + f'  note_book_vad {file_name} loaded')
                else:
                    print(Fore.RED + '  please enter file name')

        except Exception as e:
            print(f'{e} invalid input, try again')


def menu_notebook(*args):
    print(Fore.RED + f" {' ' * 9}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ************** NOTEBOOK **************\n',
          Fore.GREEN + ' 1. show all notes\n',
          ' 2. add new note\n',
          ' 3. add tag for note\n',
          ' 4. find note by word\n',
          ' 5. find note by tag\n',
          ' 6. edit note\n',
          ' 7. delete  note\n',
          ' 8. clear notebook\n',
          ' 9. save notebook\n',
          ' 10. load notebook\n',
          ' 11. exit\n',
          Fore.WHITE + '**************************************\n')


def notebook():
    init()
    file_name = 'save/note_book_save.bin'
    bot = BotNotebook()
    bot.book.load(file_name)

    while True:
        os.system('cls')
        menu_notebook()
        user_input = input(Fore.BLUE + '  your choose >>>: ')

        if user_input == '11':
            bot.book.save(file_name)
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            return 'exit'

        bot.handle(user_input)
        input(Fore.YELLOW + '\n  press Enter to continue')

        if user_input in ['2', '3', '6', '7', '8']:
            bot.book.save(file_name)



def about_calculate():
    print(Fore.RED + f" {' ' * 18}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ******************** DESCRIPTION *******************\n',
          Fore.GREEN + ' to use the calculator in the line, enter the\n',
          ' mathematical operation of the example "5+12/9",and\n',
          ' to get the result of the calculation, press Enter\n',
          Fore.WHITE + '****************************************************\n')


def menu_calculate():
    print(Fore.RED + f" {' ' * 4}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ****** CALCULATOR ******\n',
          Fore.GREEN + ' 1. about\n',
          ' 2. run calculator\n',
          ' 3. exit\n',
          Fore.WHITE + '************************\n')


def calculate():
    init()
    while True:
        os.system('cls')
        menu_calculate()

        user_input = input(Fore.BLUE + '  your choose >>>: ')

        if user_input == '1':
            os.system('cls')
            about_calculate()
            input(Fore.YELLOW + '  press Enter to continue')

        elif user_input == '2':
            os.system('cls')
            print(Fore.RED + f" {' ' * 6}CLI ASSISTANT BOT")
            print(Fore.WHITE + ' ********** CALCULATOR **********')
            print(Fore.GREEN + '  enter a mathematical operation')
            operation = input(Fore.BLUE + '  >>>: ')
            try:
                result = numexpr.evaluate(operation)
                print(Fore.MAGENTA + f"  result: {result}")
                input(Fore.YELLOW + '\n  press Enter to continue')
            except Exception:
                print(Fore.RED + '\n  incorrect operating, try again')
                input(Fore.YELLOW + '\n  press Enter to continue')
                continue

        elif user_input == '3':
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            return 'exit'


def normalize(name):  # заміна кирилиці на латиницю
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ!#$%&()*+,-/:;<>=?@[]^~{|}'\\`. "
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g",
        "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",
        "_",
        "_", "_", "_", "_", "_", "_", "_", "_", "_")
    TRANS = {}
    CYRILLIC = tuple(CYRILLIC_SYMBOLS)

    for c, l in zip(CYRILLIC, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    if re.search(r'\..{2,5}$', name):
        s_res = re.search(r'\..{2,5}$', name)
        suffix = s_res.group()
        name = name.removesuffix(suffix)
        name = name.translate(TRANS)
        name += suffix
    else:
        name = name.translate(TRANS)
    return name


# переміщує відомі файлу у спеціальну теку
def move_file(files_patern, path, el, dst):
    for doc_patern in files_patern:
        if re.search(doc_patern, el):
            new_el = normalize(el)  # змінюю назову файлу
            src = os.path.join(path, el)  # шлях папки, з якої переміщуємо файл
            dst = os.path.join(dst, new_el)  # шлях папки, куде переміщуємо файл
            # пробуємо перемісти файл (переміщуємо з валениям)
            try:
                shutil.copy(src, dst)
                print(Fore.WHITE + "  file is copied successfully", el)
                os.remove(src)
                print(Fore.WHITE + "  file is deleted successfully", el)

            except shutil.SameFileError:
                print(Fore.RED + "  source and destination represents the same file", el)
                os.remove(src)
                print(Fore.RED + "  file is deleted successfully", el)

            except PermissionError:
                print(Fore.RED + "  permission denied", el)

            except Exception:
                print(Fore.RED + "  error occurred while copying file", el)


# переміщує невідомі файлу у спеціальну папку
def move_unknown_file(files_patern, path, el, dst):
    for doc_patern in files_patern:
        if re.search(doc_patern, el) is None:
            new_el = normalize(el)  # змінюю назву файлу
            src = os.path.join(path, el)
            dst = os.path.join(dst, new_el)
            try:
                shutil.copy(src, dst)
                os.remove(src)
                print(Fore.WHITE + "  file is copied successfully")
            except shutil.SameFileError:
                print(Fore.RED + "  source and destination represents the same file")
            except PermissionError:
                print(Fore.RED + "  permission denied")
            except OSError:
                pass


def rec_sort(path):  # сортуємо файл
    # створюємо папки для сортування файлів
    new_folders = ['images',
                   'documents',
                   'audio',
                   'video',
                   'archives',
                   'programs',
                   'unknown']

    for el in new_folders:
        try:
            os.mkdir(path + '\\' + el)
        except FileExistsError:
            print(Fore.RED + f"  file already exists: {el}")
        except OSError:
            print(Fore.RED + f"  error creating folder: {el}")

    dst_doc = os.path.join(path, 'documents')
    dst_img = os.path.join(path, 'images')
    dst_aud = os.path.join(path, 'audio')
    dst_vid = os.path.join(path, 'video')
    dst_arh = os.path.join(path, 'archives')
    dst_prg = os.path.join(path, 'programs')
    dst_un = os.path.join(path, 'unknown')
    el_list = os.listdir(path)

    for folder in new_folders:  # видаляємо стандартні папки з циклу
        for el in el_list:
            if folder == el:
                el_list.remove(el)
    for el in el_list:
        image_files = ['\.jpeg$', '\.png$', '\.jpg$', '\.svg$', '\.tiff$', '\.tif$', '\.bmp$', '\.gif$']
        video_files = ['\.avi$', '\.mp4$', '\.mov$', '\.mkv$', '\.3gp$', '\.3g2$', '\.mpg$', '\.mpeg$']
        doc_files = ['\.doc$', '\.docx$', '\.txt$', '\.pdf$',
                     '\.xls$', '\.xlsx$', '\.pptx$', '\.mpp$', '\.html$', '\.csv$', '\.bin$', '\.rtf$']
        audio_files = ['\.mp3$', '\.ogg$', '\.wav$', '\.amr$', '\.mid$', '\.midi$', '\.mpa$', '\.wma$']
        arch_files = ['\.zip$', '\.gz$', '\.tar$', '\.7z$', '\.rar$']
        program_files = ['\.exe$', '\.bat$', '\.apk$']
        unknown_files = []

        # створив список з відомих розширень файлів
        unknown_files.extend(image_files)
        unknown_files.extend(video_files)
        unknown_files.extend(doc_files)
        unknown_files.extend(audio_files)
        unknown_files.extend(arch_files)
        unknown_files.extend(program_files)

        if not os.path.isdir(path + '\\' + el):  # It is a file
            # move the file
            move_file(image_files, path, el, dst_img)  # переміщуємо картинки
            move_file(video_files, path, el, dst_vid)
            move_file(doc_files, path, el, dst_doc)
            move_file(audio_files, path, el, dst_aud)
            move_file(arch_files, path, el, dst_arh)
            move_file(program_files, path, el, dst_prg)
            move_unknown_file(unknown_files, path, el, dst_un)
        elif os.path.isdir(path + '\\' + el):  # It is a folder
            rec_sort(path + '\\' + el)


def delete_empty_folders(path):  # видаляє порожні папки
    for el in os.listdir(path):  # перебираємо всі елементи в структурі (теки, файли)
        if os.path.isdir(path + '\\' + el):  # якщо елемент є тека
            try:
                os.rmdir(path + '\\' + el)
                print(Fore.WHITE + "  directory '%s' has been removed successfully" % (path + '\\' + el))
                log("directory '%s' has been removed successfully" % (path + '\\' + el))
                delete_empty_folders(path)
            except OSError:
                # print(Fore.RED + "  directory '%s' can not be removed" % (path + '\\' + el))
                log("directory '%s' can not be removed" % (path + '\\' + el))
                delete_empty_folders(path + '\\' + el)


def about_filesort():
    print(Fore.RED + f" {' ' * 18}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ********************* DESCRIPTION ********************\n',
          Fore.GREEN + ' the script helps to sort files in folders according\n',
          ' to popular file types as a result, files will be \n',
          ' moved into folders: <images>, <documents>,\n',
          ' <audio>, <video>, <archives>, <programs>, <unknown>\n',
          ' if the folder does\'t contain files of some file\n',
          ' type then a new folder for this type will not create\n',
          Fore.WHITE + '*******************************************************\n')


def menu_filesort():
    print(Fore.RED + f" {' ' * 4}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ****** FILE SORT ******\n',
          Fore.GREEN + ' 1. about\n',
          ' 2. run file sort\n',
          ' 3. exit\n',
          Fore.WHITE + '************************\n')


def filesort():
    init()
    while True:
        os.system('cls')
        menu_filesort()
        user_input = input(Fore.BLUE + '  your choose >>>: ')

        if user_input == '1':
            os.system('cls')
            about_filesort()
            input(Fore.YELLOW + '  press Enter to continue')

        elif user_input == '2':
            os.system('cls')
            print(Fore.RED + f" {' ' * 7}CLI ASSISTANT BOT")
            print(Fore.WHITE + ' ********** FILE SORT **********')
            print(Fore.GREEN + '  input the file path')
            path = input(Fore.BLUE + '  >>>: ')
            try:
                if os.path.exists(path):
                    rec_sort(path)
                    delete_empty_folders(path)
                    print(Fore.MAGENTA + '\n  sorting completed successfully')
                    input(Fore.YELLOW + '\n  press Enter to continue')
                else:
                    print(Fore.RED + f'\n  path {path} is not found, try again')
                    log(f'path {path} is not found, try again')
                    input(Fore.YELLOW + '\n  press Enter to continue')

            except Exception:
                input(Fore.YELLOW + '\n  press Enter to continue')
                continue

        elif user_input == '3':
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            return 'exit'


def main():
    init()
    while True:
        os.system('cls')
        print(Fore.RED + f" {' ' * 11}CLI ASSISTANT BOT")
        print(Fore.WHITE + ' **************** MENU ****************\n',
              Fore.GREEN + ' 1. address book\n',
              ' 2. note book\n',
              ' 3. file sort\n',
              ' 4. calculator\n',
              ' 5. exit\n',
              Fore.WHITE + '***************************************\n')

        user_input = input(Fore.BLUE + '  your choose >>>: ')

        if user_input == '1':
            result = addressbook()
            if result == 'exit':
                continue

        elif user_input == '2':
            result = notebook()
            if result == 'exit':
                continue

        elif user_input == '3':
            result = filesort()
            if result == 'exit':
                continue

        elif user_input == '4':
            result = calculate()
            if result == 'exit':
                continue

        elif user_input == '5':
            print(Fore.MAGENTA + '\n  good bye')
            sleep(2)
            break


if __name__ == '__main__':
    main()
