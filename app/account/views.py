from . import account


@account.route('/', methods=['GET'])
def index():
    return 'Hi'
