import datetime

from typing import Dict, Optional, Tuple
import re
import sqlalchemy as db
from sqlalchemy.orm import relationship

from tyko.schema.avtables import AVTables, SerializedData


class FormatTypes(AVTables):
    __tablename__ = "format_types"

    id = db.Column(
        "format_id", db.Integer, primary_key=True, autoincrement=True)

    name = db.Column("name", db.Text)

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        return {
            "format_types_id": self.id,
            "name": self.name
        }


class OpenReel(AVTables):
    __tablename__ = "open_reel"

    item_id = db.Column(
        db.Integer, db.ForeignKey("item.item_id"), primary_key=True)

    item = relationship("CollectionItem", foreign_keys=[item_id])

    date_recorded = db.Column(
        "date_recorded", db.Date
    )

    track_count = db.Column("track_count", db.Text)
    tape_size = db.Column("tape_size", db.Text)
    reel_diam = db.Column("reel_diam", db.Integer)
    reel_type = db.Column("reel_type", db.Text)
    tape_thickness = db.Column("tape_thickness", db.Integer)
    tape_brand = db.Column("tape_brand", db.Text)
    base = db.Column("base", db.Text)
    wind = db.Column("wind", db.Text)
    track_speed = db.Column("track_speed", db.Text)
    track_configuration = db.Column("track_configuration", db.Text)
    track_duration = db.Column("track_duration", db.Text)
    generation = db.Column("generation", db.Text)

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        return {
            "item_id": self.item_id,
            "date_recorded": self.serialize_date(self.date_recorded),
            "track_count": self.track_count,
            "tape_size": self.tape_size,
            "reel_diam": self.reel_diam,
            "reel_type": self.reel_type,
            "tape_thickness": self.tape_thickness,
            "tape_brand": self.tape_brand,
            "base": self.base,
            "wind": self.wind,
            "track_speed": self.track_speed,
            "track_configuration": self.track_configuration,
            "track_duration": self.track_duration,
            "generation": self.generation
        }


class Film(AVTables):
    __tablename__ = "film"

    item_id = db.Column(
        db.Integer, db.ForeignKey("item.item_id"), primary_key=True)

    item = relationship("CollectionItem", foreign_keys=[item_id])

    date_of_film = db.Column("date_of_film", db.Date)
    can_label = db.Column("can_label", db.Text)
    leader_label = db.Column("leader_label", db.Text)
    length = db.Column("length", db.Integer)
    duration = db.Column("duration", db.Text)
    format_gauge = db.Column("format_gauge", db.Integer)
    base = db.Column("base", db.Text)
    edge_code_date = db.Column("edge_code_date", db.Date)
    sound = db.Column("sound", db.Text)
    color = db.Column("color", db.Text)
    image_type = db.Column("image_type", db.Text)
    ad_test_date = db.Column("ad_test_date", db.Date)
    ad_test_level = db.Column("ad_test_level", db.Integer)

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        return {
            "item_id": self.item_id,
            "date_of_film": self.serialize_date(self.date_of_film),
            "can_label": self.can_label,
            "leader_label": self.leader_label,
            "length": self.length,
            "duration": self.duration,
            "format_gauge": self.format_gauge,
            "base": self.base,
            "edge_code_date": self.serialize_date(self.edge_code_date),
            "sound": self.sound,
            "color": self.color,
            "image_type": self.image_type,
            "ad_test_date": self.serialize_date(self.ad_test_date),
            "ad_test_level": self.ad_test_level,
        }


class GroovedDisc(AVTables):
    __tablename__ = "grooved_disc"

    item_id = db.Column(
        db.Integer, db.ForeignKey("item.item_id"), primary_key=True)

    item = relationship("CollectionItem", foreign_keys=[item_id])

    # This is a year
    date_recorded = db.Column("date_recorded", db.Integer)
    side = db.Column("side", db.Text)
    duration = db.Column("duration", db.Text)
    diameter = db.Column("diameter", db.Integer)
    disc_material = db.Column("disc_material", db.Text)
    base = db.Column("base", db.Text)
    playback_direction = db.Column("playback_direction", db.Text)
    playback_speed = db.Column("playback_speed", db.Text)

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        return {
            "item_id": self.item_id,
            "date_recorded": self.date_recorded,
            "side": self.side,
            "duration": self.duration,
            "diameter": self.diameter,
            "disc_material": self.disc_material,
            "base": self.base,
            "playback_direction": self.playback_direction,
            "playback_speed": self.playback_speed

        }


