"""
Colors defined as Enum

The colours have been sourced from:
https://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
"""

# flake8: noqa

from enum import Enum


class Colour(Enum):

    def __repr__(self):
        return f'{self.name}: {self.value}'

    def __str__(self) -> str:
        return self.name

    @property
    def hex(self) -> str:
        return self.value

    @property
    def rgb(self) -> tuple:
        value = self.value.lstrip('#')
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

    ALICE_BLUE =             '#F0F8FF'
    ANTIQUE_WHITE =          '#FAEBD7'
    AQUA =                   '#00FFFF'
    AQUAMARINE =             '#7FFFD4'
    AZURE =                  '#F0FFFF'
    BEIGE =                  '#F5F5DC'
    BISQUE =                 '#FFE4C4'
    BLACK =                  '#000000'
    BLANCHEDALMOND =         '#FFEBCD'
    BLUE =                   '#0000FF'
    BLUEVIOLET =             '#8A2BE2'
    BROWN =                  '#A52A2A'
    BURLYWOOD =              '#DEB887'
    CADET_BLUE =             '#5F9EA0'
    CHARTREUSE =             '#7FFF00'
    CHOCOLATE =              '#D2691E'
    CORAL =                  '#FF7F50'
    CORNFLOWER_BLUE =        '#6495ED'
    CORNSILK =               '#FFF8DC'
    CRIMSON =                '#DC143C'
    CYAN =                   '#00FFFF'
    DARK_BLUE =              '#00008B'
    DARK_CYAN =              '#008B8B'
    DARK_GOLDENROD =         '#B8860B'
    DARK_GRAY =              '#A9A9A9'
    DARK_GREEN =             '#006400'
    DARK_KHAKI =             '#BDB76B'
    DARK_MAGENTA =           '#8B008B'
    DARK_OLIVEGREEN =        '#556B2F'
    DARK_ORANGE =            '#FF8C00'
    DARK_ORCHID =            '#9932CC'
    DARK_RED =               '#8B0000'
    DARK_SALMON =            '#E9967A'
    DARK_SEAGREEN =          '#8FBC8F'
    DARK_SLATEBLUE =         '#483D8B'
    DARK_SLATEGRAY =         '#2F4F4F'
    DARK_TURQUOISE =         '#00CED1'
    DARK_VIOLET =            '#9400D3'
    DEEP_PINK =              '#FF1493'
    DEEP_SKYBLUE =           '#00BFFF'
    DIMGRAY =                '#696969'
    DODGERBLUE =             '#1E90FF'
    FIREBRICK =              '#B22222'
    FLORAL_WHITE =           '#FFFAF0'
    FOREST_GREEN =           '#228B22'
    FUCHSIA =                '#FF00FF'
    GAINSBORO =              '#DCDCDC'
    GHOST_WHITE =            '#F8F8FF'
    GOLD =                   '#FFD700'
    GOLDENROD =              '#DAA520'
    GRAY =                   '#808080'
    GREEN =                  '#008000'
    GREEN_YELLOW =           '#ADFF2F'
    HONEYDEW =               '#F0FFF0'
    HOT_PINK =               '#FF69B4'
    INDIAN_RED =             '#CD5C5C'
    INDIGO =                 '#4B0082'
    IVORY =                  '#FFFFF0'
    KHAKI =                  '#F0E68C'
    LAVENDER =               '#E6E6FA'
    LAVENDER_BLUSH =         '#FFF0F5'
    LAWNGREEN =              '#7CFC00'
    LEMONCHIFFON =           '#FFFACD'
    LIGHT_BLUE =             '#ADD8E6'
    LIGHT_CORAL =            '#F08080'
    LIGHT_CYAN =             '#E0FFFF'
    LIGHT_GOLDENROD_YELLOW = '#FAFAD2'
    LIGHT_GREEN =            '#90EE90'
    LIGHT_GRAY =             '#D3D3D3'
    LIGHT_PINK =             '#FFB6C1'
    LIGHT_SALMON =           '#FFA07A'
    LIGHT_SEAGREEN =         '#20B2AA'
    LIGHT_SKYBLUE =          '#87CEFA'
    LIGHT_SLATEGRAY =        '#778899'
    LIGHT_STEELBLUE =        '#B0C4DE'
    LIGHT_YELLOW =           '#FFFFE0'
    LIME =                   '#00FF00'
    LIMEGREEN =              '#32CD32'
    LINEN =                  '#FAF0E6'
    MAGENTA =                '#FF00FF'
    MAROON =                 '#800000'
    MEDIUM_AQUAMARINE =      '#66CDAA'
    MEDIUM_BLUE =            '#0000CD'
    MEDIUM_ORCHID =          '#BA55D3'
    MEDIUM_PURPLE =          '#9370DB'
    MEDIUM_SEAGREEN =        '#3CB371'
    MEDIUM_SLATEBLUE =       '#7B68EE'
    MEDIUM_SPRINGGREEN =     '#00FA9A'
    MEDIUM_TURQUOISE =       '#48D1CC'
    MEDIUM_VIOLETRED =       '#C71585'
    MIDNIGHT_BLUE =          '#191970'
    MINTCREAM =              '#F5FFFA'
    MISTYROSE =              '#FFE4E1'
    MOCCASIN =               '#FFE4B5'
    NAVAJOWHITE =            '#FFDEAD'
    NAVY =                   '#000080'
    OLDLACE =                '#FDF5E6'
    OLIVE =                  '#808000'
    OLIVEDRAB =              '#6B8E23'
    ORANGE =                 '#FFA500'
    ORANGERED =              '#FF4500'
    ORCHID =                 '#DA70D6'
    PALE_GOLDENROD =         '#EEE8AA'
    PALE_GREEN =             '#98FB98'
    PALE_TURQUOISE =         '#AFEEEE'
    PALE_VIOLETRED =         '#DB7093'
    PAPAYA_WHIP =            '#FFEFD5'
    PEACHPUFF =              '#FFDAB9'
    PERU =                   '#CD853F'
    PINK =                   '#FFC0CB'
    PLUM =                   '#DDA0DD'
    POWDER_BLUE =            '#B0E0E6'
    PURPLE =                 '#800080'
    RED =                    '#FF0000'
    ROSYBROWN =              '#BC8F8F'
    ROYAL_BLUE =             '#4169E1'
    SADDLE_BROWN =           '#8B4513'
    SALMON =                 '#FA8072'
    SANDY_BROWN =            '#FAA460'
    SEA_GREEN =              '#2E8B57'
    SEA_SHELL =              '#FFF5EE'
    SIENNA =                 '#A0522D'
    SILVER =                 '#C0C0C0'
    SKYBLUE =                '#87CEEB'
    SLATE_BLUE =             '#6A5ACD'
    SLATE_GRAY =             '#708090'
    SNOW =                   '#FFFAFA'
    SPRING_GREEN =           '#00FF7F'
    STEEL_BLUE =             '#4682B4'
    TAN =                    '#D2B48C'
    TEAL =                   '#008080'
    THISTLE =                '#D8BFD8'
    TOMATO =                 '#FF6347'
    TURQUOISE =              '#40E0D0'
    VIOLET =                 '#EE82EE'
    WHEAT =                  '#F5DEB3'
    WHITE =                  '#FFFFFF'
    WHITE_SMOKE =            '#F5F5F5'
    YELLOW =                 '#FFFF00'
    YELLOW_GREEN =           '#9ACD32'
