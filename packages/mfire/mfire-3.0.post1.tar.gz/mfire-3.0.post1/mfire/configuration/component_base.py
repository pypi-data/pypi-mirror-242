"""
@package configuration.component_base

component for Config processor module
"""

# Standard packages
from typing import List, Union
from pydantic import BaseModel

# Third party package
from shapely.geometry import (
    Point,
    Polygon,
    MultiPoint,
    MultiPolygon,
    LineString,
    MultiLineString,
)
import shapely.geometry as sh

# Own package

# local package
from mfire.configuration.datas import RHManager
from mfire.composite import PeriodCollection
from mfire.configuration.geos import MaskConfig

Geometry_used = Union[
    Point, MultiPoint, Polygon, MultiPolygon, LineString, MultiLineString
]


class ComponentManager:
    def __init__(self, rhmanager: RHManager, configuration_datetime):
        self.rhmanager = rhmanager
        self.configuration_datetime = configuration_datetime

    def useable_geometries(self, geo_config: Geometry_used) -> List[str]:
        """useable_geometries : Returns the useable geometries with
        a geographical zone according to its configuration.

        Args:
            geo_config (FeatureConfig): Geograpghical zone's configuration

        Returns:
            List[str] : list of useable geometries's names.
        """
        if not isinstance(geo_config, Geometry_used):
            return []
        return [
            gname
            for gname, bounds in self.rhmanager.rules.get_bounds()
            if sh.box(*bounds).contains(geo_config)
        ]


class CompoBase(BaseModel):
    class Config:
        copy_on_model_validation = False

    single_data_config: dict = None
    single_mask_config: MaskConfig = None
    processed_periods: PeriodCollection = None
    processed_hazards: dict = None
    all_shapes: dict = None
