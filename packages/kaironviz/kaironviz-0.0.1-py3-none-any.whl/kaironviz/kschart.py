import json
import pandas as pd
from jsmin import jsmin
import uuid
import os

from IPython.display import HTML, display

module_dir = os.path.dirname(os.path.abspath(__file__))


def sanky_chart(dataframe, headers, height=450, legend ="chart example", legend_style = 'text-align: center; font: 28px Arial', text_scale = 1, text_color = '#333', text_font='Arial', draw_labels = True, draw_column_labels = True, trancation = 20,  node_width = 20, vertical_spacing = 20, show_toolbar = True,  from_prefix = '', to_prefix = '', from_suffix = '', to_suffix = '', label_distance = 10, use_gradient = True,  client_height = 0):
    """
    create a sanky chart to visualize the relationship between columns
    """
    jsonStr = dataframe.to_json(orient='records')
    headers = json.dumps(headers)
    text = open( module_dir + '/kschart_/kschart_template.html', 'r').read()
    drillChart_js = open(module_dir + '/kschart_/kschart.js', 'r').read()
    drillChart_js = jsmin(drillChart_js)
    unique_id_str = str(uuid.uuid4())
    text = text.replace('@data_label', unique_id_str)
    chart_container_height = height + 80
    if client_height < height and client_height > 0:
        chart_container_height = client_height + 80
    if show_toolbar:
        chart_container_height = chart_container_height + 150
    text = text.replace('@chart_container_height', str(chart_container_height))
    text = text.replace('@chart_height', str(height))
    text = text.replace('@chart_client_height', str(client_height))
    text = text.replace('@chart_legend_style', legend_style)
    text = text.replace('@chart_legend_name', legend)
    text = text.replace('@chart_text_scale', str(text_scale))
    text = text.replace('@chart_text_color', text_color)
    text = text.replace('@chart_text_font', text_font)
    text = text.replace('@chart_draw_labels', str(draw_labels).lower())
    text = text.replace('@chart_draw_column_labels', str(draw_column_labels).lower())
    text = text.replace('@chart_trancation', str(trancation))
    text = text.replace('@chart_node_width', str(node_width))
    text = text.replace('@chart_vertical_spacing', str(vertical_spacing))
    text = text.replace('@chart_show_toolbar', str(show_toolbar).lower())
    text = text.replace('@chart_from_prefix', from_prefix)
    text = text.replace('@chart_to_prefix', to_prefix)
    text = text.replace('@chart_from_suffix', from_suffix)
    text = text.replace('@chart_to_suffix', to_suffix)
    text = text.replace('@chart_label_distance', str(label_distance))
    text = text.replace('@chart_use_gradient', str(use_gradient).lower())

    text = text.replace('@kschart_js_inject', drillChart_js)
    text = text.replace('@chart_headers', headers)
    text = text.replace('@chart_data', jsonStr)

    display(HTML('<div>'+text+'</div>'))
    return text



