""" Custom template system for osxphotos (implemented in PhotoInfo.render_template) """


# Rolled my own template system because:
# 1. Needed to handle multiple values (e.g. album, keyword)
# 2. Needed to handle default values if template not found
# 3. Didn't want user to need to know python (e.g. by using Mako which is
#    already used elsewhere in this project)
#
# This code isn't elegant and is prime for refactoring but it seems to work well.  PRs gladly accepted.

import datetime
import locale
import os
import pathlib
import re
from functools import partial

from ._constants import _UNKNOWN_PERSON
from .datetime_formatter import DateTimeFormatter
from .exiftool import ExifTool
from .path_utils import sanitize_dirname, sanitize_filename, sanitize_pathpart

# ensure locale set to user's locale
locale.setlocale(locale.LC_ALL, "")

PHOTO_VIDEO_TYPE_DEFAULTS = {"photo": "photo", "video": "video"}

MEDIA_TYPE_DEFAULTS = {
    "selfie": "selfie",
    "time_lapse": "time_lapse",
    "panorama": "panorama",
    "slow_mo": "slow_mo",
    "screenshot": "screenshot",
    "portrait": "portrait",
    "live_photo": "live_photo",
    "burst": "burst",
    "photo": "photo",
    "video": "video",
}

# Permitted substitutions (each of these returns a single value or None)
TEMPLATE_SUBSTITUTIONS = {
    "{name}": "Current filename of the photo",
    "{original_name}": "Photo's original filename when imported to Photos",
    "{title}": "Title of the photo",
    "{descr}": "Description of the photo",
    "{media_type}": (
        f"Special media type resolved in this precedence: {', '.join(t for t in MEDIA_TYPE_DEFAULTS)}. "
        "Defaults to 'photo' or 'video' if no special type. "
        "Customize one or more media types using format: '{media_type,video=vidéo;time_lapse=vidéo_accélérée}'"
    ),
    "{photo_or_video}": "'photo' or 'video' depending on what type the image is. To customize, use default value as in '{photo_or_video,photo=fotos;video=videos}'",
    "{hdr}": "Photo is HDR?; True/False value, use in format '{hdr?VALUE_IF_TRUE,VALUE_IF_FALSE}'",
    "{edited}": "Photo has been edited (has adjustments)?; True/False value, use in format '{edited?VALUE_IF_TRUE,VALUE_IF_FALSE}'",
    "{created.date}": "Photo's creation date in ISO format, e.g. '2020-03-22'",
    "{created.year}": "4-digit year of photo creation time",
    "{created.yy}": "2-digit year of photo creation time",
    "{created.mm}": "2-digit month of the photo creation time (zero padded)",
    "{created.month}": "Month name in user's locale of the photo creation time",
    "{created.mon}": "Month abbreviation in the user's locale of the photo creation time",
    "{created.dd}": "2-digit day of the month (zero padded) of photo creation time",
    "{created.dow}": "Day of week in user's locale of the photo creation time",
    "{created.doy}": "3-digit day of year (e.g Julian day) of photo creation time, starting from 1 (zero padded)",
    "{created.hour}": "2-digit hour of the photo creation time",
    "{created.min}": "2-digit minute of the photo creation time",
    "{created.sec}": "2-digit second of the photo creation time",
    "{created.strftime}": "Apply strftime template to file creation date/time. Should be used in form "
    + "{created.strftime,TEMPLATE} where TEMPLATE is a valid strftime template, e.g. "
    + "{created.strftime,%Y-%U} would result in year-week number of year: '2020-23'. "
    + "If used with no template will return null value. "
    + "See https://strftime.org/ for help on strftime templates.",
    "{modified.date}": "Photo's modification date in ISO format, e.g. '2020-03-22'; uses creation date if photo is not modified",
    "{modified.year}": "4-digit year of photo modification time; uses creation date if photo is not modified",
    "{modified.yy}": "2-digit year of photo modification time; uses creation date if photo is not modified",
    "{modified.mm}": "2-digit month of the photo modification time (zero padded); uses creation date if photo is not modified",
    "{modified.month}": "Month name in user's locale of the photo modification time; uses creation date if photo is not modified",
    "{modified.mon}": "Month abbreviation in the user's locale of the photo modification time; uses creation date if photo is not modified",
    "{modified.dd}": "2-digit day of the month (zero padded) of the photo modification time; uses creation date if photo is not modified",
    "{modified.dow}": "Day of week in user's locale of the photo modification time; uses creation date if photo is not modified",
    "{modified.doy}": "3-digit day of year (e.g Julian day) of photo modification time, starting from 1 (zero padded); uses creation date if photo is not modified",
    "{modified.hour}": "2-digit hour of the photo modification time; uses creation date if photo is not modified",
    "{modified.min}": "2-digit minute of the photo modification time; uses creation date if photo is not modified",
    "{modified.sec}": "2-digit second of the photo modification time; uses creation date if photo is not modified",
    "{modified.strftime}": "Apply strftime template to file modification date/time. Should be used in form "
    + "{modified.strftime,TEMPLATE} where TEMPLATE is a valid strftime template, e.g. "
    + "{modified.strftime,%Y-%U} would result in year-week number of year: '2020-23'. "
    + "If used with no template will return null value. Uses creation date if photo is not modified. "
    + "See https://strftime.org/ for help on strftime templates.",
    "{today.date}": "Current date in iso format, e.g. '2020-03-22'",
    "{today.year}": "4-digit year of current date",
    "{today.yy}": "2-digit year of current date",
    "{today.mm}": "2-digit month of the current date (zero padded)",
    "{today.month}": "Month name in user's locale of the current date",
    "{today.mon}": "Month abbreviation in the user's locale of the current date",
    "{today.dd}": "2-digit day of the month (zero padded) of current date",
    "{today.dow}": "Day of week in user's locale of the current date",
    "{today.doy}": "3-digit day of year (e.g Julian day) of current date, starting from 1 (zero padded)",
    "{today.hour}": "2-digit hour of the current date",
    "{today.min}": "2-digit minute of the current date",
    "{today.sec}": "2-digit second of the current date",
    "{today.strftime}": "Apply strftime template to current date/time. Should be used in form "
    + "{today.strftime,TEMPLATE} where TEMPLATE is a valid strftime template, e.g. "
    + "{today.strftime,%Y-%U} would result in year-week number of year: '2020-23'. "
    + "If used with no template will return null value. "
    + "See https://strftime.org/ for help on strftime templates.",
    "{place.name}": "Place name from the photo's reverse geolocation data, as displayed in Photos",
    "{place.country_code}": "The ISO country code from the photo's reverse geolocation data",
    "{place.name.country}": "Country name from the photo's reverse geolocation data",
    "{place.name.state_province}": "State or province name from the photo's reverse geolocation data",
    "{place.name.city}": "City or locality name from the photo's reverse geolocation data",
    "{place.name.area_of_interest}": "Area of interest name (e.g. landmark or public place) from the photo's reverse geolocation data",
    "{place.address}": "Postal address from the photo's reverse geolocation data, e.g. '2007 18th St NW, Washington, DC 20009, United States'",
    "{place.address.street}": "Street part of the postal address, e.g. '2007 18th St NW'",
    "{place.address.city}": "City part of the postal address, e.g. 'Washington'",
    "{place.address.state_province}": "State/province part of the postal address, e.g. 'DC'",
    "{place.address.postal_code}": "Postal code part of the postal address, e.g. '20009'",
    "{place.address.country}": "Country name of the postal address, e.g. 'United States'",
    "{place.address.country_code}": "ISO country code of the postal address, e.g. 'US'",
    "{searchinfo.season}": "Season of the year associated with a photo, e.g. 'Summer'; (Photos 5+ only, applied automatically by Photos' image categorization algorithms).",
    "{exif.camera_make}": "Camera make from original photo's EXIF information as imported by Photos, e.g. 'Apple'",
    "{exif.camera_model}": "Camera model from original photo's EXIF information as imported by Photos, e.g. 'iPhone 6s'",
    "{exif.lens_model}": "Lens model from original photo's EXIF information as imported by Photos, e.g. 'iPhone 6s back camera 4.15mm f/2.2'",
    "{uuid}": "Photo's internal universally unique identifier (UUID) for the photo, a 36-character string unique to the photo, e.g. '128FB4C6-0B16-4E7D-9108-FB2E90DA1546'",
}

