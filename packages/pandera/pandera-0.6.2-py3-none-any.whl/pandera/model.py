"""Class-based api"""
import inspect
import re
import sys
import typing
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

import pandas as pd

from . import schema_components
from . import strategies as st
from .checks import Check
from .errors import SchemaInitError
from .model_components import (
    CHECK_KEY,
    DATAFRAME_CHECK_KEY,
    CheckInfo,
    Field,
    FieldCheckInfo,
    FieldInfo,
)
from .schemas import DataFrameSchema
from .typing import LEGACY_TYPING, AnnotationInfo, Index, Series

if LEGACY_TYPING:

    def get_type_hints(
        obj: Callable[..., Any],
        globalns: Optional[Dict[str, Any]] = None,
        localns: Optional[Dict[str, Any]] = None,
        include_extras: bool = False,
    ) -> Dict[str, Any]:
        # pylint:disable=function-redefined, missing-function-docstring, unused-argument
        return typing.get_type_hints(obj, globalns, localns)


elif sys.version_info[:2] < (3, 9):
    from typing_extensions import get_type_hints
else:
    from typing import get_type_hints

SchemaIndex = Union[schema_components.Index, schema_components.MultiIndex]


_CONFIG_KEY = "Config"


MODEL_CACHE: Dict[Type["SchemaModel"], DataFrameSchema] = {}


class BaseConfig:  # pylint:disable=R0903
    """Define DataFrameSchema-wide options.

    *new in 0.5.0*
    """

    name: Optional[str] = None  #: name of schema
    coerce: bool = False  #: coerce types of all schema components

    #: make sure all specified columns are in the validated dataframe -
    #: if ``"filter"``, removes columns not specified in the schema
    strict: Union[bool, str] = False

    ordered: bool = False  #: validate columns order
    multiindex_name: Optional[str] = None  #: name of multiindex

    #: coerce types of all MultiIndex components
    multiindex_coerce: bool = False

    #: make sure all specified columns are in validated MultiIndex -
    #: if ``"filter"``, removes indexes not specified in the schema
    multiindex_strict: bool = False

    #: validate MultiIndex in order
    multiindex_ordered: bool = True


_config_options = [
    attr for attr in vars(BaseConfig) if not attr.startswith("_")
]


def _extract_config_options(config: Type) -> Dict[str, Any]:
    return {
        name: value
        for name, value in vars(config).items()
        if name in _config_options
    }


