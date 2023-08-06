from __future__ import absolute_import, division, print_function

import ast
import distutils
import json
import os
import re
import sys
import subprocess
import logging
import zipfile
from collections import OrderedDict

from random import choice

from six import iteritems, string_types

logger = logging.getLogger(__name__)


def pdflatex_command_found():
    return bool(distutils.spawn.find_executable('pdflatex'))


def get_sublist(list, idxs):
    """Get items of a list based on a collection of indices.

    :param list: list from which items are taken
    :type list: list
    :param idxs: list with indices to be collected
    :type idxs: list
    :return: new list based on idxs
    :rtype: list
    """
    return [list[i] for i in idxs]


def assert_dict_keys(dic, expected_keys, all_keys_required=False):
    """Method to assert that a dictionary has the expected keys and (optionally) to check if is has all the keys.

    :param dic: dictionary to checked
    :type dic: dict
    :param expected_keys: keys expected in dictionary
    :type expected_keys: list
    :param all_keys_required: (optional) to check if all keys are in the dictionary
    :type all_keys_required: bool
    :returns: check results
    """
    assert isinstance(dic, dict), 'dic should be a dictionary.'
    dict_keys = list(dic)
    if all_keys_required:
        assert not set(expected_keys).symmetric_difference(dict_keys), 'Not all expected keys are in the dictionary.'
    else:
        assert set(dict_keys).issubset(expected_keys), 'Dictionary keys are not a subset of the expected keys.'


def dict_to_ord_dict(dic, key_order):
    """Method to transform a Python dictionary into a Python ordered dictionary.

    :param dic: dictionary
    :type dic: dict
    :param key_order: order of the keys
    :type key_order: list
    :return: ordered dictionary
    :rtype: OrderedDict

    .. note:: the key_order list can have items that are not present in the given dictionary. All keys of the
        dictionary should be in the order though.
    """
    assert isinstance(dic, dict), 'dic should be of type dict.'
    assert isinstance(key_order, list), 'key_order should be of type list.'
    assert len(key_order) == len(set(key_order)), 'key_order should consist of unique elements.'
    ord_dict = OrderedDict()
    for key in key_order:
        if key in dic:
            ord_dict.update({key: dic[key]})
            del dic[key]
    assert not dic, 'Dictionary still contains elements with keys: {}'.format(list(dic))
    return ord_dict


def add_nested_dict_entry(dic, attrbs, val=None):
    assert isinstance(attrbs, (list, tuple)), 'Input attributes should be a list or tuple, now is a {}'\
        .format(type(attrbs))
    current_dict = dic
    for i, attrb in enumerate(attrbs):
        if attrb not in current_dict:
            current_dict[attrb] = dict()
        if i == len(attrbs)-1:
            current_dict[attrb] = val
        else:
            if not isinstance(current_dict[attrb], dict):
                current_dict[attrb] = dict()
            current_dict = current_dict[attrb]


