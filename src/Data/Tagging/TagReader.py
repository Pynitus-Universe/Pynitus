"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Vivian Franz, Noah Hummel

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import taglib
from typing import Dict, List, Any, TypeVar

from src.Data.Tagging import TagSupport

Strings = TypeVar("Strings", str, List[str], None)


def __cleanAttribute(tag_name: str, tag_value: Any) -> TagSupport.TagValue:  # TODO: refactor for readability
    """
    Performs strong type checking on a previously read attribute and tries to convert it's type
    into the desired type according to TagSupport.
    If the attribute cannot be converted to the right type, the appropriate empty value for
    the attribute is returned (None for non list-type attributes, [] for list-type attributes).

    :param tag_name: The Taglib ID of the attribute
    :param tag_value: The attribute's value
    :return: The safe-to-use tag_value of the right type
    """

    def __cleanStrings(strings_or_string):
        """
        TODO
        :param strings_or_string:
        :return:
        """

        def __cleanString(string):
            if string in TagSupport.EMPTY_SYNONYMS:
                return None
            return string

        if type(strings_or_string) == str:
            return __cleanString(strings_or_string)
        else:
            return [__cleanString(s) for s in strings_or_string]

    tag_primitive_type = TagSupport.getPrimitiveType(tag_name)

    if TagSupport.isListType(tag_name):  # Should this attribute be represented as a list?

        if type(tag_value) is list:  # Is it actually a list?
            if not all(type(value) is tag_primitive_type for value in tag_value):  # Some entries have the wrong type
                try:
                    tag_value = [tag_primitive_type(e) for e in tag_value]  # Try to fix those entries naively
                except Exception:  # The entries couldn't be fixed
                    tag_value = []  # Throw the corrupted data away.

        elif tag_value is not None:  # The tag wasn't a list, but maybe it's still of the right type...
            if type(tag_value) is not tag_primitive_type:  # The type is wrong, try to cast the type naively...
                try:
                    tag_value = [tag_primitive_type(tag_value)]
                except Exception:
                    tag_value = []
        else:  # tag_value is None, but list-types should be [] if no data is given
            tag_value = []

    else:  # attribute shouldn't be a list.
        if type(tag_value) is list:  # if it's a list though (taglib does this...)...
            if len(tag_value) > 0:  # ... then maybe the first element is usable.
                tag_value = tag_value[0]

        # check the type
        if not type(tag_value) is tag_primitive_type: # The type is wrong, try to cast the type naively...
            try:
                tag_value = tag_primitive_type(tag_value)
            except Exception:
                tag_value = None

    if tag_primitive_type is str:
        tag_value = __cleanStrings(tag_value)

    return tag_value


def writeTag(file_path: str, tags: Dict[str, List[str]]) -> None:
    """
    Writes given Information to Tag assuming that it is defined in TagSupport
    :param file_path: Path of Media File to writes Tags
    :param tags: tag Keys and Values
    :return: None
    """
    audio_file = taglib.File(file_path)
    audio_file.tags.update(tags)
    audio_file.save()
    audio_file.close()


def readTag(file_path: str) -> Dict[str, any]:
    """
    Returns selected Tag Information defined in TagSupport
    :param file_path: Path to Media File to read Tags of
    :return: Dict with filled Tag Information given by Track and selected by TAGLIB_INTERNAL_NAMES
    """
    audio_file = taglib.File(file_path)

    tags = dict(audio_file.tags)
    tags["LENGTH"] = [str(audio_file.length)]  # Fix to make taglib behave consistently with TagSupport
    # writeTag(file_path, tags)

    clean_tags = dict({})

    for tag_name in TagSupport.TAGLIB_IDENTIFIERS:  # Fill all supported attribute fields
        # Strong type checking to avoid data corruption, this stuff will end up in the db!
        clean_tags[TagSupport.getInternalName(tag_name)] = __cleanAttribute(tag_name, tags.get(tag_name))

    return clean_tags
