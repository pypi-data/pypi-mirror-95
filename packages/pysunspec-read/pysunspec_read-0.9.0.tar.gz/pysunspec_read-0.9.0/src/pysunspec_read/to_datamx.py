import logging
from datetime import datetime

from sunspec.core.client import ClientPoint, ClientBlock

from .options import ReadOptions
from datamx.models.values import Groups, Group, Value


def to_datamx(client, read_options: ReadOptions):
    now = get_now()
    mx_groups = Groups(datetime=now)
    log = logging.getLogger(__name__)
    log.info("Reading time: " + mx_groups.datetime.isoformat())
    for model in client.device.models_list:
        if skip_model(model, read_options):
            continue

        for block in model.blocks:

            mx_group = None

            for point in block.points_list:
                if point.value is None:
                    pass
                    # print("Skipping point that has no value id={}".format(point.point_type.id))
                elif read_options and not read_options.allow_id(point.point_type.id):
                    pass
                    # print("Skipping point by id={}".format(point.point_type.id))
                else:
                    if mx_group is None:
                        mx_group = create_mx_group(block)
                        mx_group.name = model.model_type.name
                        mx_groups.groups.append(mx_group)

                    mx_value = create_value(point)
                    if mx_group.values is None:
                        mx_group.values = []
                    mx_group.values.append(mx_value)

    return mx_groups


def get_now():
    return datetime.now()


def create_value(point: ClientPoint):
    value = Value(id=point.point_type.id, value=point.value)
    value.value = point.value
    # value.base = point.value_base
    # value.scale = point.value_sf
    # value.location = Location(address=point.addr)
    # if point.impl:
    #     value.impl = True
    # if point.dirty:
    #     value.properties = []
    #     value.properties.append(Property(name="dirty", value=True))
    #
    # value.vtype = create_value_type(point)
    return value


# def create_value_type(point: ClientPoint):
#     point_type = point.point_type
#     vtype = ValueType(id = point_type.id, description=point_type.description,
#                       label=point_type.label, notes=point_type.notes)
#     vtype.units = point_type.units
#     vtype.access = point_type.access
#     vtype.data_type = point_type.type
#     if point_type.mandatory:
#         vtype.required = True
#     # don't populate with an empty string
#     if point_type.value_default:
#         vtype.default = point_type.value_default
#     vtype.location = Location(offset=point_type.offset, length=point_type.len)
#
#     if point_type.sf is not None:
#         vtype.properties = []
#         vtype.properties.append(Property(name="point type sf", value=(point_type.sf)))
#     return vtype


def skip_model(model, read_options):
    if model.model_type is None:
        return True

    model_not_allowed = read_options and not read_options.allow_model(model.model_type.name)
    if model_not_allowed:
        return True


def create_mx_group(block: ClientBlock):
    mx_group = Group()
    # mx_group.model =
    # mx_group.location = Location(address=block.addr, index=block.index, length=block.len)
    # think len here is same as on block_type
    # if block.type:
    #     mx_group.properties = []
    #     mx_group.properties.append(Property(name="type", value=(block.type)))
    #     think this is always same as on block and block_type, maybe don't add it to the properties
    # mx_group.gtype=GroupType(name=block.block_type.name, type=block.block_type.type)
    # TODO fix up repeating?
    if block.type == "repeating":
        mx_group.type = "repeating"
    else:
        mx_group.type = "fixed"
    # mx_group.gtype.location = Location(length=block.block_type.len)

    return mx_group

# def create_mx_groups(model):
#     mx_model = Groups(datetime=)
#     # mx_model.location = Location(index=model.index, length = model.len, address=model.addr)
#     # mx_model.mtype = ModelType(
#     #                     location=Location(length=model.model_type.len),
#     #                     label=model.model_type.label,
#     #                     description=model.model_type.description,
#     #                     notes=model.model_type.notes,
#     #                     name=model.model_type.name,
#     # )
#     # what about model_type.repeating_block?
#     return mx_model


# def print_model_xml(client):
#     root = ET.Element(pics.PICS_ROOT)
#     client.device.to_pics(root, single_repeating=False)
#     ET.indent(root)
#     print(ET.tostring(root).decode())
