from flask import Markup
from itertools import product

# maps strings to dictionaries
def domains():
    BOOLEAN = [False, True]
    COLOR = xrange(256*256*256)
    return {
        'opacity': [.9, 1],
        'h_left_above': BOOLEAN,
        'h_right_above': BOOLEAN,
        'c_top_above': BOOLEAN,
        'k_top_above': BOOLEAN,
        'palette_1': COLOR,
        'palette_2': COLOR,
        'palette_3': COLOR,
        'palette_4': COLOR,
        'palette_5': COLOR,
        'colors_limit': [3, 4, 5],
        'h_left_color': range(5),
        'h_mid_color': range(5),
        'h_right_color': range(5),
        'a_outer_color': range(5),
        'a_inner_color': range(5),
        'c_top_color': range(5),
        'c_bottom_color': range(5),
        'k_top_color': range(5),
        'k_bottom_color': range(5),
    }

def mutate(parameters):
    return parameters

def combine(parent_a, parent_b):
    return genetic.combine_random(parent_a, parent_b)

# returns Markup object
def generate(parameters):
    def color2rgb(color):
        return '#%06x' % color
    limit = parameters['colors_limit']
    colors = list(map(color2rgb, [parameters['palette_{}'.format(i)] for i in range(1,6)]))
    opacity = parameters['opacity']
    h_left = '''<rect height="110.0" width="50.0" opacity="{opacity}" fill="%s"/>''' % colors[parameters['h_left_color'] % limit]
    h_mid = '''<rect height="33.333333333333336" width="100.0" opacity="{opacity}" fill="%s" x="10.0" y="38.33333333333333"/>''' % colors[parameters['h_mid_color']]
    h_right = '''<rect height="110.0" width="50.0" opacity="{opacity}" fill="%s" x="60.0"/>''' % colors[parameters['h_right_color'] % limit]
    if parameters['h_left_above']:
        h_parts = [h_mid, h_left]
    else:
        h_parts = [h_left, h_mid]
    if parameters['h_right_above']:
        h_parts.append(h_right)
    else:
        h_parts.insert(0, h_right)
    letter_h = '''
      <g transform="translate(20.0,20.0)">
        <g height="110.0" width="110.0">
        {}{}{}
        </g>
      </g>
    '''.format(*h_parts)
    letter_a = '''
      <g transform="translate(150.0,20.0)">
        <g height="110.0" width="110.0">
          <polygon points="0,110.0 110.0,110.0 55.0,0" opacity="{opacity}" fill="%s"/>
          <polygon points="20.0,110.0 90.0,110.0 55.0,40.0" opacity="{opacity}" fill="%s"/>
        </g>
      </g>
    ''' % (colors[parameters['a_outer_color'] % limit], colors[parameters['a_inner_color'] % limit])
    c_bottom = '''<g transform="translate(0,110.0) scale(1,-1)">
            <path opacity="{opacity}" d="M 99.49593469062211,22.671811123913976 A 55.0,55.0 0 1 0 33.95241121992003 105.81337428812076 Z" fill="%s"/>
          </g>''' % colors[parameters['c_bottom_color'] % limit]
    c_top = '''<path opacity="{opacity}" d="M 99.49593469062211,22.671811123913976 A 55.0,55.0 0 1 0 33.95241121992003 105.81337428812076 Z" fill="%s"/>''' % colors[parameters['c_top_color'] % limit]
    c_parts = [c_bottom, c_top] if parameters['c_top_above'] else [c_top, c_bottom]
    letter_c = '''
      <g transform="translate(20.0,150.0)">
        <g height="110.0" width="110.0">
        {}{}
        </g>
      </g>
    '''.format(*c_parts)
    k_top = '''<polygon points="0,110.0 0,0 110.0,0 50.0,110.0" opacity="{opacity}" fill="%s"/>''' % colors[parameters['k_top_color'] % limit]
    k_bottom = '''<polygon points="0,0 0,110.0 110.0,110.0 50.0,0" opacity="{opacity}" fill="%s"/>''' % colors[parameters['k_bottom_color'] % limit]
    k_parts = [k_bottom, k_top] if parameters['k_top_above'] else [k_top, k_bottom]
    letter_k = '''
      <g transform="translate(150.0,150.0)">
        <g height="110.0" width="110.0">
        {}{}
        </g>
      </g>
    '''.format(*k_parts)
    logo = '''
    <svg xmlns="http://www.w3.org/2000/svg" height="280.0" width="280.0" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
      <rect height="100%" width="100%" fill="#ecf0f1"/>
      {}{}{}{}
    </svg>
    '''.format(letter_h, letter_a, letter_c, letter_k, opacity=opacity)
    return Markup(logo)