def color_list():
    """A list of distinguisable colors.

    :return: list with HTML Hex colors
    """
    return ["#006FA6", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#FFDBE5", "#A30059", "#000000",
            "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87", "#5A0007", "#809693",
            "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80", "#61615A", "#BA0900", "#6B7900",
            "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100", "#DDEFFF", "#000035", "#7B4F4B", "#A1C299",
            "#300018", "#0AA6D8", "#013349", "#00846F", "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744",
            "#C0B9B2", "#C2FF99", "#001E09", "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68",
            "#7A87A1", "#788D66", "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED",
            "#886F4C", "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
            "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00", "#7900D7",
            "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700", "#549E79", "#FFF69F",
            "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329", "#5B4534", "#FDE8DC", "#404E55",
            "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C", "#83AB58", "#001C1E", "#D1F7CE", "#004B28",
            "#C8D0F6", "#A3A489", "#806C66", "#222800", "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59",
            "#8ADBB4", "#1E0200", "#5B4E51", "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94",
            "#7ED379", "#012C58", "#7A7BFF", "#D68E01", "#353339", "#78AFA1", "#FEB2C6", "#75797C", "#837393",
            "#943A4D", "#B5F4FF", "#D2DCD5", "#9556BD", "#6A714A", "#001325", "#02525F", "#0AA3F7", "#E98176",
            "#DBD5DD", "#5EBCD1", "#3D4F44", "#7E6405", "#02684E", "#962B75", "#8D8546", "#9695C5", "#E773CE",
            "#D86A78", "#3E89BE", "#CA834E", "#518A87", "#5B113C", "#55813B", "#E704C4", "#00005F", "#A97399",
            "#4B8160", "#59738A", "#FF5DA7", "#F7C9BF", "#643127", "#513A01", "#6B94AA", "#51A058", "#A45B02",
            "#1D1702", "#E20027", "#E7AB63", "#4C6001", "#9C6966", "#64547B", "#97979E", "#006A66", "#391406",
            "#F4D749", "#0045D2", "#006C31", "#DDB6D0", "#7C6571", "#9FB2A4", "#00D891", "#15A08A", "#BC65E9",
            "#FFFFFE", "#C6DC99", "#203B3C", "#671190", "#6B3A64", "#F5E1FF", "#FFA0F2", "#CCAA35", "#374527",
            "#8BB400", "#797868", "#C6005A", "#3B000A", "#C86240", "#29607C", "#402334", "#7D5A44", "#CCB87C",
            "#B88183", "#AA5199", "#B5D6C3", "#A38469", "#9F94F0", "#A74571", "#B894A6", "#71BB8C", "#00B433",
            "#789EC9", "#6D80BA", "#953F00", "#5EFF03", "#E4FFFC", "#1BE177", "#BCB1E5", "#76912F", "#003109",
            "#0060CD", "#D20096", "#895563", "#29201D", "#5B3213", "#A76F42", "#89412E", "#1A3A2A", "#494B5A",
            "#A88C85", "#F4ABAA", "#A3F3AB", "#00C6C8", "#EA8B66", "#958A9F", "#BDC9D2", "#9FA064", "#BE4700",
            "#658188", "#83A485", "#453C23", "#47675D", "#3A3F00", "#061203", "#DFFB71", "#868E7E", "#98D058",
            "#6C8F7D", "#D7BFC2", "#3C3E6E", "#D83D66", "#2F5D9B", "#6C5E46", "#D25B88", "#5B656C", "#00B57F",
            "#545C46", "#866097", "#365D25", "#252F99", "#00CCFF", "#674E60", "#FC009C", "#92896B"]


def hex_to_rgb(value):
    """Function to translate a hex color string to an RGB color tuple.

    :param value: HTML hex color
    :type value: str
    :return: RGB colors
    :rtype: tuple
    """

    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def get_uid(preference, uids):
    """Simple function to determine a valid uid which is not part of the uids list

    :param preference: preferred name for the uid
    :type preference: str
    :param uids: list of existing uids
    :type uids: list
    :return: a valid uid which
    :rtype: str
    """

    if preference not in uids:
        uid = preference
    else:
        i = 1
        uid = preference + '_' + str(i)
        while uid in uids:
            i += 1
            uid = preference + '_' + str(i)

    return uid


