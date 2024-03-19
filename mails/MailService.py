from mails import MailRepository


def get_texts(no_messages: int):
    return MailRepository.get_all_texts(no_messages=no_messages)