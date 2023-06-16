_eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
_to_rus = dict(zip(_eng_chars, _rus_chars))
_to_eng = dict(zip(_rus_chars, _eng_chars))


def to_rus(s):
    return u''.join([_to_rus.get(c, c) for c in s])


def to_eng(s):
    return u''.join([_to_eng.get(c, c) for c in s])


print(to_rus('привет'))
print(to_eng('привет'))
