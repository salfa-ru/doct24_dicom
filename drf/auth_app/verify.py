from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException

from config.config import settings


def phone_number_verify(raw_phone):
    # if raw_phone[0] != '8' and raw_phone[0] != '+':
    #     raw_phone = '+' + raw_phone
    try:
        phone_number = PhoneNumber.from_string(
            phone_number=raw_phone,
            region=settings.PHONENUMBER_DEFAULT_REGION).as_e164
    except NumberParseException:
        phone_number = None
    return phone_number
