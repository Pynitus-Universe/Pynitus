"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

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

from src.Data.Track.Track import Track


class FileTrack(Track):
    """
    A Track which uses a local file as it's source
    """

    description = "A Local File"

    def __init__(self, location, title: str, artist: str, album: str):
        super().__init__(location, title, artist, album)

        self.playback_handler_class  # = PlaybackHandler
        self.playback_handler_instance = None  # TODO: Move to central PlaybackHandler
        self.delegate = None

    def available(self):
        return True  # TODO
