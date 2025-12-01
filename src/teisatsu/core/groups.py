from ..classifiers import *
from .. import scripts

TAGS = [
    {'name': 'ipv4',         'func': is_ipv4         },
    {'name': 'ipv6',         'func': is_ipv6         },
    {'name': 'email',        'func': is_email        },
    {'name': 'card_number',  'func': is_card_number  },
    {'name': 'iban',         'func': is_iban         },
    {'name': 'country_code', 'func': is_country_code },
    {'name': 'domain',       'func': is_domain       },
    # {'name': 'hostname',     'func': is_hostname     },
    {'name': 'mac_address',  'func': is_mac_address  },
    {'name': 'url',          'func': is_url          },
]

SCRIPTS = [
    {
        'name': script.TSS_NAME,
        'tags': script.TSS_TAGS,
        'requirements': script.TSS_REQUIREMENTS,
        'object': script.TSS_OBJECT
    }
    for script in scripts.scripts_list
]