from enum import IntEnum

class Tag(IntEnum):
    IPV4           = 101
    IPV6           = 102
    DOMAIN         = 103
    EMAIL          = 104
    HOSTNAME       = 105
    CARD_NUMBER    = 106
    IBAN           = 107
    COUNTRY_CODE   = 108
    MAC_ADDRESS    = 109
    URL            = 110

# Автоматически создаем TAG2STR
TAG2STR = {tag.value: tag.name for tag in Tag}

# Также можно получить обратное отображение
STR2TAG = {tag.name: tag.value for tag in Tag}