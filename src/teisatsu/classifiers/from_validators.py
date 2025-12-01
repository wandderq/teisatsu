from typing import Any

import validators


# tag: ipv4
def is_ipv4(thing: Any) -> bool | str:
    return 'tag' if (validators.ipv4(thing) == True) else False


# tag: ipv6
def is_ipv6(thing: Any) -> bool | str:
    return 'tag' if (validators.ipv6(thing) == True) else False


# tag: email
def is_email(thing: Any) -> bool | str:
    return 'tag' if (validators.email(thing) == True) else False


# tag: card_number
def is_card_number(thing: Any) -> bool | str:
    return 'tag' if (validators.card_number(thing) == True) else False


# tag: iban
def is_iban(thing: Any) -> bool | str:
    return 'tag' if (validators.iban(thing) == True) else False


# tag: country_code
def is_country_code(thing: Any) -> bool | str:
    return 'tag' if (validators.country_code(thing) == True) else False


# tag: domain
def is_domain(thing: Any) -> bool | str:
    return 'tag' if (validators.domain(thing) == True) else False


# tag: hostname
def is_hostname(thing: Any) -> bool | str:
    return 'tag' if (validators.hostname(thing) == True) else False


# tag: mac_address
def is_mac_address(thing: Any) -> bool | str:
    return 'tag' if (validators.mac_address(thing) == True) else False


# tag: url
def is_url(thing: Any) -> bool | str:
    return 'tag' if (validators.url(thing) == True) else False