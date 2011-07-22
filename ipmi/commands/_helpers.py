__all__ = ["SIMPLE_VAL", "BOOL_VAL", "parse_response"]

SIMPLE_VAL = 1
BOOL_VAL = 2

def str2bool(v):
  return v.lower() == "true"

def field_to_attr(field_name):
    return field_name.lower().replace(' ', '_')

def field_to_objval(obj, field_info, field_name, value):
    attr_name = field_info.get('attr', field_to_attr(field_name))
    attr_conv = field_info.get('conv', SIMPLE_VAL)

    if attr_conv == SIMPLE_VAL:
        setattr(obj, attr_name, value)
    elif attr_conv == BOOL_VAL:
        setattr(obj, attr_name, str2bool(value))
    else:
        setattr(obj, attr_name, attr_conv(value))

def parse_response(obj, response, mapping):
    lines = response.split("\n")
    left_over = []
    for line in lines:
        if line.find(':') == -1:
            continue

        field, value = [field.strip() for field in line.split(":")]

        field_info = mapping.get(field)

        if field_info == None:
            left_over.append((field, value))
            continue

        field_to_objval(obj, field_info, field, value)
