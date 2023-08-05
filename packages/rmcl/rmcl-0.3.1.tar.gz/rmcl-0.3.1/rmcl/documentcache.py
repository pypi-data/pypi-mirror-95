# Copyright 2020-2021 Robert Schroll
# This file is part of rmcl and is distributed under the MIT license.

_cached_key = None
_cached_value = None

def get_document(id_, version, form):
    if (id_, version, form) == _cached_key:
        return _cached_value
    return None

def set_document(id_, version, form, document):
    global _cached_key, _cached_value
    _cached_key = (id_, version, form)
    _cached_value = document