class SchemaModel:
    """Definition of a :class:`~pandera.DataFrameSchema`.

    *new in 0.5.0*

    See the :ref:`User Guide <schema_models>` for more.
    """

    Config: Type[BaseConfig] = BaseConfig
    __schema__: Optional[DataFrameSchema] = None
    __config__: Optional[Type[BaseConfig]] = None

    #: Key according to `FieldInfo.name`
    __fields__: Dict[str, Tuple[AnnotationInfo, FieldInfo]] = {}
    __checks__: Dict[str, List[Check]] = {}
    __dataframe_checks__: List[Check] = []

    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} may not be instantiated.")

    def __init_subclass__(cls, **kwargs):
        """Ensure :class:`~pandera.model_components.FieldInfo` instances."""
        super().__init_subclass__(**kwargs)
        # pylint:disable=no-member
        for field_name in cls.__annotations__.keys():
            if field_name not in cls.__dict__:  # Field omitted
                field = Field()
                field.__set_name__(cls, field_name)
                setattr(cls, field_name, field)

    @classmethod
    def to_schema(cls) -> DataFrameSchema:
        """Create :class:`~pandera.DataFrameSchema` from the :class:`.SchemaModel`."""
        if cls in MODEL_CACHE:
            return MODEL_CACHE[cls]

        cls.__fields__ = cls._collect_fields()
        check_infos = typing.cast(
            List[FieldCheckInfo], cls._collect_check_infos(CHECK_KEY)
        )

        cls.__checks__ = cls._extract_checks(
            check_infos, field_names=list(cls.__fields__.keys())
        )

        df_check_infos = cls._collect_check_infos(DATAFRAME_CHECK_KEY)
        cls.__dataframe_checks__ = cls._extract_df_checks(df_check_infos)

        cls.__config__ = cls._collect_config()
        mi_kwargs = {
            name[len("multiindex_") :]: value
            for name, value in vars(cls.__config__).items()
            if name.startswith("multiindex_")
        }
        columns, index = cls._build_columns_index(
            cls.__fields__, cls.__checks__, **mi_kwargs
        )
        cls.__schema__ = DataFrameSchema(
            columns,
            index=index,
            checks=cls.__dataframe_checks__,  # type: ignore
            coerce=cls.__config__.coerce,
            strict=cls.__config__.strict,
            name=cls.__config__.name,
            ordered=cls.__config__.ordered,
        )
        if cls not in MODEL_CACHE:
            MODEL_CACHE[cls] = cls.__schema__
        return cls.__schema__

    @classmethod
    @pd.util.Substitution(validate_doc=DataFrameSchema.validate.__doc__)
    def validate(
        cls,
        check_obj: pd.DataFrame,
        head: Optional[int] = None,
        tail: Optional[int] = None,
        sample: Optional[int] = None,
        random_state: Optional[int] = None,
        lazy: bool = False,
    ) -> pd.DataFrame:
        """%(validate_doc)s"""
        return cls.to_schema().validate(
            check_obj, head, tail, sample, random_state, lazy
        )

    @classmethod
    @pd.util.Substitution(strategy_doc=DataFrameSchema.strategy.__doc__)
    @st.strategy_import_error
    def strategy(cls, *, size=None):
        """%(strategy_doc)s"""
        return cls.to_schema().strategy(size=size)

    @classmethod
    @pd.util.Substitution(example_doc=DataFrameSchema.strategy.__doc__)
    @st.strategy_import_error
    def example(cls, *, size=None):
        """%(example_doc)s"""
        return cls.to_schema().example(size=size)

    @classmethod
    def _build_columns_index(  # pylint:disable=too-many-locals
        cls,
        fields: Dict[str, Tuple[AnnotationInfo, FieldInfo]],
        checks: Dict[str, List[Check]],
        **multiindex_kwargs: Any,
    ) -> Tuple[
        Dict[str, schema_components.Column],
        Optional[Union[schema_components.Index, schema_components.MultiIndex]],
    ]:
        index_count = sum(
            annotation.origin is Index for annotation, _ in fields.values()
        )

        columns: Dict[str, schema_components.Column] = {}
        indices: List[schema_components.Index] = []
        for field_name, (annotation, field) in fields.items():
            field_checks = checks.get(field_name, [])
            field_name = field.name
            check_name = getattr(field, "check_name", None)

            if annotation.metadata:
                if field.dtype_kwargs:
                    raise TypeError(
                        "Cannot specify redundant 'dtype_kwargs' "
                        + f"for {annotation.raw_annotation}."
                        + "\n Usage Tip: Drop 'typing.Annotated'."
                    )
                dtype_kwargs = _get_dtype_kwargs(annotation)
                dtype = annotation.arg(**dtype_kwargs)
            else:
                dtype = annotation.arg

            if annotation.origin is Series:
                col_constructor = (
                    field.to_column if field else schema_components.Column
                )

                if check_name is False:
                    raise SchemaInitError(
                        f"'check_name' is not supported for {field_name}."
                    )

                columns[field_name] = col_constructor(  # type: ignore
                    dtype,
                    required=not annotation.optional,
                    checks=field_checks,
                    name=field_name,
                )
            elif annotation.origin is Index:
                if annotation.optional:
                    raise SchemaInitError(
                        f"Index '{field_name}' cannot be Optional."
                    )

                if check_name is False or (
                    # default single index
                    check_name is None
                    and index_count == 1
                ):
                    field_name = None  # type:ignore

                index_constructor = (
                    field.to_index if field else schema_components.Index
                )
                index = index_constructor(  # type: ignore
                    dtype, checks=field_checks, name=field_name
                )
                indices.append(index)
            else:
                raise SchemaInitError(
                    f"Invalid annotation '{field_name}: {annotation.raw_annotation}'"
                )

        return columns, _build_schema_index(indices, **multiindex_kwargs)

    @classmethod
    def _get_model_attrs(cls) -> Dict[str, Any]:
        """Return all attributes.
        Similar to inspect.get_members but bypass descriptors __get__.
        """
        bases = inspect.getmro(cls)[:-1]  # bases -> SchemaModel -> object
        attrs = {}
        for base in reversed(bases):
            attrs.update(base.__dict__)
        return attrs

    @classmethod
    def _collect_fields(cls) -> Dict[str, Tuple[AnnotationInfo, FieldInfo]]:
        """Centralize publicly named fields and their corresponding annotations."""
        annotations = get_type_hints(  # pylint:disable=unexpected-keyword-arg
            cls, include_extras=True
        )
        attrs = cls._get_model_attrs()

        missing = []
        for name, attr in attrs.items():
            if inspect.isroutine(attr):
                continue
            if name.startswith("_") or name == _CONFIG_KEY:
                # ignore private and reserved keywords
                annotations.pop(name, None)
            elif name not in annotations:
                missing.append(name)

        if missing:
            raise SchemaInitError(f"Found missing annotations: {missing}")

        fields = {}
        for field_name, annotation in annotations.items():
            field = attrs[field_name]  # __init_subclass__ guarantees existence
            if not isinstance(field, FieldInfo):
                raise SchemaInitError(
                    f"'{field_name}' can only be assigned a 'Field', "
                    + f"not a '{type(field)}.'"
                )
            fields[field.name] = (AnnotationInfo(annotation), field)
        return fields

    @classmethod
    def _collect_config(cls) -> Type[BaseConfig]:
        """Collect config options from bases."""
        bases = inspect.getmro(cls)[:-1]
        bases = typing.cast(Tuple[Type[SchemaModel]], bases)
        root_model, *models = reversed(bases)

        options = _extract_config_options(root_model.Config)
        for model in models:
            config = getattr(model, _CONFIG_KEY, {})
            base_options = _extract_config_options(config)
            options.update(base_options)
        return type("Config", (BaseConfig,), options)

    @classmethod
    def _collect_check_infos(cls, key: str) -> List[CheckInfo]:
        """Collect inherited check metadata from bases.
        Inherited classmethods are not in cls.__dict__, that's why we need to
        walk the inheritance tree.
        """
        bases = inspect.getmro(cls)[:-2]  # bases -> SchemaModel -> object
        bases = typing.cast(Tuple[Type[SchemaModel]], bases)

        method_names = set()
        check_infos = []
        for base in bases:
            for attr_name, attr_value in vars(base).items():
                check_info = getattr(attr_value, key, None)
                if not isinstance(check_info, CheckInfo):
                    continue
                if attr_name in method_names:  # check overridden by subclass
                    continue
                method_names.add(attr_name)
                check_infos.append(check_info)
        return check_infos

    @classmethod
    def _extract_checks(
        cls, check_infos: List[FieldCheckInfo], field_names: List[str]
    ) -> Dict[str, List[Check]]:
        """Collect field annotations from bases in mro reverse order."""
        checks: Dict[str, List[Check]] = {}
        for check_info in check_infos:
            check_info_fields = {
                field.name if isinstance(field, FieldInfo) else field
                for field in check_info.fields
            }
            if check_info.regex:
                matched = _regex_filter(field_names, check_info_fields)
            else:
                matched = check_info_fields

            check_ = check_info.to_check(cls)

            for field in matched:
                if field not in field_names:
                    raise SchemaInitError(
                        f"Check {check_.name} is assigned to a non-existing field '{field}'."
                    )
                if field not in checks:
                    checks[field] = []
                checks[field].append(check_)
        return checks

    @classmethod
    def _extract_df_checks(cls, check_infos: List[CheckInfo]) -> List[Check]:
        """Collect field annotations from bases in mro reverse order."""
        return [check_info.to_check(cls) for check_info in check_infos]


def _build_schema_index(
    indices: List[schema_components.Index], **multiindex_kwargs: Any
) -> Optional[SchemaIndex]:
    index: Optional[SchemaIndex] = None
    if indices:
        if len(indices) == 1:
            index = indices[0]
        else:
            index = schema_components.MultiIndex(indices, **multiindex_kwargs)
    return index


def _regex_filter(seq: Iterable, regexps: Iterable[str]) -> Set[str]:
    """Filter items matching at least one of the regexes."""
    matched: Set[str] = set()
    for regex in regexps:
        pattern = re.compile(regex)
        matched.update(filter(pattern.match, seq))
    return matched


def _get_dtype_kwargs(annotation: AnnotationInfo) -> Dict[str, Any]:
    dtype_arg_names = list(inspect.signature(annotation.arg).parameters.keys())
    if len(annotation.metadata) != len(dtype_arg_names):
        raise TypeError(
            f"Annotation '{annotation.arg.__name__}' requires "
            + f"all positional arguments {dtype_arg_names}."
        )
    return dict(zip(dtype_arg_names, annotation.metadata))
