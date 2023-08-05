import logging

from pysunspec_data.data import Data
from pysunspec_data.block import Block
from pysunspec_data.model import Model
from pysunspec_data.point import Point
from .options import ReadOptions
from datetime import datetime

def to_data(client, read_options: ReadOptions):
    now = datetime.now()
    data = Data()
    data.reading_time = now.isoformat()
    log = logging.getLogger(__name__)

    log.info("running at " + data.reading_time)
    for model in client.device.models_list:
        if skip_model(model, read_options):
            continue
        data_model = None

        for block in model.blocks:

            data_block = None

            for point in block.points_list:
                if point.value is None:
                    pass
                    # print("Skipping point that has no value id={}".format(point.point_type.id))
                elif read_options and not read_options.allow_id(point.point_type.id):
                    pass
                    # print("Skipping point by id={}".format(point.point_type.id))
                else:
                    if data_model is None:
                        data_model = add_model_details(data, model)
                    if data_block is None:
                        data_block = add_block_details(block, data_model)

                    data_point = create_point(point)

                    data_block.add(data_point)

    return data


def create_point(point):
    data_point = Point(id=point.point_type.id)
    data_point.value = point.value
    data_point.value_base = point.value_base
    data_point.value_sf = point.value_sf
    data_point.addr = point.addr
    data_point.dirty = point.dirty
    data_point.impl = point.impl
    data_point.point_type.units = point.point_type.units
    data_point.point_type.label = point.point_type.label
    data_point.point_type.access = point.point_type.access
    data_point.point_type.description = point.point_type.description
    data_point.point_type.len = point.point_type.len
    data_point.point_type.notes = point.point_type.notes
    data_point.point_type.offset = point.point_type.offset
    data_point.point_type.sf = point.point_type.sf
    data_point.point_type.type = point.point_type.type
    data_point.point_type.mandatory = point.point_type.mandatory
    data_point.point_type.value_default = point.point_type.value_default
    return data_point


def skip_model(model, read_options):
    if model.model_type is None:
        return True

    model_not_allowed = read_options and not read_options.allow_model(model.model_type.name)
    if model_not_allowed:
        return True

def add_block_details(block, data_model):
    data_block = Block(type=block.block_type.type)
    data_block.index = block.index
    data_block.addr = block.addr
    data_block.len = block.len
    data_block.type = block.type
    data_block.block_type.name = block.block_type.name
    data_block.block_type.len = block.block_type.len
    data_model.add(data_block)
    return data_block


def add_model_details(data, model):
    data_model = Model(id=model.id, name=model.model_type.name)
    data_model.id = model.id
    data_model.index = model.index
    data_model.model_type.label = model.model_type.label
    data_model.model_type.len = model.model_type.len
    data_model.model_type.notes = model.model_type.notes
    data_model.model_type.description = model.model_type.description
    data.addModel(data_model)
    return data_model

# def printModelXml(client):
#     root = ET.Element(pics.PICS_ROOT)
#     client.device.to_pics(root, single_repeating=False)
#     ET.indent(root)
#     print(ET.tostring(root).decode())