def get_mdao_setup(mdao_setup):
    """Simple function to specify the MDAO architecture and convergence type based on a single string.

    :param mdao_setup: MDF-GS, MDF-J, IDF
    :type mdao_setup: str
    :return: mdo_architecture, mda_type, allow_unconverged_couplings
    :rtype: str
    """

    mdao_defintions = ['unconverged-MDA',  # 0
                       'unconverged-MDA-GS',  # 1
                       'unconverged-MDA-J',  # 2
                       'converged-MDA-GS',  # 3
                       'converged-MDA-J',  # 4
                       'MDF-GS',  # 5
                       'MDF-J',  # 6
                       'IDF',  # 7
                       'unconverged-OPT',  # 8
                       'unconverged-OPT-GS',  # 9
                       'unconverged-OPT-J',  # 10
                       'unconverged-DOE',  # 11
                       'unconverged-DOE-GS',  # 12
                       'unconverged-DOE-J',  # 13
                       'converged-DOE-GS',  # 14
                       'converged-DOE-J',  # 15
                       'CO',  # 16
                       'BLISS-2000']  # 17
    if mdao_setup.endswith(('-FF', '-MC', '-LH', '-CT', '-BB')):
        mdao_setup = mdao_setup[:-3]

    if mdao_setup == mdao_defintions[0]:
        mdo_architecture = 'unconverged-MDA'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[1]:
        mdo_architecture = 'unconverged-MDA'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[2]:
        mdo_architecture = 'unconverged-MDA'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[3]:
        mdo_architecture = 'converged-MDA'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[4]:
        mdo_architecture = 'converged-MDA'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[5]:
        mdo_architecture = 'MDF'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[6]:
        mdo_architecture = 'MDF'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[7]:
        mdo_architecture = 'IDF'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[8]:
        mdo_architecture = 'unconverged-OPT'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[9]:
        mdo_architecture = 'unconverged-OPT'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[10]:
        mdo_architecture = 'unconverged-OPT'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[11]:
        mdo_architecture = 'unconverged-DOE'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[12]:
        mdo_architecture = 'unconverged-DOE'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[13]:
        mdo_architecture = 'unconverged-DOE'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[14]:
        mdo_architecture = 'converged-DOE'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[15]:
        mdo_architecture = 'converged-DOE'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[16]:
        mdo_architecture = 'CO'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[17]:
        mdo_architecture = 'BLISS-2000'
        mda_type = None
        allow_unconverged_couplings = False
    else:
        raise IOError('Incorrect mdao_setup "%s" specified.' % mdao_setup)

    # TODO: Check this!
    if 'unconverged' in mdao_setup:
        allow_unconverged_couplings = True

    return mdo_architecture, mda_type, allow_unconverged_couplings


def test_attr_cond(attr_value, operator, test_value):
    """
    Function to check a given conditional statement and return True or False.

    :param attr_value: value of the actual attribute
    :type attr_value: str, float, int
    :param operator: conditional operator to be used ('<','<=','==','!=','>=','>', 'in')
    :type operator: str
    :param test_value: value to which the attribute value should be compared.
    :type test_value: str, float, int
    :return: result of the conditional statement.
    :rtype: bool
    """

    # Assert inputs
    pos_ops = ['<', '<=', '==', '!=', '>=', '>', 'in']
    assert isinstance(operator, string_types)
    assert {operator}.intersection(set(pos_ops)), "'%s' is an invalid operator, possible operators are: %s." % \
                                                  (operator, pos_ops)
    if operator in pos_ops[0:6]:
        assert type(attr_value) == type(test_value), "Types to be compared (%s and %s) do not match." % \
                                                         (type(attr_value), type(test_value))
    else:
        assert isinstance(attr_value, string_types), "Attribute value of type string was expected."
        assert isinstance(test_value, list), "Test value of type list was expected."

    # Analyse conditional statement
    if operator == pos_ops[0]:
        return True if attr_value < test_value else False
    elif operator == pos_ops[1]:
        return True if attr_value <= test_value else False
    elif operator == pos_ops[2]:
        return True if attr_value == test_value else False
    elif operator == pos_ops[3]:
        return True if attr_value != test_value else False
    elif operator == pos_ops[4]:
        return True if attr_value >= test_value else False
    elif operator == pos_ops[5]:
        return True if attr_value > test_value else False
    elif operator == pos_ops[6]:
        return True if attr_value in test_value else False


def export_as_json(data, filename, indent=None, sort_keys=True, cwd=None):
    """
    Function to export a data object to a json file.

    :param data: object with the data to be exported
    :type data: dict or list
    :param filename: name of the json file
    :type filename: str
    :param indent: number of spaces for one indentation
    :type indent: int
    :param sort_keys: option for sorting keys
    :type sort_keys: bool
    :param cwd: current working directory
    :type cwd: None, str
    :return: json file
    :rtype: file
    """
    assert isinstance(filename, string_types)
    assert filename[-5:] == '.json', 'File extension should be given and should be ".json".'
    if cwd is not None: 
        os.chdir(cwd)
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=indent, sort_keys=sort_keys)


