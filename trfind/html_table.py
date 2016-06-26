
def _get_some_text_content(table_cell_node):
    ''' Remove all the links and crap and just return a simplified contents string
    '''
    try: 
        title = table_cell_node.text.strip()
        if title:
            return title
    except AttributeError:
        pass # No content at the top level; we need to go deeper

    children = table_cell_node.getchildren()
    for child in children:
        # Sometimes there are multiple links and stuff; the real name is in the first element that works
        try:
            return _get_some_text_content(child)
        except AttributeError:
            continue


def _get_first_link_target(node):
    return node.find('a').attrib['href']


def _get_report_data_from_row(results_row, headers, link_column_index):
    values = [_get_some_text_content(col) for col in results_row]
    data = dict(zip(headers, values))
    data['Link'] = _get_first_link_target(results_row[link_column_index])
    return data


def get_basic_data_from_table(table_node, link_column_index):
    ''' Given an HTML table etree node, get simplified row contents as a list of dicts
    '''
    rows = iter(table_node.findall('tr'))
    headers = [_get_some_text_content(col) for col in next(rows)]

    return [
        _get_report_data_from_row(row, headers, link_column_index)
        for row in rows
    ]
