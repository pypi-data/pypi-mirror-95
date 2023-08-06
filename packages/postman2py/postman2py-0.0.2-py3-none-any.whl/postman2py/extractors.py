import json
import ntpath
import magic
import os
from loguru import logger
from pathlib import Path

def extract_dict_from_raw_mode_data(raw):
    """extract json to dictionay

    :param raw: jsondata
    :return: :extracted dict
    """
    try:
        return json.loads(raw)
    except json.decoder.JSONDecodeError:
        return {}


def exctact_dict_from_files(data):
    """extract files from dict data.

    :param data: [{"key":"filename", "src":"relative/absolute path to file"}]
    :return: :tuple of file metadata for requests library
    """
    data['src'] = f"{os.getcwd()}/{data['src']}"
    if not Path(data['src']).exists():
        raise Exception(
            'File '+data['src']+' does not exist')

    mime = magic.Magic(mime=True)
    file_mime = mime.from_file(data['src'])
    file_name = ntpath.basename(data['src'])
    return (file_name, open(data['src'], 'rb'), file_mime, {
        'Content-Disposition': 'form-data; name="'+data['key']+'"; filename="' + file_name + '"',
        'Content-Type': file_mime})


def extract_dict_from_formdata_mode_data(formdata):
    data = {}
    files = {}
    try:
        for row in formdata:
            if row['type'] == "text":
                data[row['key']] = row['value']
            if row['type'] == "file":
                files[row['key']] = exctact_dict_from_files(row)
        return data, files
    except Exception as e:
        logger.error(f"extract from formdata_mode_data error occurred: {e}")
        return data, files


def extract_dict_from_raw_headers(raw):
    d = {}
    for header in raw.split('\n'):
        try:
            key, value = header.split(': ')
            d[key] = value
        except ValueError:
            continue

    return d


def extract_dict_from_headers(data):
    d = {}
    for header in data:
        try:
            if 'disabled' in header and header['disabled'] == True:
                continue
            d[header['key']] = header['value']
        except ValueError:
            continue

    return d


def extract_dict_from_urlencoded(data):
    body = {}
    if len(data['body']['urlencoded']) != 0:
        for entry in data['body']['urlencoded']:
            for k, v in entry.items():
                body[entry['key']] = entry['value']
    return body


def format_object(o, key_values):
    if isinstance(o, str):
        try:
            return o.replace('{{', '{').replace('}}', '}').format(**key_values)
        except KeyError as e:
            raise KeyError(
                "Except value %s in PostPython environment variables.\n Environment variables are %s" % (e, key_values))
    elif isinstance(o, dict):
        return format_dict(o, key_values)
    elif isinstance(o, list):
        return [format_object(oo, key_values) for oo in o]
    elif isinstance(o, object):
        return o


def format_dict(d, key_values):
    kwargs = {}
    for k, v in d.items():
        kwargs[k] = format_object(v, key_values)
    return kwargs