# Permitted multi-value substitutions (each of these returns None or 1 or more values)
TEMPLATE_SUBSTITUTIONS_MULTI_VALUED = {
    "{album}": "Album(s) photo is contained in",
    "{folder_album}": "Folder path + album photo is contained in. e.g. 'Folder/Subfolder/Album' or just 'Album' if no enclosing folder",
    "{keyword}": "Keyword(s) assigned to photo",
    "{person}": "Person(s) / face(s) in a photo",
    "{label}": "Image categorization label associated with a photo (Photos 5+ only)",
    "{label_normalized}": "All lower case version of 'label' (Photos 5+ only)",
    "{comment}": "Comment(s) on shared Photos; format is 'Person name: comment text' (Photos 5+ only)",
    "{exiftool:GROUP:TAGNAME}": "Use exiftool (https://exiftool.org) to extract metadata, in form GROUP:TAGNAME, from image.  "
    "E.g. '{exiftool:EXIF:Make}' to get camera make, or {exiftool:IPTC:Keywords} to extract keywords. "
    "See https://exiftool.org/TagNames/ for list of valid tag names.  You must specify group (e.g. EXIF, IPTC, etc) "
    "as used in `exiftool -G`. exiftool must be installed in the path to use this template.",
    "{searchinfo.holiday}": "Holiday names associated with a photo, e.g. 'Christmas Day'; (Photos 5+ only, applied automatically by Photos' image categorization algorithms).",
    "{searchinfo.activity}": "Activities associated with a photo, e.g. 'Sporting Event'; (Photos 5+ only, applied automatically by Photos' image categorization algorithms).",
    "{searchinfo.venue}": "Venues associated with a photo, e.g. name of restaurant; (Photos 5+ only, applied automatically by Photos' image categorization algorithms).",
    "{searchinfo.venue_type}": "Venue types associated with a photo, e.g. 'Restaurant'; (Photos 5+ only, applied automatically by Photos' image categorization algorithms).",
}