def transform_data_into_strings(data, keys_to_be_removed=list()):
    """
    Utility function to transform certain data types in a dictionary into strings.

    :param data: dictionary with data
    :type data: dict
    :param keys_to_be_removed: list of keys that have to be removed from the dict
    :type keys_to_be_removed: list
    :return: adjusted dictionary
    :rtype: dict
    """

    # Input assertions
    assert isinstance(data, dict)
    assert isinstance(keys_to_be_removed, list)

    for key, item in iteritems(data):
        if item is None:
            data[key] = "None"
        elif type(item) is list:
            data[key] = str(item)
        elif type(item) is dict:
            data[key] = str(item)
        elif type(item) is tuple:
            data[key] = str(item)

    for key in keys_to_be_removed:
        if key in data:
            del data[key]

    return data


def transform_string_into_format(data, keys_to_be_removed=list()):
    """
    Utility function to transform certain strings back into their original data format (NoneType, list, etc.).

    :param data: dictionary with data
    :type data: dict
    :param keys_to_be_removed: list of keys that have to be removed from the dict
    :type keys_to_be_removed: list
    :return: adjusted dictionary
    :rtype: dict
    """

    # Input assertions
    assert isinstance(data, dict)
    assert isinstance(keys_to_be_removed, list)

    for key, item in iteritems(data):
        if item == "None":
            data[key] = None
        elif isinstance(item, string_types):
            if item[0] == '[' and item[-1] == ']':
                data[key] = ast.literal_eval(item)
            elif item[0] == '{' and item[-1] == '}':
                data[key] = ast.literal_eval(item)
            elif item[0] == '(' and item[-1] == ')':
                data[key] = ast.literal_eval(item)

    for key in keys_to_be_removed:
        if key in data:
            del data[key]

    return data


def make_plural(string):
    """
    Function to convert a string to its plural form.

    :param string: initial string
    :type string: str
    :return: plural string
    :rtype: str
    """

    if string[-3:] == 'sis':
        # e.g. 'analysis' should become 'analyses'
        string = string[:-3] + 'ses'
    else:
        # e.g. 'variable' should become 'variables'
        string += 's'

    return string


def make_singular(string):
    """
    Function to convert a string to its singular form.

    :param string: initial string
    :type string: str
    :return: singular string
    :rtype: str
    """

    if string[-3:] == 'ses':
        # e.g. 'analyses' should become 'analysis'
        string = string[:-3] + 'sis'
    elif string[-1:] == 's':
        # e.g. 'variables' should become 'variable'
        string = string[:-1]

    return string


def make_camel_case(string, make_plural_option=False):
    """
    Function to make a string camelCase.

    :param string: non-camelcase string
    :type string: str
    :param make_plural_option: pluralize camelcase string
    :type make_plural_option: bool
    :return: camelcase string
    :rtype: str
    """

    word_regex_pattern = re.compile("[^A-Za-z]+")
    words = word_regex_pattern.split(string)
    string = "".join(w.lower() if i is 0 else w.title() for i, w in enumerate(words))

    if string[-3:] == 'Uid':
        string = string[:-3] + 'UID'  # TODO: This can also be solved more generically.

    if make_plural_option:
        string = make_plural(string)

    return string


def unmake_camel_case(string, separator='_'):
    """
    Function to make camelCase a string with separator (e.g. underscores).

    :param string: camelCase string
    :type string: str
    :param separator: symbol/symbols used as separator
    :type separator: str
    :return: string with separator
    :rtype: str
    """

    string = re.sub(r"(\w)([A-Z])", r"\1"+separator+r"\2", string)  # Add separator
    string = string.lower()  # Remove capitalization

    # Hack for uIDs
    # TODO: Remove this if camelCase is used throughout KADMOS
    if string[-5:] == '_ui_d':
        string = string[:-5] + '_u_i_d'

    return string


def format_string_for_vistoms(string, prefix='', suffix=''):
    """
    Function to format a string such that it can be used in VISTOMS.

    :param string: string to be formatted
    :type string: str
    :param prefix: prefix to be placed in front of the string
    :type prefix: str
    :param suffix: suffix to be appended to the string
    :type suffix: str
    :return: formatted string
    :rtype: str
    """
    replacement_list = ((' ', ''), ('_', '-'), ('[', ''), (']', ''), ('.', '-'))
    for repl in replacement_list:
        string = string.replace(repl[0], repl[1])
    return str(prefix) + string + str(suffix)


