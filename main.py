from datetime import datetime
import calendar
from prompt_toolkit.validation import Validator
from prompt_toolkit import prompt


class ComputeNextBirthDay:
    # let us isolate the function to convert a text string to a date in a dedicated function
    #
    # let us get flexible and allow for different ways to express the birthday
    # this list of 'pattens' allows for the following notation formats
    #
    # - YYYY-MM-DD (example: 2023-11-16)
    # - DD.MM.YYYY (example: 16.11.2023)
    # - DD/MM/YYYY (example: 16/11/2023)
    # - DD-MM-YYYY (example: 16-11-2023)
    # ... and off
    @staticmethod
    def parse_text_to_date(text: str) -> datetime.date:
        date_formats = ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y')
        # we simply try if the conversion succeeds; if it does not and any error occurs
        # then this method returns False
        for fmt in date_formats:
            try:
                return_date = datetime.strptime(text, fmt)
                return return_date
            except ValueError:
                pass
        return None

    # is_date : function that validates if the provided text value complies to the date format we expect
    #
    # We need this as the user input for birthdate is text, and we want to compute with the value new
    # dates; this is why we need to be sure we can convert the value input by the user to a date
    # we have to
    def is_date(self, text: str) -> bool:
        # we simply try if the conversion succeeds; if it does not
        # then this method returns False
        parsed_date = self.parse_text_to_date(text)
        if not parsed_date:
            return False
        return True

    # is_birthday_still_this_year : function that checks if your birthday wil still be this year or not
    #
    # We need this as we need to compute when the next upcoming birthday will be; will it be this or next year
    @staticmethod
    def is_birthday_still_this_year(birthday: datetime) -> bool:
        # let us just see if the birthday (set to the same year as current year) comes 'after' the
        # today in the same year
        today = datetime.now()
        return birthday > today

    # get_next_birthday : function that retrieves the birthday given by the user and computes when the next
    # birthday will be
    def compute_next_birthday(self, text: str) -> datetime:
        birthday = self.parse_text_to_date(text)
        # decide if the year of the birthday needs to be set to this or next year
        if self.is_birthday_still_this_year(birthday.replace(year=datetime.now().year)):
            new_birthday = birthday.replace(year=datetime.now().year)
        else:
            new_birthday = birthday.replace(year=datetime.now().year + 1)
        return new_birthday

    def get_validator(self) -> Validator:
        return Validator.from_callable(
            self.is_date,
            error_message='Invalid birthdate. please fill in a valid birthdate',
            move_cursor_to_end=True
        )

    @staticmethod
    def compute_age(birthday: datetime) -> int:
        today = datetime.now()
        delta = today - birthday
        return delta.days // 365

    @staticmethod
    def compute_days_to_wait(next_birthday: datetime) -> int:
        today = datetime.now()
        delta = next_birthday - today
        return delta.days

    def compute_birthday(self) -> None:
        # we need to make sure the user puts in a correct date. This validator from prompt toolkit
        # module allows us to bind the validation of the date (@see function is_date) to the users prompt input
        date_validator = self.get_validator()

        # Let us ask for the users name
        # For name we use no validation. If we want we can bind a validation just as is with the birthday
        name = prompt('What is your name?\n')

        # let us ask for the birthday and make sure the user types in a correct date
        # birthday prompt assigns the validator binding (@see date_validator)
        birth_date = prompt('What is your birthdate?\n', validator=date_validator, validate_while_typing=False)

        # we get the next upcoming birthday
        next_birthday: datetime = self.compute_next_birthday(birth_date)

        birth_date_date_type: datetime = self.parse_text_to_date(birth_date)
        weekday_of_birth = birth_date_date_type.strftime("%A")

        # we print a nice message showing when the next birthday may be expected
        print("")
        print("")
        print("Hi {0}!".format(name))
        print("Thank you for your information!")
        print("You where born on {0}, {1} the {2}th in {3}!".format(
            weekday_of_birth,
            calendar.month_name[birth_date_date_type.month],
            birth_date_date_type.day,
            birth_date_date_type.year)
        )
        print("You are {0} years old!".format(
            self.compute_age(birth_date_date_type))
        )
        print("And your next birthday wil be on {0}, {1} the {2}th in {3}!".format(
            next_birthday.strftime("%A"),
            calendar.month_name[next_birthday.month],
            next_birthday.day,
            next_birthday.year))
        print("Just {0} days to wait .... ".format(self.compute_days_to_wait(next_birthday)))
        raise SystemExit("Finished...")


if __name__ == '__main__':
    print('Starting next birthday calculator ....')
    compute = ComputeNextBirthDay()
    compute.compute_birthday()