# Just the multi-valued substitution names without the braces
MULTI_VALUE_SUBSTITUTIONS = [
    field.replace("{", "").replace("}", "")
    for field in TEMPLATE_SUBSTITUTIONS_MULTI_VALUED
]

# regular expressions for matching template syntax
RE_OPENING_BRACE = r"(?<!\{)\{"  # match { but not {{
RE_DELIM = r"([^}]*\+)?"  # group 1: optional DELIM+
RE_FIELD_NAME = r"([^\\,}+\?]+)"  # group 2: field name
RE_PATH_SEP = r"(\([^{}\)]*\))?"  # group 3: optional (PATH_SEP)
# + r"(\[[^{}\)]*\])?"  # group 4: optional [REPLACE]
RE_REPLACE = r"(\[[^{}]*\])?"  # group 4: optional [REPLACE]
RE_BOOL_VAL = r"(\?[^\\,}]*)?"  # group 5: optional ?TRUE_VALUE for boolean fields
RE_DEFAULT_VAL = r"(,[\w\=\;\-\%. ]*)?"  # group 6: optional ,DEFAULT
RE_CLOSING_BRACE = r"(?=\}(?!\}))\}"  # match } but not }}

MATCH_GROUPS_TOTAL = 6
MATCH_GROUPS_DELIM = 1
MATCH_GROUPS_FIELD = 2
MATCH_GROUPS_PATH_SEP = 3
MATCH_GROUPS_REPLACE = 4
MATCH_GROUPS_BOOL_VAL = 5
MATCH_GROUPS_DEFAULT = 6

# default values for string manipulation template options
INPLACE_DEFAULT = ","
PATH_SEP_DEFAULT = os.path.sep