def format_string_for_vistoms_new(string, prefix='', suffix=''):
    """
    Function to format a string such that it can be used in VISTOMS.

    :param string: string to be formatted
    :type string: str
    :param prefix: prefix to be placed in front of the string
    :type prefix: str
    :param suffix: suffix to be appended to the string
    :type suffix: str
    :return: formatted string
    :rtype: str
    """
    replacement_list = ((' ', ''), ('_', '-'))
    for repl in replacement_list:
        string = string.replace(repl[0], repl[1])

    string = re.sub("[\[].*?[\]]", "", string)
    string = string.split('.')[0]

    return str(prefix) + string + str(suffix)


def format_string_for_latex(string, prefix='', suffix=''):
    """
    Function to format a string such that it can be used in LaTeX.

    :param string: string to be formatted
    :type string: str
    :param prefix: prefix to be placed in front of the string
    :type prefix: str
    :param suffix: suffix to be appended to the string
    :type suffix: str
    :return: formatted string
    :rtype: str
    """
    replacement_list = (('_', '\_'), ('&', '\&'), ('%', '\%'), ('#', '\#'))
    string.encode('unicode-escape')
    for repl in replacement_list:
        string = string.replace(repl[0], repl[1])
    return str(prefix) + string + str(suffix)


def get_list_entries(*args):
    """
    Utility to return only certain values of a given list based on the indices.

    :param args: list and indices
    :type args: list and int
    :return: list with requested values at indices
    :rtype: list
    """
    assert isinstance(args[0], list), 'First argument should be a list.'
    assert len(args) > 1, 'At least two arguments are required.'
    input_list = args[0]
    return_list = []
    for arg in args[1:]:
        assert isinstance(arg, int), 'Indices should be integers.'
        return_list.append(input_list[arg])
    return return_list


def remove_if_exists(input_list, entries_to_remove):
    """
    Utility to remove certain values from a list.

    :param input_list: initial list
    :type input_list: list
    :param entries_to_remove: values to remove
    :type entries_to_remove: list
    :return: list with removed entries
    :rtype: list
    """
    assert isinstance(input_list, list)

    for entry in entries_to_remove:
        if entry in input_list:
            input_list.remove(entry)
    return input_list


def get_friendly_id(uid_length):
    """ Create a recognisable ID string.

    :param uid_length: length of the ID
    :type uid_length: int
    :return: new ID
    :rtype: str
    """
    v = 'aeiou'
    c = 'bdfghklmnprstvw'
    return ''.join([choice(v if i % 2 else c) for i in range(uid_length)])


def get_unique_friendly_id(used_ids, uid_length):
    """Return an ID that is not in our list of already used IDs.

    :param used_ids: already used IDs
    :type used_ids: list
    :param uid_length: length of the ID
    :type uid_length: int
    :return: new unique ID
    :rtype: str
    """

    # trying infinitely is a bad idea
    limit = 1000

    count = 0
    while count < limit:
        idx = get_friendly_id(uid_length)
        if idx not in used_ids:
            return idx
        count += 1
        if count == limit:
            raise NotImplementedError('Could not create a unique UID, increase limit or uid_length used.')


def open_file(filename):
    """
    Utility to open a file cross-platform.

    :param filename: Filename including extension and path, e.g. 'sampledir/samplefile.pdf'
    :type filename: str
    :return: An opened file
    """

    if sys.platform == 'linux2':
        return subprocess.check_output('xdg-open ' + filename, shell=True)
    elif sys.platform == 'darwin':
        return subprocess.check_output('open ' + re.escape(filename), shell=True)
    else:
        return subprocess.check_output('start ' + filename, shell=True)


