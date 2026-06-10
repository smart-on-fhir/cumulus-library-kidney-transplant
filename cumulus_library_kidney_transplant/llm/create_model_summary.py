import enum
import pydantic
import pathlib

from typing import Any, get_args, get_origin, Union
from types import UnionType

from cumulus_library_kidney_transplant.llm.model import (
    KidneyTransplantDonorGroupAnnotation,
    ImmunosuppressiveMedicationsAnnotation,
    KidneyTransplantLongitudinalAnnotation,
    MultipleTransplantHistoryAnnotation,
)

_INDENT = "    "
_IGNORE_FIELDS = {"has_mention", "spans"}


def _field_description(field: Any) -> str | None:
    """
    Retrieves the description of a given field or None if not defined.
    """
    if hasattr(field, "description") and field.description:
        return field.description
    return None


def _is_model_type(tp: Any) -> bool:
    """
    Determines if the type is a subclass of pydantic.BaseModel.
    """
    return isinstance(tp, type) and issubclass(tp, pydantic.BaseModel)


def _is_span_augmented(model_cls: type[pydantic.BaseModel]) -> bool:
    """
    Duck typing based on the presence of has_mention and spans fields.
    """
    model_fields = model_cls.model_fields
    return all(span_field in model_fields for span_field in _IGNORE_FIELDS)


def _unwrap_optional(tp: Any) -> tuple[Any, bool]:
    """
    Unwrap Optional types to extract the inner type and optionality status.
    
    Returns:
        - A tuple of (inner_type, is_optional) where is_optional is True if the
          original type was Optional[T] (i.e., Union[T, None]).
        - Returns the original tp and False if it's not Optional.
    """
    origin = get_origin(tp)
    if origin is Union or origin is UnionType:
        args = get_args(tp)
        # Check if this is Optional (Union with exactly 2 args, one being None)
        if len(args) == 2 and type(None) in args:
            other = args[0] if args[1] is type(None) else args[1]
            return other, True
    return tp, False


def _extract_model_type(tp: Any) -> tuple[type[pydantic.BaseModel] | None, bool]:
    """
    Extract a BaseModel type from a type annotation, unwrapping Optional types and drilling down for a list if true.
    Returns a tuple of (model_type, is_list).
    """
    base, _ = _unwrap_optional(tp)
    origin = get_origin(base)
    if origin is list:
        args = get_args(base)
        if args and _is_model_type(args[0]):
            return args[0], True
    if _is_model_type(base):
        return base, False
    return None, False


def _extract_enum_type(tp: Any) -> type[enum.Enum] | None:
    """
    Extract an enum.Enum type from a type annotation, unwrapping Optional types.
    """
    base, _ = _unwrap_optional(tp)
    if isinstance(base, type) and issubclass(base, enum.Enum):
        return base
    return None


def _type_to_string(tp: Any) -> str:
    base, is_optional = _unwrap_optional(tp)
    origin = get_origin(base)
    if origin is list:
        args = get_args(base)
        # Handle case of list[Any]
        inner = _type_to_string(args[0]) if args else "Any"
        rendered = f"A list of [{inner}]"
    elif _extract_enum_type(base):
        rendered = f"{base.__name__} (Choice Value)"
    elif base is bool:
        rendered = "True or False"
    elif base is str:
        rendered = "Plaintext string"
    elif base is int:
        rendered = "Integer number"
    elif isinstance(base, type):
        rendered = base.__name__
    else:
        # Clean up typing module' prefixes as-needed
        rendered = str(base).replace("typing.", "")
    if is_optional:
        return f"Optional mention of [{rendered}]"
    return rendered


def _class_walk(current_cls: type[pydantic.BaseModel], indent_level: int, indent_txt: str) -> list[str]:
    lines = []
    span_augmented = _is_span_augmented(current_cls)

    for name, field in current_cls.model_fields.items():
        if span_augmented and name in _IGNORE_FIELDS:
            continue
        
        annotation = field.annotation
        description = _field_description(field)
        nested_model, is_list = _extract_model_type(annotation)
        current_indent = indent_txt * indent_level
        if nested_model:
            if is_list:
                lines.append(f"{current_indent}{name}: A (possibly empty) list of {nested_model.__name__} instances, which contain:")
                lines += _class_walk(nested_model, indent_level + 1, indent_txt)
            else:
                lines.append(f"{current_indent}{name}:")
                lines += _class_walk(nested_model, indent_level + 1, indent_txt)
            lines.append("")
            lines.append("")
            continue
        # Base-level field and type
        type_str = _type_to_string(annotation)
        lines.append(f"{current_indent}{name} = {type_str}")

        # Determine if there are comments to add below that
        comment_bits = []
        if description:
            comment_bits.append(f"{description}")
        enum_type = _extract_enum_type(annotation)
        if enum_type:
            comment_bits.append("Possible Values:")
            for value in enum_type:
                comment_bits.append(f"  - {value.value}")
        if comment_bits:
            comment_prefix = f"{current_indent}{indent_txt}# "
            # Comments should start with a common prefix, increasing indentation
            for comment in comment_bits:
                # Add one more level of indentation, and then the comment
                lines.append(f"{comment_prefix}{comment}")
        
    return lines


def create_model_summary(model: pydantic.BaseModel | type[pydantic.BaseModel], path: str = "summaries/model_summary.txt", indent_txt: str = _INDENT) -> str:
    # Be flexible enough to handle a model instance or the class itself
    model_cls = model if isinstance(model, type) else model.__class__

    # Start the recursive _class_walk
    lines = _class_walk(model_cls, 0, indent_txt=indent_txt)

    # Add a header with the model class name
    header = f'model = "{model_cls.__name__}"'
    lines.insert(0, header)
    model_summary = "\n".join(lines)
    
    # Save the summary to a text file for easier viewing
    with open(pathlib.Path(__file__).parent / path, "w") as f:
        f.write(model_summary) 
    return model_summary

if __name__ == "__main__":
    create_model_summary(KidneyTransplantDonorGroupAnnotation, path='summaries/donor_group_summary.txt')
    create_model_summary(ImmunosuppressiveMedicationsAnnotation, path='summaries/treatment_summary.txt')
    create_model_summary(KidneyTransplantLongitudinalAnnotation, path='summaries/longitudinal_summary.txt')
    create_model_summary(MultipleTransplantHistoryAnnotation, path='summaries/multiple_transplant_history_summary.txt')
    
