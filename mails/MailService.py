from mails import MailRepository, FakeNewsDetector


def get_texts(no_messages: int):
    return MailRepository.get_all_texts(no_messages=no_messages)


def get_interpreted_messages(no_messages: int):
    messages, no_messages = get_texts(no_messages=no_messages)
    return FakeNewsDetector.getMessages(messages)