def get_element_dict(xpath, var_value=None, var_dim=None, include_reference_data=False):
    """
    Function to create a D3.js-type dictionary for a nested tree based on an xpath.

    :param xpath: xpath for the element
    :type xpath: str
    :param var_value: value of the element in a reference file
    :type var_value: float
    :param var_dim: dimension of the element in a reference file
    :type var_dim: int
    :param include_reference_data: setting on whether reference data should be include in the path
    :type include_reference_data: bool
    :return: nested dictionary
    :rtype: dict
    """

    # Make tree dictionary
    xpath_list = xpath.split('/')[1:]
    xpath_list.reverse()
    max_depth = len(xpath_list) - 1

    for idx, element in enumerate(xpath_list):
        if idx == 0:
            if include_reference_data:
                element_dict = dict(name=element, level=max_depth - idx, type='variable',
                                    value=var_value, dimension=var_dim)
            else:
                element_dict = dict(name=element, level=max_depth - idx, type='variable')
        else:
            if idx != max_depth:
                # TODO: Should this not be a different type? Like group?
                # noinspection PyUnboundLocalVariable
                element_dict = dict(name=element, level=max_depth - idx, type='variable', children=[element_dict])
            else:
                # noinspection PyUnboundLocalVariable
                element_dict = dict(name=element, level=max_depth - idx, children=[element_dict])
    # noinspection PyUnboundLocalVariable
    return element_dict


def translate_list(l, dictionary):
    """
    Utility to quickly translate all elements in a list with a dictionary.

    :param l: list to be translated
    :type l: list
    :param dictionary: dictionary used for the translation
    :type dictionary: dict
    :return: translated list
    :rtype: list
    """
    translated = [dictionary.get(li, li) for li in l]
    return translated


def translate_dict_keys(dictionary, translations):
    """
    Utility to (recursively) translate all keys in a dictionary with a translation dictionary.

    :param dictionary: dictionary to be translated
    :type dictionary: dict
    :param translations: dictionary used for the translation
    :type translations: dict
    :return: translated dictionary
    :rtype: dict
    """

    for key, value in iteritems(dictionary):
        if key in translations:
            del(dictionary[key])
            key = translations[key]
        if type(value) == dict:
            value = translate_dict_keys(value, translations)
        dictionary[key] = value

    return dictionary


def filter_group_vars(group_dict, current_group_idx, filter_setting):
    """Method to get the variables of a local/external group.

    :param group_dict: local/external group
    :type group_dict: dict
    :param current_group_idx: index of the current group
    :type current_group_idx: int
    :param filter_setting: filter on 'local' or 'external' groups
    :type filter_setting: list, string
    :return: group variables
    :rtype: list
    """

    if isinstance(filter_setting, list):
        return [var for var, groups in iteritems(group_dict) if current_group_idx in groups and var in filter_setting]
    elif isinstance(filter_setting, string_types):
        if filter_setting == 'local':
            return [group_coup for group_coup, group_idx in iteritems(group_dict) if group_idx == current_group_idx]
        elif filter_setting == 'external':
            return [group_coup for group_coup, group_idx in iteritems(group_dict) if group_idx != current_group_idx]
    else:
        raise NotImplementedError('Current settings of this function are not implemented.')


def get_group_vars(sa, current_group_idx):
    """Method to get the variables with respect to the subgroup.

    :param sa: system analysis dictionary
    :type sa: dict
    :param current_group_idx: index of the subgroup
    :type current_group_idx: int
    :return: multiple lists with variables
    :rtype: tuple
    """

    global_des_vars_group = filter_group_vars(sa['des_vars']['groups'], current_group_idx, sa['des_vars']['global'])
    local_des_vars_group = filter_group_vars(sa['des_vars']['groups'], current_group_idx, sa['des_vars']['local'])
    local_cnstrnt_vars_group = filter_group_vars(sa['constraints']['groups_vars'], current_group_idx,
                                                 sa['constraints']['local_vars'])
    local_group_couplings_group = filter_group_vars(sa['couplings']['groups'], current_group_idx, 'local')
    external_group_couplings_group = filter_group_vars(sa['couplings']['groups'], current_group_idx, 'external')

    return global_des_vars_group, local_des_vars_group, local_cnstrnt_vars_group, local_group_couplings_group, \
           external_group_couplings_group


