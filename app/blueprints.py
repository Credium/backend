from flask import Blueprint


def _factory(partial_module_string, url_prefix):
    name = partial_module_string
    import_name = 'app.{}.views'.format(partial_module_string)
    template_folder = 'templates'
    blueprint = Blueprint(name,
                          import_name,
                          template_folder=template_folder,
                          url_prefix=url_prefix)
    return blueprint


account = _factory('account', '/account')

all_blueprints = (account, )