def sanky_chart2(dataframe, src_name, dest_name, src_level, dest_level, height=450, legend ="chart example", legend_style = 'text-align: center; font: 28px Arial', text_scale = 1, text_color = '#333', text_font='Arial', draw_labels = True, draw_column_labels = True, trancation = 20,  node_width = 20, vertical_spacing = 20, show_toolbar = True, from_prefix = '', to_prefix = '', from_suffix = '', to_suffix = '', label_distance = 10, color_mode = 0, use_gradient = True, client_height = 0):
    """
    create a sanky chart to visualize relationship between source and destination column entities where level is the column that the entities belong to in the sanky chart belongs to
    """
    jsonStr = dataframe.to_json(orient='records')
    text = open(module_dir + '/kschart_/kschart_template2.html', 'r').read()
    drillChart_js = open(module_dir + '/kschart_/kschart.js', 'r').read()
    drillChart_js = jsmin(drillChart_js)
    unique_id_str = str(uuid.uuid4())
    text = text.replace('@data_label', unique_id_str)
    chart_container_height = height + 100
    if client_height < height and client_height > 0:
        chart_container_height = client_height + 100
    if show_toolbar:
        chart_container_height = chart_container_height + 150
    text = text.replace('@chart_container_height', str(chart_container_height))
    text = text.replace('@chart_height', str(height))
    text = text.replace('@chart_client_height', str(client_height))
    text = text.replace('@chart_legend_style', legend_style)
    text = text.replace('@chart_legend_name', legend)
    text = text.replace('@chart_text_scale', str(text_scale))
    text = text.replace('@chart_text_color', text_color)
    text = text.replace('@chart_text_font', text_font)
    text = text.replace('@chart_draw_labels', str(draw_labels).lower())
    text = text.replace('@chart_draw_column_labels', str(draw_column_labels).lower())
    text = text.replace('@chart_trancation', str(trancation))
    text = text.replace('@chart_node_width', str(node_width))
    text = text.replace('@chart_vertical_spacing', str(vertical_spacing))
    text = text.replace('@chart_show_toolbar', str(show_toolbar).lower())
    text = text.replace('@chart_from_prefix', from_prefix)
    text = text.replace('@chart_to_prefix', to_prefix)
    text = text.replace('@chart_from_suffix', from_suffix)
    text = text.replace('@chart_to_suffix', to_suffix)
    text = text.replace('@chart_label_distance', str(label_distance))
    text = text.replace('@chart_color_mode', str(color_mode))
    text = text.replace('@chart_use_gradient', str(use_gradient).lower())


    text = text.replace('@kschart_js_inject', drillChart_js)
    text = text.replace('@chart_src_name', src_name)
    text = text.replace('@chart_dest_name', dest_name)
    text = text.replace('@chart_src_level', src_level)
    text = text.replace('@chart_dest_level', dest_level)
    text = text.replace('@chart_data', jsonStr)

    display(HTML('<div>'+text+'</div>'))
    return text


def drill_chart(data, start_label, y_label = 'values', legend = 'Drill Chart', legend_color = 'black', legend_font = 'Bold 20px Arial', legend_pos = 'bottom', legend_align = 'center', nav_color = '#046688', nav_font = '16px Arial', nav_justify = 'right', nav_padding = '10px', label_scale = 1.2, label_color = 'black', resolution = 1.2, background_color = 'transparent', height = 480, max_column_width=100):
    """
        create a n level drill down chart
    """
    jsonStr = json.dumps(data)
    text = open(module_dir +'/kschart_/drill_Chart_template.html', 'r').read()
    drillChart_js = open(module_dir +'/kschart_/drillChart.js', 'r').read()
    drillChart_js = jsmin(drillChart_js)
    unique_id_str = str(uuid.uuid4())

    text = text.replace('@data_label', unique_id_str)

    chart_container_height = height + 80
    text = text.replace('@chart_container_height', str(chart_container_height))

    text = text.replace('@chart_start_label', start_label)
    text = text.replace('@chart_y_label', y_label)
    text = text.replace('@chart_legend_text', legend)
    text = text.replace('@chart_legend_color', legend_color)
    text = text.replace('@chart_legend_font', legend_font)
    text = text.replace('@chart_legend_pos', legend_pos)
    text = text.replace('@chart_legend_align', legend_align)
    text = text.replace('@chart_nav_color', nav_color)
    text = text.replace('@chart_nav_font', nav_font)
    text = text.replace('@chart_nav_justify', nav_justify)
    text = text.replace('@chart_nav_padding', nav_padding)
    text = text.replace('@chart_label_scale', str(label_scale))
    text = text.replace('@chart_label_color', label_color)
    text = text.replace('@chart_resolution', str(resolution))
    text = text.replace('@chart_background_color', background_color)
    text = text.replace('@chart_height', str(height))
    text = text.replace('@chart_max_column_width', str(max_column_width))



    text = text.replace('@drill_chart_js_inject', drillChart_js)
    text = text.replace('@chart_data', jsonStr)

    display(HTML('<div>'+text+'</div>'))
    return text
