import pytest

import mesop.protos.ui_pb2 as pb
from mesop.components.box.box import box
from mesop.components.button.button import button
from mesop.components.radio.radio import radio
from mesop.editor.component_configs import (
  generate_component_config,
  get_component_configs,
)
from mesop.labs.layout import columns


def test_generate_component_config_button():
  proto = generate_component_config(button)
  assert proto.component_name.core_module is True
  assert proto.component_name.fn_name == "button"
  assert proto.fields[0] == pb.EditorField(name="on_click")
  assert proto.fields[1] == pb.EditorField(
    name="type",
    type=pb.FieldType(
      literal_type=pb.LiteralType(
        literals=[
          pb.LiteralElement(string_literal="raised"),
          pb.LiteralElement(string_literal="flat"),
          pb.LiteralElement(string_literal="stroked"),
          pb.LiteralElement(string_literal="icon"),
        ],
      )
    ),
  )


def test_generate_component_config_box():
  proto = generate_component_config(box)
  assert proto.component_name.core_module is True
  assert proto.component_name.fn_name == "box"
  assert proto.accepts_child
  assert proto.fields[0].name == "style"
  assert proto.fields[0].type.struct_type.struct_name == "Style"
  # Don't make this a change-detector test; it will slowly accumulate
  # more fields.
  assert len(proto.fields[0].type.struct_type.fields) > 15


def test_generate_component_config_radio():
  proto = generate_component_config(radio)
  assert proto.component_name.core_module is True
  assert proto.component_name.fn_name == "radio"
  assert proto.accepts_child is False
  assert proto.fields[0] == pb.EditorField(
    name="options",
    type=pb.FieldType(
      list_type=pb.ListType(
        type=pb.FieldType(
          struct_type=pb.StructType(
            struct_name="RadioOption",
            fields=[
              pb.EditorField(
                name="label", type=pb.FieldType(string_type=pb.StringType())
              ),
              pb.EditorField(
                name="value", type=pb.FieldType(string_type=pb.StringType())
              ),
            ],
          )
        )
      )
    ),
  )


def test_generate_component_config_labs_column():
  proto = generate_component_config(columns)
  assert proto.component_name.HasField("core_module") is False
  assert proto.component_name.module_path == "mesop.labs.layout"
  assert proto.component_name.fn_name == "columns"


def test_get_component_configs():
  # Don't make this a change-detector test; it will slowly accumulate
  # more component configs.
  assert len(get_component_configs()) >= 3


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
