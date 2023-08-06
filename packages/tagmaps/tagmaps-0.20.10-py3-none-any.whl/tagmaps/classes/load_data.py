# -*- coding: utf-8 -*-

"""Module for loading data

Returns:
    cleanedPost: a subset of the original available
                 post attributes
                 that is needed for Tag Maps clustering
"""

from __future__ import absolute_import

import csv
import json
import logging
import sys
from decimal import Decimal
from typing import (IO, Any, Dict, Iterable, Iterator, Optional, OrderedDict,
                    Set, Tuple)

from shapely.geometry import Point

from tagmaps.classes.shared_structure import AnalysisBounds, PostStructure
from tagmaps.classes.utils import Utils


class LoadData():
    """Main Class for ingesting data

    - will apply basic filters (based on stoplists etc.)
    - Returns CleanedPost
    """

    def __init__(
            self, cfg, user_variety_input=None,
            console_reporting=None):
        """Initializes Load Data structure"""
        if user_variety_input is None:
            user_variety_input = False
        if console_reporting is None:
            console_reporting = False
        self.filelist = self._read_local_files(cfg)
        self.guid_hash = set()  # global list of guids
        self.append_to_already_exist = False  # unused?
        self.shape_exclude_locid_hash = set()
        self.shape_included_locid_hash = set()
        self.filter_origin = cfg.filter_origin
        self.cfg = cfg
        self.console_reporting = console_reporting
        self.log = logging.getLogger("tagmaps")
        self.bounds = AnalysisBounds()
        self.distinct_locations_set = set()
        self.ignore_empty_latlng = False
        self.current_file = None
        # basic statistics collection
        self.stats = DataStats()
        if user_variety_input:
            # get user input for max tags to process
            # this is combined here with output reporting
            # of how many files to process
            # the user can start loading data with enter, or
            # by adding a number (e.g. 100), which will
            # later be used to remove the long tail for tags/emoji
            self._get_imax()

    def __enter__(self):
        """Main pipeline for reading posts from file

        Combine multiple generators to single pipeline
        that is returned for being processed by
        with-statement.
        """
        post_pipeline = self._parse_postlist(
            self._process_inputfile(
                self._parse_input_files(count=True)))
        return post_pipeline

    def __exit__(self, c_type, value, traceback):
        """Contextmanager exit: nothing to do here"""
        return False

    def _parse_input_files(self, count: bool = None) -> Iterator[IO[str]]:
        """Loops input input filelist and
        returns opened file handles
        """
        for file_name in self.filelist:
            if count:
                self.stats.partcount += 1
            self.current_file = file_name.stem
            yield open(file_name, 'r', newline='', encoding='utf8')

    def is_intermediate(self):
        """Auto test if intermediate data is present"""
        post_reader = next(self._process_inputfile(
            self._parse_input_files(
                count=False)))
        for post in post_reader:
            pguid = post.get(self.cfg.source_map.post_guid_col)
            if pguid is None and post.get("guid") is not None:
                # if column name is "guid",
                # data is likely of type intermediate
                self.log.info(
                    "Intermediate data detected.. skipping filtering step.\n")
                return True
            return False

    def _process_inputfile(
            self, file_handles: Iterator[IO[str]]) -> Iterator[Any]:
        """File parse for CSV or JSON from open file handle

        Output: produces a list of post that can be parsed
        """
        post_reader = []
        for file_handle in file_handles:
            if self.cfg.source_map.file_extension == "csv":
                post_reader = csv.DictReader(
                    file_handle,
                    delimiter=self.cfg.source_map.delimiter,
                    quotechar=self.cfg.source_map.quote_char,
                    quoting=self.cfg.source_map.quoting)
                # next(post_list, None)  # skip headerline
            elif self.cfg.source_map.file_extension == "json":
                post_reader = post_reader + json.loads(
                    file_handle.read())
            yield post_reader

    def _parse_postlist(
            self, post_readers: Iterable[OrderedDict[str, Optional[str]]]):
        """Process posts according to specifications

        Returns generator for single record
        """
        # row_num = 0
        msg = None
        for post_reader in post_readers:
            Utils.check_fileheader(
                post_reader.fieldnames, self.cfg.source_map, self.current_file)
            for post in post_reader:
                # row_num += 1
                lbsn_post = self._parse_post(post)
                if lbsn_post is None:
                    continue
                else:
                    self.stats.count_glob += 1
                    msg = self._report_progress()
                    # if (row_num % 10 == 0):
                    # modulo: print only once every 10 iterations
                    if self.console_reporting:
                        print(msg, end='\r')
                yield lbsn_post
        # log last message to file, clean stdout
        if msg and self.console_reporting:
            print(" " * len(msg), end='\r')
        sys.stdout.flush()
        if self.stats.count_glob == 0:
            raise ValueError(
                f"No posts found in input data. "
                f"First file: {next(iter(self.filelist or []), None)}.")
        self.log.info(msg)

    def _report_progress(self):
        """Status report"""
        msg = (
            f'Cleaned input to {len(self.distinct_locations_set):02d} '
            f'distinct locations from '
            f'{self.stats.count_glob:02d} posts '
            f'(File {self.stats.partcount} of {len(self.filelist)}) - '
            f'Skipped posts: {self.stats.skipped_count} - skipped tags: '
            f'{self.stats.count_tags_skipped} of '
            f'{self.stats.count_tags_global}')
        return msg

    def _parse_post(self, post: Dict[str, str]) -> Optional[PostStructure]:
        """Process single post and attach to common structure"""
        # skip duplicates and erroneous entries
        post_guid = post.get(self.cfg.source_map.post_guid_col)
        if post_guid in self.guid_hash:
            self.stats.skipped_count += 1
            return None
        if post_guid is None:
            raise ValueError(f"Post guid is None: {post}")
        self.guid_hash.add(post_guid)
        origin_id = post.get(self.cfg.source_map.originid_col)
        if origin_id is None:
            origin_id = 0
        if (self.filter_origin and
                not origin_id == self.filter_origin):
            # optional exclude origin
            self.stats.skipped_count += 1
            return None
        user_guid = post.get(self.cfg.source_map.user_guid_col)
        if user_guid is None:
            raise ValueError(f"User guid is None: {post}")
        if not self.cfg.ignore_stoplists and \
                self.cfg.sort_out_user_set is not None \
                and user_guid in self.cfg.sort_out_user_set:
            return None
        # Continue Parse Post
        lbsn_post = PostStructure(
            origin_id=int(origin_id), guid=post_guid, user_guid=user_guid)
        lbsn_post.post_url = post.get(self.cfg.source_map.post_url_col)
        lbsn_post.post_publish_date = \
            post.get(self.cfg.source_map.post_publish_date_col)
        # Process Spatial Query first (if skipping necessary)
        if self.cfg.sort_out_places and \
                self._is_sortout_place(post):
            return None
        lat = None
        lng = None
        if self._is_empty_latlng(post):
            if self.ignore_empty_latlng:
                pass
            else:
                return None
        else:
            # assign lat/lng coordinates from dict
            lat, lng = self._correct_placelatlng(
                post.get(self.cfg.source_map.place_guid_col),
                post.get(self.cfg.source_map.latitude_col),
                post.get(self.cfg.source_map.longitude_col)
            )
            # update boundary
            self.bounds.upd_latlng_bounds(lat, lng)
            lbsn_post.latitude = lat
            lbsn_post.longitude = lng
        if lat is None or lng is None:
            # Try to substitude place_guid
            # if self.ignore_empty_latlng has been set to True
            lbsn_post.loc_id = post.get(
                self.cfg.source_map.place_guid_col)
            if not lbsn_post.loc_id:
                self.log.warning('Neither coordinates nor place guid found.')
        else:
            # Note: loc_id not loaded from file
            # create loc_id from lat/lng
            lbsn_post.loc_id = f'{lat}:{lng}'
        # counting of distinct loc ids
        self.distinct_locations_set.add(lbsn_post.loc_id)
        lbsn_post.loc_name = post.get(self.cfg.source_map.place_name_col)
        # exclude posts outside boundary
        if (self.cfg.shapefile_intersect or self.cfg.shapefile_exclude) and \
                self._is_outside_shapebounds(lbsn_post) is True:
            return None
        if self.cfg.cluster_tags or \
                self.cfg.cluster_emoji or \
                self.cfg.topic_modeling:
            post_body = post.get(self.cfg.source_map.post_body_col)
            post_title = post.get(self.cfg.source_map.post_title_col)
            if self.cfg.ignore_stoplists:
                lbsn_post.post_body = post_body
                lbsn_post.post_title = post_title
            else:
                if self.cfg.select_tags_set is not None:
                    # if positive filterlist available
                    lbsn_post.post_body = Utils.select_words(
                        post_body, self.cfg.select_tags_set)
                    lbsn_post.post_title = Utils.select_words(
                        post_title, self.cfg.select_tags_set)
                else:
                    # check against stoplists
                    lbsn_post.post_body = Utils.remove_stopwords(
                        post_body, self.cfg.sort_out_always_set)
                    lbsn_post.post_title = Utils.remove_stopwords(
                        post_title, self.cfg.sort_out_always_set)
        else:
            lbsn_post.post_title = ""
            lbsn_post.post_body = ""
        lbsn_post.post_like_count = self._get_count_frompost(
            post.get(self.cfg.source_map.post_like_count_col))
        lbsn_post.hashtags = set()
        if self.cfg.cluster_tags or self.cfg.topic_modeling:
            lbsn_post.hashtags = self._get_tags(
                post.get(self.cfg.source_map.tags_col))
        if self.cfg.cluster_emoji:
            lbsn_post.emoji = self._get_emoji(lbsn_post.post_body)
            # no merge anymore:
            # lbsn_post.hashtags = set.union(post_emoji)
        lbsn_post.post_create_date = \
            post.get(self.cfg.source_map.post_create_date_col)
        lbsn_post.post_views_count = self._get_count_frompost(
            post.get(self.cfg.source_map.post_views_count_col))
        # return parsed post object
        return lbsn_post

    @staticmethod
    def _read_local_files(config):
        """Read Local Files according to config parameters

        - returns list of file-paths
        """
        input_path = config.input_folder
        filelist = list(input_path.glob(
            f'*.{config.source_map.file_extension}'))
        input_count = len(filelist)
        if input_count == 0:
            raise ValueError(
                f'No input files *.'
                f'{config.source_map.file_extension} '
                f'in ./{input_path.name}/ found.')
        return filelist

    @staticmethod
    def _get_count_frompost(count_string: Optional[str]) -> int:
        """Parse post like count field"""
        if count_string and not count_string == "":
            try:
                photo_likes_int = int(count_string)
                return photo_likes_int
            except TypeError:
                logging.getLogger("tagmaps").debug(
                    f'\nPost like count parser: Type Error: '
                    f'{type(count_string)} not a valid number format '
                    f'Returning 0.')
            except ValueError:
                logging.getLogger("tagmaps").debug(
                    f'\nPost like count parser: Value Error: '
                    f'{count_string} not a valid number. '
                    f'Returning 0.')
        return 0

    def _get_emoji(self, post_body: Optional[str]) -> Set[str]:
        """extract emoji, use selection list if available"""
        emoji_filtered = Utils.select_emoji(
            Utils.extract_emoji(post_body), self.cfg.select_emoji_set)
        if emoji_filtered:
            self.stats.count_emojis_global += len(emoji_filtered)
        return emoji_filtered

    def _get_tags(self, tags_string: Optional[str]) -> Set[str]:
        """extract tags, apply filter lists if available"""
        # base str conversion to set
        tags = set(filter(None, tags_string.lower().split(";")))
        # Filter tags based on two stoplists
        if self.cfg.ignore_stoplists:
            count_tags = len(tags)
            count_skipped = 0
        else:
            tags, count_tags, count_skipped = \
                Utils.filter_tags(
                    tags,
                    self.cfg.sort_out_always_set,
                    self.cfg.sort_out_always_instr_set,
                    self.cfg.select_tags_set
                )
        # update global stats
        self.stats.count_tags_global += count_tags
        self.stats.count_tags_skipped += count_skipped
        return tags

    def _correct_placelatlng(
            self, place_guid_string: Optional[str], lat, lng) -> Tuple[Decimal, Decimal]:
        """If place corrections available, update lat/lng coordinates
        Needs test: not place_guid_string
        """
        if (self.cfg.correct_places and not place_guid_string and
                place_guid_string in self.cfg.correct_place_latlng_dict):
            lat = Decimal(
                # correct lat
                self.cfg.correct_place_latlng_dict[place_guid_string][0])
            lng = Decimal(
                # correct lng
                self.cfg.correct_place_latlng_dict[place_guid_string][1])
        else:
            # return original lat/lng
            lat = Decimal(lat)  # original lat
            lng = Decimal(lng)  # original lng
        return lat, lng

    def _is_outside_shapebounds(self, post):
        """Skip all posts outside shapefile """
        # do not expensive spatial check twice:
        if post.loc_id in self.shape_exclude_locid_hash:
            self.stats.skipped_count += 1
            return True
        if post.loc_id not in self.shape_included_locid_hash:
            lng_lat_point = Point(post.longitude, post.latitude)
            if Utils.check_intersect_polylist(
                    lng_lat_point, self.cfg.shapefile_intersect,
                    self.cfg.shapefile_exclude) is False:
                self.stats.skipped_count += 1
                self.shape_exclude_locid_hash.add(post.loc_id)
                return True
            self.shape_included_locid_hash.add(post.loc_id)
        return False

    def _is_empty_latlng(self, post):
        """ skip non-geotagged medias"""
        latitude = post.get(self.cfg.source_map.latitude_col)
        longitude = post.get(self.cfg.source_map.longitude_col)
        if not latitude or not longitude:
            self.stats.count_non_geotagged += 1
            return True
        return False

    def _is_sortout_place(self, post):
        """Returns False if place of post is in ignore list"""
        place_guid = post.get(self.cfg.source_map.place_guid_col)
        if place_guid:
            if place_guid in self.cfg.sort_out_places_set:
                self.stats.skipped_count += 1
                return True
        return False

    def _get_imax(self):
        """User Input to get number of tags to process"""
        if self.cfg.auto_mode:
            return
        if self.cfg.cluster_tags or self.cfg.cluster_emoji:
            inputtext = \
                input(f'Files to process: {len(self.filelist)}. \nOptional: '
                      f'Enter a Number for the variety of tags to process '
                      f'(default is 1000)\nPress Enter to proceed.. \n')
            if inputtext is None \
                    or inputtext == "" \
                    or not inputtext.isdigit():
                return
            self.cfg.max_items = int(inputtext)

    def input_stats_report(self):
        """Return input stats"""
        self.log.info(
            f'\nTotal post count (PC): '
            f'{self.stats.count_glob:02d}')
        self.log.info(
            f'Total tag count (PTC): '
            f'{self.stats.count_tags_global}')
        self.log.info(
            f'Total emoji count (PEC): '
            f'{self.stats.count_emojis_global}')


class DataStats():
    """Class storing basic data stats"""

    def __init__(self):
        """Initialize stats."""
        self.count_glob = 0
        self.partcount = 0
        self.skipped_count = 0
        self.count_non_geotagged = 0
        self.count_outside_shape = 0
        self.count_tags_global = 0
        self.count_emojis_global = 0
        self.count_tags_skipped = 0