class AudioVideo(AVTables):
    __tablename__ = "audio_video"

    item_id = db.Column(
        db.Integer, db.ForeignKey("item.item_id"), primary_key=True)

    item = relationship("CollectionItem", foreign_keys=[item_id])
    date_recorded = db.Column("date_recorded", db.Date)
    side = db.Column("side", db.Text)
    duration = db.Column("duration", db.Text)
    format_subtype = db.Column("format_subtype", db.Text)

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        return {
            "item_id": self.item_id,
            "date_recorded": self.serialize_date(self.date_recorded),
            "side": self.side,
            "duration": self.duration,
            "format_subtype": self.format_subtype

        }


class Format(AVTables):
    __abstract__ = True
    obj_sequence = db.Column("obj_sequence", db.Integer)


class AudioCassette(Format):

    __tablename__ = "AudioCassettes"
    name = db.Column("name", db.Text)
    table_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.object_id"))
    parent_object = relationship("CollectionObject", foreign_keys=[object_id])

    format_type_id = db.Column(db.Integer,
                               db.ForeignKey("cassette_types.table_id"))

    format_type = relationship("CassetteType")

    tape_type_id = db.Column(db.Integer,
                             db.ForeignKey("cassette_tape_types.table_id"))

    tape_type = relationship("CassetteTapeType")

    tape_thickness_id = \
        db.Column(db.Integer,
                  db.ForeignKey("cassette_tape_thickness.table_id"))

    tape_thickness = relationship("CassetteTapeThickness")

    inspection_date = db.Column("inspection_date", db.Date)
    recording_date = db.Column("recording_date", db.Date)
    recording_date_precision = db.Column("recording_date_precision",
                                         db.Integer, default=3)

    # REGEX
    REGEX_DAY_MONTH_YEAR = re.compile(r"^([0-1][0-9])-([0-2][0-9])-([0-9]){4}")
    REGEX_YEAR_ONLY = re.compile(r"^([1-9]){4}$")
    REGEX_MONTH_YEAR = re.compile(r"^([0-1][0-9])-([0-9]){4}$")

    @classmethod
    def serialize_date(cls, date: Optional[datetime.datetime.date],
                       precision=3):

        if isinstance(date, datetime.date):
            if precision == 3:
                return date.strftime("%m-%d-%Y")

            if precision == 2:
                return date.strftime("%m-%Y")

            if precision == 1:
                return date.strftime("%Y")

        return None

    @classmethod
    def encode_date(cls, date_string: str) -> Tuple[datetime.datetime, int]:

        if cls.REGEX_DAY_MONTH_YEAR.match(date_string):
            return datetime.datetime.strptime(date_string, "%m-%d-%Y"), 3

        if cls.REGEX_MONTH_YEAR.match(date_string):
            return datetime.datetime.strptime(date_string, "%m-%Y"), 2

        if cls.REGEX_YEAR_ONLY.match(date_string):
            return datetime.datetime.strptime(date_string, "%Y"), 1

        raise AttributeError("Unknown date format: {}".format(date_string))

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        serialized_data = {
            "name": self.name,
            "id": self.table_id,
            "format_type": self.format_type.serialize(),
            "inspection_date": self.serialize_date(self.inspection_date),
            "obj_sequence": self.obj_sequence,
            "date_recorded":
                self.serialize_date(self.recording_date,
                                    self.recording_date_precision),
        }

        if self.tape_type is not None:
            serialized_data["tape_type"] = self.tape_type.serialize()

        if self.tape_thickness is not None:
            serialized_data["tape_thickness"] = self.tape_thickness.serialize()

        return serialized_data


class CassetteType(AVTables):
    __tablename__ = "cassette_types"
    table_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column("name", db.String)

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        return {
            "name": self.name,
            "id": self.table_id
        }


class CassetteTapeType(AVTables):
    __tablename__ = "cassette_tape_types"
    table_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column("name", db.String)

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        return {
            "name": self.name,
            "id": self.table_id
        }


class CassetteTapeThickness(AVTables):
    __tablename__ = "cassette_tape_thickness"
    table_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column("name", db.String)

    def serialize(self, recurse=False) -> Dict[str, SerializedData]:
        return {
            "name": self.name,
            "id": self.table_id
        }


# =============================================================================
# Enumerated tables
# =============================================================================
#
# To keep the enumerated id tables consistent, the ids are hardcoded
#
# Important Note:
#
# Add to the bottom of this list, For compatibility reasons, do not
# edit existing value ids


# =============================================================================

format_types = {
    "audio video": (1, AudioVideo),
    "audio": (2,),
    "video": (3,),
    "open reel": (4, OpenReel),
    "grooved disc": (5, GroovedDisc),
    "film": (6, Film)
}