class PhotoTemplate:
    """ PhotoTemplate class to render a template string from a PhotoInfo object """

    def __init__(self, photo, exiftool_path=None):
        """ Inits PhotoTemplate class with photo

        Args:
            photo: a PhotoInfo instance.
            exiftool_path: optional path to exiftool for use with {exiftool:} template; if not provided, will look for exiftool in $PATH
        """
        self.photo = photo
        self.exiftool_path = exiftool_path

        # holds value of current date/time for {today.x} fields
        # gets initialized in get_template_value
        self.today = None

    def make_subst_function(self, none_str, filename, dirname, get_func=None):
        """ returns: substitution function for use in re.sub 
            none_str: value to use if substitution lookup is None and no default provided
            get_func: function that gets the substitution value for a given template field
                    default is get_template_value which handles the single-value fields """

        if get_func is None:
            # used by make_subst_function to get the value for a template substitution
            get_func = partial(
                self.get_template_value, filename=filename, dirname=dirname
            )

        # closure to capture photo, none_str, filename, dirname in subst
        def subst(matchobj):
            groups = len(matchobj.groups())
            if groups != MATCH_GROUPS_TOTAL:
                raise ValueError(
                    f"Unexpected number of groups: expected {MATCH_GROUPS_TOTAL}, got {groups}"
                )

            delim = matchobj.group(MATCH_GROUPS_DELIM)
            field = matchobj.group(MATCH_GROUPS_FIELD)
            path_sep = matchobj.group(MATCH_GROUPS_PATH_SEP)
            replace = matchobj.group(MATCH_GROUPS_REPLACE)
            bool_val = matchobj.group(MATCH_GROUPS_BOOL_VAL)
            default = matchobj.group(MATCH_GROUPS_DEFAULT)

            # drop the '+' on delim
            delim = delim[:-1] if delim is not None else None
            # drop () from path_sep
            path_sep = path_sep.strip("()") if path_sep is not None else None
            # drop [] from replace
            replace = replace[1:-1] if replace is not None else None
            # drop the ? on bool_val
            bool_val = bool_val[1:] if bool_val is not None else None
            # drop the comma on default
            default_val = default[1:] if default is not None else None

            try:
                val = get_func(
                    field, default_val, bool_val, delim, path_sep, replacement=replace
                )
            except ValueError:
                return matchobj.group(0)

            if val is None:
                # field valid but didn't match a value
                if default == ",":
                    val = ""
                else:
                    val = default_val if default_val is not None else none_str

            return val

        return subst

    def render(
        self,
        template,
        none_str="_",
        path_sep=None,
        expand_inplace=False,
        inplace_sep=None,
        filename=False,
        dirname=False,
        strip=False,
    ):
        """ Render a filename or directory template 

        Args:
            template: str template 
            none_str: str to use default for None values, default is '_' 
            path_sep: optional string to use as path separator, default is os.path.sep
            expand_inplace: expand multi-valued substitutions in-place as a single string 
                instead of returning individual strings
            inplace_sep: optional string to use as separator between multi-valued keywords
            with expand_inplace; default is ','
            filename: if True, template output will be sanitized to produce valid file name
            dirname: if True, template output will be sanitized to produce valid directory name 
            strip: if True, strips leading/trailing whitespace from rendered templates

        Returns:
            ([rendered_strings], [unmatched]): tuple of list of rendered strings and list of unmatched template values
        """

        if path_sep is None:
            path_sep = PATH_SEP_DEFAULT

        if inplace_sep is None:
            inplace_sep = INPLACE_DEFAULT

        # the rendering happens in two phases:
        # phase 1: handle all the single-value template substitutions
        #          results in a single string with all the template fields replaced
        # phase 2: loop through all the multi-value template substitutions
        #          could result in multiple strings
        #          e.g. if template is "{album}/{person}" and there are 2 albums and 3 persons in the photo
        #          there would be 6 possible renderings (2 albums x 3 persons)

        # regex to find {template_field,optional_default} in strings
        # pylint: disable=anomalous-backslash-in-string
        regex = (
            RE_OPENING_BRACE
            + RE_DELIM
            + RE_FIELD_NAME
            + RE_PATH_SEP
            + RE_REPLACE
            + RE_BOOL_VAL
            + RE_DEFAULT_VAL
            + RE_CLOSING_BRACE
        )

        if type(template) is not str:
            raise TypeError(f"template must be type str, not {type(template)}")

        subst_func = self.make_subst_function(none_str, filename, dirname)

        # do the replacements
        rendered = re.sub(regex, subst_func, template)

        # do multi-valued placements
        # start with the single string from phase 1 above then loop through all
        # multi-valued fields and all values for each of those fields
        # rendered_strings will be updated as each field is processed
        # for example: if two albums, two keywords, and one person and template is:
        # "{created.year}/{album}/{keyword}/{person}"
        # rendered strings would do the following:
        # start (created.year filled in phase 1)
        #   ['2011/{album}/{keyword}/{person}']
        # after processing albums:
        #   ['2011/Album1/{keyword}/{person}',
        #    '2011/Album2/{keyword}/{person}',]
        # after processing keywords:
        #   ['2011/Album1/keyword1/{person}',
        #    '2011/Album1/keyword2/{person}',
        #    '2011/Album2/keyword1/{person}',
        #    '2011/Album2/keyword2/{person}',]
        # after processing person:
        #   ['2011/Album1/keyword1/person1',
        #    '2011/Album1/keyword2/person1',
        #    '2011/Album2/keyword1/person1',
        #    '2011/Album2/keyword2/person1',]

        rendered_strings = self._render_multi_valued_templates(
            rendered, none_str, path_sep, expand_inplace, inplace_sep, filename, dirname
        )

        # process exiftool: templates
        rendered_strings = self._render_exiftool_template(
            rendered_strings,
            none_str,
            path_sep,
            expand_inplace,
            inplace_sep,
            filename,
            dirname,
        )

        # find any {fields} that weren't replaced
        unmatched = []
        for rendered_str in rendered_strings:
            unmatched.extend(
                [
                    no_match[1]
                    for no_match in re.findall(regex, rendered_str)
                    if no_match[1] not in unmatched
                ]
            )

        # fix any escaped curly braces
        rendered_strings = [
            rendered_str.replace("{{", "{").replace("}}", "}")
            for rendered_str in rendered_strings
        ]

        if filename:
            rendered_strings = [
                sanitize_filename(rendered_str) for rendered_str in rendered_strings
            ]

        if strip:
            rendered_strings = [
                rendered_str.strip() for rendered_str in rendered_strings
            ]

        return rendered_strings, unmatched

    def _render_multi_valued_templates(
        self,
        rendered,
        none_str,
        path_sep,
        expand_inplace,
        inplace_sep,
        filename,
        dirname,
    ):
        rendered_strings = [rendered]
        new_rendered_strings = []
        while new_rendered_strings != rendered_strings:
            new_rendered_strings = rendered_strings
            for field in MULTI_VALUE_SUBSTITUTIONS:
                # Build a regex that matches only the field being processed
                re_str = (
                    RE_OPENING_BRACE
                    + RE_DELIM
                    + r"("
                    + field  # group 2: field name
                    + r")"
                    + RE_PATH_SEP
                    + RE_REPLACE
                    + RE_BOOL_VAL
                    + RE_DEFAULT_VAL
                    + RE_CLOSING_BRACE
                )
                regex_multi = re.compile(re_str)

                # holds each of the new rendered_strings, dict to avoid repeats (dict.keys())
                new_strings = {}

                for str_template in rendered_strings:
                    matches = regex_multi.search(str_template)
                    if matches:
                        path_sep = (
                            matches.group(MATCH_GROUPS_PATH_SEP).strip("()")
                            if matches.group(MATCH_GROUPS_PATH_SEP) is not None
                            else path_sep
                        )
                        replace = (
                            matches.group(MATCH_GROUPS_REPLACE)[1:-1]
                            if matches.group(MATCH_GROUPS_REPLACE) is not None
                            else None
                        )
                        values = self.get_template_value_multi(
                            field,
                            path_sep,
                            filename=filename,
                            dirname=dirname,
                            replacement=replace,
                        )
                        if (
                            expand_inplace
                            or matches.group(MATCH_GROUPS_DELIM) is not None
                        ):
                            delim = (
                                matches.group(MATCH_GROUPS_DELIM)[:-1]
                                if matches.group(MATCH_GROUPS_DELIM) is not None
                                else inplace_sep
                            )
                            # instead of returning multiple strings, join values into a single string
                            val = (
                                delim.join(sorted(values))
                                if values and values[0]
                                else None
                            )

                            def lookup_template_value_multi(
                                lookup_value, *args, **kwargs
                            ):
                                """ Closure passed to make_subst_function get_func 
                                        Capture val and field in the closure 
                                        Allows make_subst_function to be re-used w/o modification
                                        _ is not used but required so signature matches get_template_value """
                                if lookup_value == field:
                                    return val
                                else:
                                    raise ValueError(
                                        f"Unexpected value: {lookup_value}"
                                    )

                            subst = self.make_subst_function(
                                none_str,
                                filename,
                                dirname,
                                get_func=lookup_template_value_multi,
                            )
                            new_string = regex_multi.sub(subst, str_template)

                            # update rendered_strings for the next field to process
                            rendered_strings = list({new_string})
                        else:
                            # create a new template string for each value
                            for val in values:

                                def lookup_template_value_multi(
                                    lookup_value, *args, **kwargs
                                ):
                                    """ Closure passed to make_subst_function get_func 
                                        Capture val and field in the closure 
                                        Allows make_subst_function to be re-used w/o modification
                                        _ is not used but required so signature matches get_template_value """
                                    if lookup_value == field:
                                        return val
                                    else:
                                        raise ValueError(
                                            f"Unexpected value: {lookup_value}"
                                        )

                                subst = self.make_subst_function(
                                    none_str,
                                    filename,
                                    dirname,
                                    get_func=lookup_template_value_multi,
                                )
                                new_string = regex_multi.sub(subst, str_template)
                                new_strings[new_string] = 1

                            # update rendered_strings for the next field to process
                            rendered_strings = sorted(list(new_strings.keys()))
        return rendered_strings

    def _render_exiftool_template(
        self,
        rendered_strings,
        none_str,
        path_sep,
        expand_inplace,
        inplace_sep,
        filename,
        dirname,
    ):
        # TODO: lots of code commonality with render_multi_valued_templates -- combine or pull out
        # TODO: put these in globals
        if path_sep is None:
            path_sep = os.path.sep

        if inplace_sep is None:
            inplace_sep = ","

        # Build a regex that matches only the field being processed
        re_str = (
            RE_OPENING_BRACE
            + RE_DELIM
            + r"(exiftool:[^\\,}+\?\[\]]+)"  # group 3 field name
            + RE_PATH_SEP
            + RE_REPLACE
            + RE_BOOL_VAL
            + RE_DEFAULT_VAL
            + RE_CLOSING_BRACE
        )
        regex_multi = re.compile(re_str)

        # holds each of the new rendered_strings, dict to avoid repeats (dict.keys())
        new_rendered_strings = []
        while new_rendered_strings != rendered_strings:
            new_rendered_strings = rendered_strings
            new_strings = {}
            for str_template in rendered_strings:
                matches = regex_multi.search(str_template)
                if matches:
                    # allmatches = regex_multi.finditer(str_template)
                    # for matches in allmatches:
                    path_sep = (
                        matches.group(MATCH_GROUPS_PATH_SEP).strip("()")
                        if matches.group(MATCH_GROUPS_PATH_SEP) is not None
                        else path_sep
                    )
                    replace = (
                        matches.group(MATCH_GROUPS_REPLACE)[1:-1]
                        if matches.group(MATCH_GROUPS_REPLACE) is not None
                        else None
                    )
                    field = matches.group(MATCH_GROUPS_FIELD)
                    subfield = field[9:]
                    if not self.photo.path:
                        values = [None]
                    else:
                        exif = ExifTool(self.photo.path, exiftool=self.exiftool_path)
                        exifdict = exif.asdict()
                        exifdict = {k.lower(): v for (k, v) in exifdict.items()}
                        subfield = subfield.lower()
                        if subfield in exifdict:
                            values = exifdict[subfield]
                            values = (
                                [values] if not isinstance(values, list) else values
                            )
                            if replace and values:
                                new_values = []
                                for value in values:
                                    new_values.append(self.replace(value, replace))
                                values = new_values

                            # sanitize directory names if needed
                            if filename:
                                values = [sanitize_pathpart(value) for value in values]
                            elif dirname:
                                values = [sanitize_dirname(value) for value in values]

                        else:
                            values = [None]
                    if expand_inplace or matches.group(MATCH_GROUPS_DELIM) is not None:
                        delim = (
                            matches.group(MATCH_GROUPS_DELIM)[:-1]
                            if matches.group(MATCH_GROUPS_DELIM) is not None
                            else inplace_sep
                        )
                        # instead of returning multiple strings, join values into a single string
                        val = (
                            delim.join(sorted(values)) if values and values[0] else None
                        )

                        def lookup_template_value_exif(lookup_value, *args, **kwargs):
                            """ Closure passed to make_subst_function get_func 
                                    Capture val and field in the closure 
                                    Allows make_subst_function to be re-used w/o modification
                                    _ is not used but required so signature matches get_template_value """
                            if lookup_value == field:
                                return val
                            else:
                                raise ValueError(f"Unexpected value: {lookup_value}")

                        subst = self.make_subst_function(
                            none_str,
                            filename,
                            dirname,
                            get_func=lookup_template_value_exif,
                        )
                        new_string = regex_multi.sub(subst, str_template)
                        # update rendered_strings for the next field to process
                        rendered_strings = list({new_string})
                    else:
                        # create a new template string for each value
                        for val in values:

                            def lookup_template_value_exif(
                                lookup_value, *args, **kwargs
                            ):
                                """ Closure passed to make_subst_function get_func 
                                    Capture val and field in the closure 
                                    Allows make_subst_function to be re-used w/o modification
                                    _ is not used but required so signature matches get_template_value """
                                if lookup_value == field:
                                    return val
                                else:
                                    raise ValueError(
                                        f"Unexpected value: {lookup_value}"
                                    )

                            subst = self.make_subst_function(
                                none_str,
                                filename,
                                dirname,
                                get_func=lookup_template_value_exif,
                            )
                            new_string = regex_multi.sub(subst, str_template)
                            new_strings[new_string] = 1
                        # update rendered_strings for the next field to process
                        rendered_strings = sorted(list(new_strings.keys()))
        return rendered_strings

    def get_template_value(
        self,
        field,
        default,
        bool_val=None,
        delim=None,
        path_sep=None,
        filename=False,
        dirname=False,
        replacement=None,
    ):
        """lookup value for template field (single-value template substitutions)

        Args:
            field: template field to find value for.
            default: the default value provided by the user
            bool_val: True value if expression is boolean 
            delim: delimiter for expand in place
            path_sep: path separator for fields that are path-like
            filename: if True, template output will be sanitized to produce valid file name
            dirname: if True, template output will be sanitized to produce valid directory name 
            replacement: str, value to replace any illegal file path characters with; default = ":"
        
        Returns:
            The matching template value (which may be None).

        Raises:
            ValueError if no rule exists for field.
        """

        # initialize today with current date/time if needed
        if self.today is None:
            self.today = datetime.datetime.now()

        value = None

        # wouldn't a switch/case statement be nice...
        if field == "name":
            value = pathlib.Path(self.photo.filename).stem
        elif field == "original_name":
            value = pathlib.Path(self.photo.original_filename).stem
        elif field == "title":
            value = self.photo.title
        elif field == "descr":
            value = self.photo.description
        elif field == "media_type":
            value = self.get_media_type(default)
        elif field == "photo_or_video":
            value = self.get_photo_video_type(default)
        elif field == "hdr":
            value = self.get_photo_bool_attribute("hdr", default, bool_val)
        elif field == "edited":
            value = self.get_photo_bool_attribute("hasadjustments", default, bool_val)
        elif field == "created.date":
            value = DateTimeFormatter(self.photo.date).date
        elif field == "created.year":
            value = DateTimeFormatter(self.photo.date).year
        elif field == "created.yy":
            value = DateTimeFormatter(self.photo.date).yy
        elif field == "created.mm":
            value = DateTimeFormatter(self.photo.date).mm
        elif field == "created.month":
            value = DateTimeFormatter(self.photo.date).month
        elif field == "created.mon":
            value = DateTimeFormatter(self.photo.date).mon
        elif field == "created.dd":
            value = DateTimeFormatter(self.photo.date).dd
        elif field == "created.dow":
            value = DateTimeFormatter(self.photo.date).dow
        elif field == "created.doy":
            value = DateTimeFormatter(self.photo.date).doy
        elif field == "created.hour":
            value = DateTimeFormatter(self.photo.date).hour
        elif field == "created.min":
            value = DateTimeFormatter(self.photo.date).min
        elif field == "created.sec":
            value = DateTimeFormatter(self.photo.date).sec
        elif field == "created.strftime":
            if default:
                try:
                    value = self.photo.date.strftime(default)
                except:
                    raise ValueError(f"Invalid strftime template: '{default}'")
            else:
                value = None
        elif field == "modified.date":
            value = (
                DateTimeFormatter(self.photo.date_modified).date
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).date
            )
        elif field == "modified.year":
            value = (
                DateTimeFormatter(self.photo.date_modified).year
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).year
            )
        elif field == "modified.yy":
            value = (
                DateTimeFormatter(self.photo.date_modified).yy
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).yy
            )
        elif field == "modified.mm":
            value = (
                DateTimeFormatter(self.photo.date_modified).mm
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).mm
            )
        elif field == "modified.month":
            value = (
                DateTimeFormatter(self.photo.date_modified).month
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).month
            )
        elif field == "modified.mon":
            value = (
                DateTimeFormatter(self.photo.date_modified).mon
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).mon
            )
        elif field == "modified.dd":
            value = (
                DateTimeFormatter(self.photo.date_modified).dd
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).dd
            )
        elif field == "modified.dow":
            value = (
                DateTimeFormatter(self.photo.date_modified).dow
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).dow
            )
        elif field == "modified.doy":
            value = (
                DateTimeFormatter(self.photo.date_modified).doy
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).doy
            )
        elif field == "modified.hour":
            value = (
                DateTimeFormatter(self.photo.date_modified).hour
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).hour
            )
        elif field == "modified.min":
            value = (
                DateTimeFormatter(self.photo.date_modified).min
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).min
            )
        elif field == "modified.sec":
            value = (
                DateTimeFormatter(self.photo.date_modified).sec
                if self.photo.date_modified
                else DateTimeFormatter(self.photo.date).sec
            )
        elif field == "modified.strftime":
            if default:
                try:
                    date = self.photo.date_modified or self.photo.date
                    value = date.strftime(default)
                except:
                    raise ValueError(f"Invalid strftime template: '{default}'")
            else:
                value = None
        elif field == "today.date":
            value = DateTimeFormatter(self.today).date
        elif field == "today.year":
            value = DateTimeFormatter(self.today).year
        elif field == "today.yy":
            value = DateTimeFormatter(self.today).yy
        elif field == "today.mm":
            value = DateTimeFormatter(self.today).mm
        elif field == "today.month":
            value = DateTimeFormatter(self.today).month
        elif field == "today.mon":
            value = DateTimeFormatter(self.today).mon
        elif field == "today.dd":
            value = DateTimeFormatter(self.today).dd
        elif field == "today.dow":
            value = DateTimeFormatter(self.today).dow
        elif field == "today.doy":
            value = DateTimeFormatter(self.today).doy
        elif field == "today.hour":
            value = DateTimeFormatter(self.today).hour
        elif field == "today.min":
            value = DateTimeFormatter(self.today).min
        elif field == "today.sec":
            value = DateTimeFormatter(self.today).sec
        elif field == "today.strftime":
            if default:
                try:
                    value = self.today.strftime(default)
                except:
                    raise ValueError(f"Invalid strftime template: '{default}'")
            else:
                value = None
        elif field == "place.name":
            value = self.photo.place.name if self.photo.place else None
        elif field == "place.country_code":
            value = self.photo.place.country_code if self.photo.place else None
        elif field == "place.name.country":
            value = (
                self.photo.place.names.country[0]
                if self.photo.place and self.photo.place.names.country
                else None
            )
        elif field == "place.name.state_province":
            value = (
                self.photo.place.names.state_province[0]
                if self.photo.place and self.photo.place.names.state_province
                else None
            )
        elif field == "place.name.city":
            value = (
                self.photo.place.names.city[0]
                if self.photo.place and self.photo.place.names.city
                else None
            )
        elif field == "place.name.area_of_interest":
            value = (
                self.photo.place.names.area_of_interest[0]
                if self.photo.place and self.photo.place.names.area_of_interest
                else None
            )
        elif field == "place.address":
            value = (
                self.photo.place.address_str
                if self.photo.place and self.photo.place.address_str
                else None
            )
        elif field == "place.address.street":
            value = (
                self.photo.place.address.street
                if self.photo.place and self.photo.place.address.street
                else None
            )
        elif field == "place.address.city":
            value = (
                self.photo.place.address.city
                if self.photo.place and self.photo.place.address.city
                else None
            )
        elif field == "place.address.state_province":
            value = (
                self.photo.place.address.state_province
                if self.photo.place and self.photo.place.address.state_province
                else None
            )
        elif field == "place.address.postal_code":
            value = (
                self.photo.place.address.postal_code
                if self.photo.place and self.photo.place.address.postal_code
                else None
            )
        elif field == "place.address.country":
            value = (
                self.photo.place.address.country
                if self.photo.place and self.photo.place.address.country
                else None
            )
        elif field == "place.address.country_code":
            value = (
                self.photo.place.address.iso_country_code
                if self.photo.place and self.photo.place.address.iso_country_code
                else None
            )
        elif field == "searchinfo.season":
            value = self.photo.search_info.season if self.photo.search_info else None
        elif field == "exif.camera_make":
            value = self.photo.exif_info.camera_make if self.photo.exif_info else None
        elif field == "exif.camera_model":
            value = self.photo.exif_info.camera_model if self.photo.exif_info else None
        elif field == "exif.lens_model":
            value = self.photo.exif_info.lens_model if self.photo.exif_info else None
        elif field == "uuid":
            value = self.photo.uuid
        else:
            # if here, didn't get a match
            raise ValueError(f"Unhandled template value: {field}")

        if value and replacement:
            value = self.replace(value, replacement)
            # process character replacements

        if filename:
            value = sanitize_pathpart(value)
        elif dirname:
            value = sanitize_dirname(value)

        return value

    def replace(self, value, replacement):
        """ process REPLACE template option

        Args:
            value: str value to process
            replacement: str in form OLD,NEW|OLD,NEW... with old and new values for replacement
        
        Returns:
            value with all replacements done
        
        Raises:
            ValueError if replacement string is in wrong format
        """
        if not value:
            return value

        replacements = replacement.split("|")
        for r in replacements:
            try:
                old, new = r.split(",")
            except ValueError:
                raise ValueError(f"Invalid template REPLACE value: {replacement}")
            value = value.replace(old, new)
        return value

    def get_template_value_multi(
        self, field, path_sep, filename=False, dirname=False, replacement=None
    ):
        """lookup value for template field (multi-value template substitutions)

        Args:
            field: template field to find value for.
            path_sep: path separator to use for folder_album field
            dirname: if True, values will be sanitized to be valid directory names; default = False
        
        Returns:
            List of the matching template values or [None].

        Raises:
            ValueError if no rule exists for field.
        """

        """ return list of values for a multi-valued template field """
        values = []
        if field == "album":
            values = self.photo.albums
        elif field == "keyword":
            values = self.photo.keywords
        elif field == "person":
            values = self.photo.persons
            # remove any _UNKNOWN_PERSON values
            values = [val for val in values if val != _UNKNOWN_PERSON]
        elif field == "label":
            values = self.photo.labels
        elif field == "label_normalized":
            values = self.photo.labels_normalized
        elif field == "folder_album":
            values = []
            # photos must be in an album to be in a folder
            for album in self.photo.album_info:
                if album.folder_names:
                    # album in folder
                    if dirname:
                        # being used as a filepath so sanitize each part
                        folder = path_sep.join(
                            sanitize_dirname(f) for f in album.folder_names
                        )
                        folder += path_sep + sanitize_dirname(album.title)
                    else:
                        folder = path_sep.join(album.folder_names)
                        folder += path_sep + album.title
                    values.append(folder)
                else:
                    # album not in folder
                    if dirname:
                        values.append(sanitize_dirname(album.title))
                    else:
                        values.append(album.title)
        elif field == "comment":
            values = [
                f"{comment.user}: {comment.text}" for comment in self.photo.comments
            ]
        elif field == "searchinfo.holiday":
            values = self.photo.search_info.holidays if self.photo.search_info else []
        elif field == "searchinfo.activity":
            values = self.photo.search_info.activities if self.photo.search_info else []
        elif field == "searchinfo.venue":
            values = self.photo.search_info.venues if self.photo.search_info else []
        elif field == "searchinfo.venue_type":
            values = (
                self.photo.search_info.venue_types if self.photo.search_info else []
            )
        elif not field.startswith("exiftool:"):
            # exiftool: templates handled by _render_exiftool_template
            raise ValueError(f"Unhandled template value: {field}")

        # do any replacements needs
        if replacement:
            new_values = []
            for value in values:
                # process replacements
                new_values.append(self.replace(value, replacement))
            values = new_values

        # sanitize directory names if needed, folder_album handled differently above
        if filename:
            values = [sanitize_pathpart(value) for value in values]
        elif dirname and field != "folder_album":
            # skip folder_album because it would have been handled above
            values = [sanitize_dirname(value) for value in values]

        # If no values, insert None so code below will substite none_str for None
        values = values or [None]
        return values

    def get_photo_video_type(self, default):
        """ return media type, e.g. photo or video """
        default_dict = parse_default_kv(default, PHOTO_VIDEO_TYPE_DEFAULTS)
        if self.photo.isphoto:
            return default_dict["photo"]
        else:
            return default_dict["video"]

    def get_media_type(self, default):
        """ return special media type, e.g. slow_mo, panorama, etc., defaults to photo or video if no special type """
        default_dict = parse_default_kv(default, MEDIA_TYPE_DEFAULTS)
        p = self.photo
        if p.selfie:
            return default_dict["selfie"]
        elif p.time_lapse:
            return default_dict["time_lapse"]
        elif p.panorama:
            return default_dict["panorama"]
        elif p.slow_mo:
            return default_dict["slow_mo"]
        elif p.screenshot:
            return default_dict["screenshot"]
        elif p.portrait:
            return default_dict["portrait"]
        elif p.live_photo:
            return default_dict["live_photo"]
        elif p.burst:
            return default_dict["burst"]
        elif p.ismovie:
            return default_dict["video"]
        else:
            return default_dict["photo"]

    def get_photo_bool_attribute(self, attr, default, bool_val):
        # get value for a PhotoInfo bool attribute
        val = getattr(self.photo, attr)
        if val:
            return bool_val
        else:
            return default


def parse_default_kv(default, default_dict):
    """ parse a string in form key1=value1;key2=value2,... as used for some template fields

    Args:
        default: str, in form 'photo=foto;video=vidéo'
        default_dict: dict, in form {"photo": "fotos", "video": "vidéos"} with default values

    Returns:
        dict in form {"photo": "fotos", "video": "vidéos"}
    """

    default_dict_ = default_dict.copy()
    if default:
        defaults = default.split(";")
        for kv in defaults:
            try:
                k, v = kv.split("=")
                k = k.strip()
                v = v.strip()
                default_dict_[k] = v
            except ValueError:
                pass
    return default_dict_