def convert_bytes(num):
    """Function to convert bytes to  KB, MB, GB, TB.

    :param num: number of bytes
    :type num: int
    :return: converted number
    :rtype: str
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """Function to return the file size.

    :param file_path: file path
    :type file_path: str
    :return: file size
    :rtype: str

    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)
    else:
        raise IOError('Could not find file: {}'.format(file_path))


def file_size_MB(file_path):
    """Function to return the file size in MB.

    :param file_path: file path
    :type file_path: str
    :return: file size in MB
    :rtype: float
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size / 1024.0 / 1024.0
    else:
        raise IOError('Could not find file: {}'.format(file_path))


def zip_file(file_to_zip, destination_archive=None, name_of_zipped_file=None):
    """Method to zip a single file as an archive.

    :param file_to_zip: path to the file to be zipped
    :type file_to_zip: str
    :param destination_archive: path to the archive to be created
    :type destination_archive: str
    :param name_of_zipped_file: name of the file inside the archive
    :type name_of_zipped_file: str
    :return: path to the ZIP-file
    :rtype: str
    """

    # Input assertions
    assert os.path.isfile(file_to_zip), "Path {} does not seem to refer to a file.".format(file_to_zip)
    if destination_archive:
        assert os.path.splitext(destination_archive)[1] == '.zip', \
            "destination_archive should end with .zip, now ends with: {}".format(os.path.splitext(destination_archive)[1])
    if name_of_zipped_file:
        assert isinstance(name_of_zipped_file, string_types), \
            "name_of_zipped_file should be a string, now {}.".format(type(name_of_zipped_file))

    # Zip file
    if destination_archive is None:
        destination_archive = str(os.path.splitext(file_to_zip)[0] + '.zip')
    if name_of_zipped_file is None:
        name_of_zipped_file = os.path.basename(file_to_zip)
    if os.path.exists(destination_archive):
        os.remove(destination_archive)
    zipfile.ZipFile(destination_archive, mode='w').write(file_to_zip, arcname=name_of_zipped_file)
    return destination_archive


def unzip_file(file_to_unzip, destination_folder=None):
    # Input assertions
    assert file_to_unzip.endswith('.zip'), \
        "file_to_unzip should end with .zip, now ends with: {}".format(os.path.splitext(file_to_unzip)[1])
    assert os.path.isfile(file_to_unzip), \
        "Path {} does not seem to refer to an existing zip-file.".format(file_to_unzip)

    # Unzip file
    if destination_folder is None:
        destination_folder = os.path.dirname(file_to_unzip)
    zip_ref = zipfile.ZipFile(file_to_unzip, 'r')
    assert len(zip_ref.filelist) == 1, "Only one file is expected in this ZIP-file with this function."
    extracted_file = os.path.join(destination_folder, zip_ref.filelist[0].filename)
    if os.path.exists(extracted_file):
        os.remove(extracted_file)
    zip_ref.extractall(destination_folder)
    zip_ref.close()
    return extracted_file


def unzip_folder(file_to_unzip, destination_folder=None, expected_file='VISTOMS.html'):
    # Input assertions
    assert file_to_unzip.endswith('.zip'), \
        "file_to_unzip should end with .zip, now ends with: {}".format(os.path.splitext(file_to_unzip)[1])
    assert os.path.isfile(file_to_unzip), \
        "Path {} does not seem to refer to an existing zip-file.".format(file_to_unzip)

    # Unzip file
    if destination_folder is None:
        destination_folder = os.path.dirname(file_to_unzip)
    zip_ref = zipfile.ZipFile(file_to_unzip, 'r')
    if expected_file:
        assert expected_file in [zip_ref_file.filename for zip_ref_file in zip_ref.filelist],\
            "Expected file {} not found in ZIP-file.".format(expected_file)
    zip_ref.extractall(destination_folder)
    zip_ref.close()
    return destination_folder


def make_float_or_keep_none(value):
    if isinstance(value, (float, int, string_types)):
        return float(value)
    elif value is None:
        return None
    else:
        raise AssertionError('Could not process value {} which is of type {}.'.format(value, type(value)))