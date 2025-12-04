from ...core.tags import Tag
import validators



def is_ipv4(thing: str) -> int:
    return Tag.IPV4 if (validators.ipv4(thing) == True) else False


def is_ipv6(thing: str) -> int:
    return Tag.IPV6 if (validators.ipv6(thing) == True) else False


def is_email(thing: str) -> int:
    return Tag.EMAIL if (validators.email(thing) == True) else False


def is_card_number(thing: str) -> int:
    return Tag.CARD_NUMBER if (validators.card_number(thing) == True) else False


def is_iban(thing: str) -> int:
    return Tag.IBAN if (validators.iban(thing) == True) else False


def is_country_code(thing: str) -> int:
    return Tag.COUNTRY_CODE if (validators.country_code(thing) == True) else False


def is_domain(thing: str) -> int:
    return Tag.DOMAIN if (validators.domain(thing) == True) else False


def is_hostname(thing: str) -> int:
    return Tag.HOSTNAME if (validators.hostname(thing) == True) else False


def is_mac_address(thing: str) -> int:
    return Tag.MAC_ADDRESS if (validators.mac_address(thing) == True) else False


def is_url(thing: str) -> int:
    return Tag.URL if (validators.url(thing) == True) else False