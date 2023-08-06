"""Components used in pandera schemas."""

import warnings
from copy import copy, deepcopy
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from . import errors
from . import strategies as st
from .error_handlers import SchemaErrorHandler
from .schemas import (
    CheckList,
    DataFrameSchema,
    PandasDtypeInputTypes,
    SeriesSchemaBase,
)


def _is_valid_multiindex_tuple_str(x: Tuple[Any]) -> bool:
    """Check that a multi-index tuple key has all string elements"""
    return isinstance(x, tuple) and all(isinstance(i, str) for i in x)


class Column(SeriesSchemaBase):
    """Validate types and properties of DataFrame columns."""

    has_subcomponents = False

    def __init__(
        self,
        pandas_dtype: PandasDtypeInputTypes = None,
        checks: CheckList = None,
        nullable: bool = False,
        allow_duplicates: bool = True,
        coerce: bool = False,
        required: bool = True,
        name: str = None,
        regex: bool = False,
    ) -> None:
        """Create column validator object.

        :param pandas_dtype: datatype of the column. A ``PandasDtype`` for
            type-checking dataframe. If a string is specified, then assumes
            one of the valid pandas string values:
            http://pandas.pydata.org/pandas-docs/stable/basics.html#dtypes
        :param checks: checks to verify validity of the column
        :param nullable: Whether or not column can contain null values.
        :param allow_duplicates: Whether or not column can contain duplicate
            values.
        :param coerce: If True, when schema.validate is called the column will
            be coerced into the specified dtype.
        :param required: Whether or not column is allowed to be missing
        :param name: column name in dataframe to validate.
        :param regex: whether the ``name`` attribute should be treated as a
            regex pattern to apply to multiple columns in a dataframe.
        :raises SchemaInitError: if impossible to build schema from parameters

        :example:

        >>> import pandas as pd
        >>> import pandera as pa
        >>>
        >>>
        >>> schema = pa.DataFrameSchema({
        ...     "column": pa.Column(pa.String)
        ... })
        >>>
        >>> schema.validate(pd.DataFrame({"column": ["foo", "bar"]}))
          column
        0    foo
        1    bar

        See :ref:`here<column>` for more usage details.
        """
        super().__init__(
            pandas_dtype, checks, nullable, allow_duplicates, coerce
        )
        if (
            name is not None
            and not isinstance(name, str)
            and not _is_valid_multiindex_tuple_str(name)
            and regex
        ):
            raise ValueError(
                "You cannot specify a non-string name when setting regex=True"
            )
        self.required = required
        self._name = name
        self._regex = regex

        if coerce and self._pandas_dtype is None:
            raise errors.SchemaInitError(
                "Must specify dtype if coercing a Column's type"
            )

    @property
    def regex(self) -> bool:
        """True if ``name`` attribute should be treated as a regex pattern."""
        return self._regex

    @property
    def _allow_groupby(self) -> bool:
        """Whether the schema or schema component allows groupby operations."""
        return True

    @property
    def properties(self) -> Dict[str, Any]:
        """Get column properties."""
        return {
            "pandas_dtype": self._pandas_dtype,
            "checks": self._checks,
            "nullable": self._nullable,
            "allow_duplicates": self._allow_duplicates,
            "coerce": self._coerce,
            "required": self.required,
            "name": self._name,
            "regex": self._regex,
        }

    def set_name(self, name: str):
        """Used to set or modify the name of a column object.

        :param str name: the name of the column object

        """
        if (
            not isinstance(name, str)
            and not _is_valid_multiindex_tuple_str(name)
            and self.regex
        ):
            raise ValueError(
                "You cannot specify a non-string name when setting regex=True"
            )
        self._name = name
        return self

    def coerce_dtype(self, obj: Union[pd.DataFrame, pd.Series, pd.Index]):
        """Coerce dtype of a column, handling duplicate column names."""
        # pylint: disable=super-with-arguments
        if isinstance(obj, (pd.Series, pd.Index)):
            return super(Column, self).coerce_dtype(obj)
        return obj.apply(
            lambda x: super(Column, self).coerce_dtype(x), axis="columns"
        )

    def validate(
        self,
        check_obj: pd.DataFrame,
        head: Optional[int] = None,
        tail: Optional[int] = None,
        sample: Optional[int] = None,
        random_state: Optional[int] = None,
        lazy: bool = False,
        inplace: bool = False,
    ) -> pd.DataFrame:
        """Validate a Column in a DataFrame object.

        :param check_obj: pandas DataFrame to validate.
        :param head: validate the first n rows. Rows overlapping with `tail` or
            `sample` are de-duplicated.
        :param tail: validate the last n rows. Rows overlapping with `head` or
            `sample` are de-duplicated.
        :param sample: validate a random sample of n rows. Rows overlapping
            with `head` or `tail` are de-duplicated.
        :param random_state: random seed for the ``sample`` argument.
        :param lazy: if True, lazily evaluates dataframe against all validation
            checks and raises a ``SchemaErrors``. Otherwise, raise
            ``SchemaError`` as soon as one occurs.
        :param inplace: if True, applies coercion to the object of validation,
            otherwise creates a copy of the data.
        :returns: validated DataFrame.
        """
        if not inplace:
            check_obj = check_obj.copy()

        if self._name is None:
            raise errors.SchemaError(
                self,
                check_obj,
                "column name is set to None. Pass the ``name` argument when "
                "initializing a Column object, or use the ``set_name`` "
                "method.",
            )

        def validate_column(check_obj, column_name):
            super(Column, copy(self).set_name(column_name)).validate(
                check_obj,
                head,
                tail,
                sample,
                random_state,
                lazy,
                inplace=inplace,
            )

        column_keys_to_check = (
            self.get_regex_columns(check_obj.columns)
            if self._regex
            else [self._name]
        )

        for column_name in column_keys_to_check:
            if self.coerce:
                check_obj.loc[:, column_name] = self.coerce_dtype(
                    check_obj.loc[:, column_name]
                )
            if isinstance(check_obj[column_name], pd.DataFrame):
                for i in range(check_obj[column_name].shape[1]):
                    validate_column(
                        check_obj[column_name].iloc[:, [i]], column_name
                    )
            else:
                validate_column(check_obj, column_name)

        return check_obj

    def get_regex_columns(
        self, columns: Union[pd.Index, pd.MultiIndex]
    ) -> Union[pd.Index, pd.MultiIndex]:
        """Get matching column names based on regex column name pattern.

        :param columns: columns to regex pattern match
        :returns: matchin columns
        """
        if isinstance(self.name, tuple):
            # handle MultiIndex case
            if len(self.name) != columns.nlevels:
                raise IndexError(
                    "Column regex name='%s' is a tuple, expected a MultiIndex "
                    "columns with %d number of levels, found %d level(s)"
                    % (self.name, len(self.name), columns.nlevels)
                )
            matches = np.ones(len(columns)).astype(bool)
            for i, name in enumerate(self.name):
                matched = pd.Index(
                    columns.get_level_values(i).str.match(name)
                ).fillna(False)
                matches = matches & np.array(matched.tolist())
            column_keys_to_check = columns[matches]
        else:
            if isinstance(columns, pd.MultiIndex):
                raise IndexError(
                    "Column regex name %s is a string, expected a dataframe "
                    "where the index is a pd.Index object, not a "
                    "pd.MultiIndex object" % (self.name)
                )
            column_keys_to_check = columns[
                # str.match will return nan values when the index value is
                # not a string.
                pd.Index(columns.str.match(self.name))
                .fillna(False)
                .tolist()
            ]
        if column_keys_to_check.shape[0] == 0:
            raise errors.SchemaError(
                self,
                columns,
                "Column regex name='%s' did not match any columns in the "
                "dataframe. Update the regex pattern so that it matches at "
                "least one column:\n%s" % (self.name, columns.tolist()),
            )
        # drop duplicates to account for potential duplicated columns in the
        # dataframe.
        return column_keys_to_check.drop_duplicates()

    @st.strategy_import_error
    def strategy(self, *, size=None):
        """Create a ``hypothesis`` strategy for generating a Column.

        :param size: number of elements to generate
        :returns: a dataframe strategy for a single column.
        """
        return super().strategy(size=size).map(lambda x: x.to_frame())

    @st.strategy_import_error
    def strategy_component(self):
        """Generate column data object for use by DataFrame strategy."""
        return st.column_strategy(
            self.pdtype,
            checks=self.checks,
            allow_duplicates=self.allow_duplicates,
            name=self.name,
        )

    def example(self, size=None) -> pd.DataFrame:
        """Generate an example of a particular size.

        :param size: number of elements in the generated Index.
        :returns: pandas DataFrame object.
        """
        # pylint: disable=import-outside-toplevel,cyclic-import,import-error
        import hypothesis

        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                category=hypothesis.errors.NonInteractiveExampleWarning,
            )
            return (
                super()
                .strategy(size=size)
                .example()
                .rename(self.name)
                .to_frame()
            )

    def __eq__(self, other):
        def _compare_dict(obj):
            return {
                k: v if k != "_checks" else set(v)
                for k, v in obj.__dict__.items()
            }

        return _compare_dict(self) == _compare_dict(other)


class Index(SeriesSchemaBase):
    """Validate types and properties of a DataFrame Index."""

    has_subcomponents = False

    @property
    def names(self):
        """Get index names in the Index schema component."""
        return [self.name]

    @property
    def _allow_groupby(self) -> bool:
        """Whether the schema or schema component allows groupby operations."""
        return False

    def validate(
        self,
        check_obj: Union[pd.DataFrame, pd.Series],
        head: Optional[int] = None,
        tail: Optional[int] = None,
        sample: Optional[int] = None,
        random_state: Optional[int] = None,
        lazy: bool = False,
        inplace: bool = False,
    ) -> Union[pd.DataFrame, pd.Series]:
        """Validate DataFrameSchema or SeriesSchema Index.

        :check_obj: pandas DataFrame of Series containing index to validate.
        :param head: validate the first n rows. Rows overlapping with `tail` or
            `sample` are de-duplicated.
        :param tail: validate the last n rows. Rows overlapping with `head` or
            `sample` are de-duplicated.
        :param sample: validate a random sample of n rows. Rows overlapping
            with `head` or `tail` are de-duplicated.
        :param random_state: random seed for the ``sample`` argument.
        :param lazy: if True, lazily evaluates dataframe against all validation
            checks and raises a ``SchemaErrors``. Otherwise, raise
            ``SchemaError`` as soon as one occurs.
        :param inplace: if True, applies coercion to the object of validation,
            otherwise creates a copy of the data.
        :returns: validated DataFrame or Series.
        """
        if self.coerce:
            check_obj.index = self.coerce_dtype(check_obj.index)
            # handles case where pandas native string type is not supported
            # by index.
            obj_to_validate = pd.Series(
                check_obj.index, name=check_obj.index.name
            ).astype(self.dtype)
        else:
            obj_to_validate = pd.Series(
                check_obj.index, name=check_obj.index.name
            )

        assert isinstance(
            super().validate(
                obj_to_validate,
                head,
                tail,
                sample,
                random_state,
                lazy,
                inplace,
            ),
            pd.Series,
        )
        return check_obj

    @st.strategy_import_error
    def strategy(self, *, size: int = None):
        """Create a ``hypothesis`` strategy for generating an Index.

        :param size: number of elements to generate.
        :returns: index strategy.
        """
        return st.index_strategy(
            self.pdtype,  # type: ignore
            checks=self.checks,
            nullable=self.nullable,
            allow_duplicates=self.allow_duplicates,
            name=self.name,
            size=size,
        )

    @st.strategy_import_error
    def strategy_component(self):
        """Generate column data object for use by MultiIndex strategy."""
        return st.column_strategy(
            self.pdtype,
            checks=self.checks,
            allow_duplicates=self.allow_duplicates,
            name=self.name,
        )

    def example(self, size: int = None) -> pd.Index:
        """Generate an example of a particular size.

        :param size: number of elements in the generated Index.
        :returns: pandas Index object.
        """
        # pylint: disable=import-outside-toplevel,cyclic-import,import-error
        import hypothesis

        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                category=hypothesis.errors.NonInteractiveExampleWarning,
            )
            return self.strategy(size=size).example()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class MultiIndex(DataFrameSchema):
    """Validate types and properties of a DataFrame MultiIndex.

    This class inherits from :class:`~pandera.schemas.DataFrameSchema` to
    leverage its validation logic.
    """

    has_subcomponents = True

    def __init__(
        self,
        indexes: List[Index],
        coerce: bool = False,
        strict: bool = False,
        name: str = None,
        ordered: bool = True,
    ) -> None:
        """Create MultiIndex validator.

        :param indexes: list of Index validators for each level of the
            MultiIndex index.
        :param coerce: Whether or not to coerce the MultiIndex to the
            specified pandas_dtypes before validation
        :param strict: whether or not to accept columns in the MultiIndex that
            aren't defined in the ``indexes`` argument.
        :param name: name of schema component
        :param ordered: whether or not to validate the indexes order.

        :example:

        >>> import pandas as pd
        >>> import pandera as pa
        >>>
        >>>
        >>> schema = pa.DataFrameSchema(
        ...     columns={"column": pa.Column(pa.Int)},
        ...     index=pa.MultiIndex([
        ...         pa.Index(pa.String,
        ...               pa.Check(lambda s: s.isin(["foo", "bar"])),
        ...               name="index0"),
        ...         pa.Index(pa.Int, name="index1"),
        ...     ])
        ... )
        >>>
        >>> df = pd.DataFrame(
        ...     data={"column": [1, 2, 3]},
        ...     index=pd.MultiIndex.from_arrays(
        ...         [["foo", "bar", "foo"], [0, 1, 2]],
        ...         names=["index0", "index1"],
        ...     )
        ... )
        >>>
        >>> schema.validate(df)
                       column
        index0 index1
        foo    0            1
        bar    1            2
        foo    2            3

        See :ref:`here<multiindex>` for more usage details.

        """
        self.indexes = indexes
        columns = {}
        for i, index in enumerate(indexes):
            if not ordered and index.name is None:
                # if the MultiIndex is not ordered, there's no way of
                # determining how to get the index level without an explicit
                # index name
                raise errors.SchemaInitError(
                    "You must specify index names if MultiIndex schema "
                    "component is not ordered."
                )
            columns[i if index.name is None else index.name] = Column(
                pandas_dtype=index._pandas_dtype,
                checks=index.checks,
                nullable=index._nullable,
                allow_duplicates=index._allow_duplicates,
            )
        super().__init__(
            columns=columns,
            coerce=coerce,
            strict=strict,
            name=name,
            ordered=ordered,
        )

    @property
    def names(self):
        """Get index names in the MultiIndex schema component."""
        return [index.name for index in self.indexes]

    @property
    def coerce(self):
        """Whether or not to coerce data types."""
        return self._coerce or any(index.coerce for index in self.indexes)

    @coerce.setter
    def coerce(self, value: bool) -> None:
        """Set coerce attribute."""
        self._coerce = value

    def coerce_dtype(self, obj: pd.MultiIndex) -> pd.MultiIndex:
        """Coerce type of a pd.Series by type specified in pandas_dtype.

        :param obj: multi-index to coerce.
        :returns: ``MultiIndex`` with coerced data type
        """
        error_handler = SchemaErrorHandler(lazy=True)

        # construct MultiIndex with coerced data types
        coerced_multi_index = {}
        for i, index in enumerate(self.indexes):
            if all(x is None for x in self.names):
                index_levels = [i]
            else:
                index_levels = [
                    i for i, name in enumerate(obj.names) if name == index.name
                ]
            for index_level in index_levels:
                index_array = obj.get_level_values(index_level)
                if index.coerce or self._coerce:
                    try:
                        index_array = index.coerce_dtype(index_array)
                    except errors.SchemaError as err:
                        error_handler.collect_error(
                            "dtype_coercion_error", err
                        )
                coerced_multi_index[index_level] = index_array

        if error_handler.collected_errors:
            raise errors.SchemaErrors(error_handler.collected_errors, obj)

        return pd.MultiIndex.from_arrays(
            [
                v
                for k, v in sorted(
                    coerced_multi_index.items(), key=lambda x: x[0]
                )
            ],
            names=obj.names,
        )

    def validate(
        self,
        check_obj: Union[pd.DataFrame, pd.Series],
        head: Optional[int] = None,
        tail: Optional[int] = None,
        sample: Optional[int] = None,
        random_state: Optional[int] = None,
        lazy: bool = False,
        inplace: bool = False,
    ) -> Union[pd.DataFrame, pd.Series]:
        """Validate DataFrame or Series MultiIndex.

        :param check_obj: pandas DataFrame of Series to validate.
        :param head: validate the first n rows. Rows overlapping with `tail` or
            `sample` are de-duplicated.
        :param tail: validate the last n rows. Rows overlapping with `head` or
            `sample` are de-duplicated.
        :param sample: validate a random sample of n rows. Rows overlapping
            with `head` or `tail` are de-duplicated.
        :param random_state: random seed for the ``sample`` argument.
        :param lazy: if True, lazily evaluates dataframe against all validation
            checks and raises a ``SchemaErrors``. Otherwise, raise
            ``SchemaError`` as soon as one occurs.
        :param inplace: if True, applies coercion to the object of validation,
            otherwise creates a copy of the data.
        :returns: validated DataFrame or Series.
        """
        # pylint: disable=too-many-locals
        if self.coerce:
            try:
                check_obj.index = self.coerce_dtype(check_obj.index)
            except errors.SchemaErrors as err:
                if lazy:
                    raise
                raise err.schema_errors[0]["error"] from err

        # Prevent data type coercion when the validate method is called because
        # it leads to some weird behavior when calling coerce_dtype within the
        # DataFrameSchema.validate call. Need to fix this by having MultiIndex
        # not inherit from DataFrameSchema.
        self_copy = deepcopy(self)
        self_copy.coerce = False
        for index in self_copy.indexes:
            index.coerce = False

        # rename integer-based column names in case of duplicate index names,
        # with at least one named index.
        if (
            not all(x is None for x in check_obj.index.names)
            and len(set(check_obj.index.names)) != check_obj.index.nlevels
        ):
            index_names = []
            for i, name in enumerate(check_obj.index.names):
                name = i if name is None else name
                if name not in index_names:
                    index_names.append(name)

            columns = {}
            for name, (_, column) in zip(
                index_names, self_copy.columns.items()
            ):
                columns[name] = column.set_name(name)
            self_copy.columns = columns

        def to_dataframe(multiindex):
            """
            Emulate the behavior of pandas.MultiIndex.to_frame, but preserve
            duplicate index names if they exist.
            """
            df = pd.DataFrame(
                {
                    i: multiindex.get_level_values(i)
                    for i in range(multiindex.nlevels)
                }
            )
            df.columns = [
                i if name is None else name
                for i, name in enumerate(multiindex.names)
            ]
            df.index = multiindex
            return df

        try:
            validation_result = super(MultiIndex, self_copy).validate(
                to_dataframe(check_obj.index),
                head,
                tail,
                sample,
                random_state,
                lazy,
                inplace,
            )
        except errors.SchemaErrors as err:
            # This is a hack to re-raise the SchemaErrors exception and change
            # the schema context to MultiIndex. This should be fixed by with
            # a more principled schema class hierarchy.
            schema_error_dicts = []
            for schema_error_dict in err.schema_errors:
                error = schema_error_dict["error"]
                error = errors.SchemaError(
                    self,
                    check_obj,
                    error.args[0],
                    error.failure_cases.assign(column=error.schema.name),
                    error.check,
                    error.check_index,
                )
                schema_error_dict["error"] = error
                schema_error_dicts.append(schema_error_dict)

            raise errors.SchemaErrors(schema_error_dicts, check_obj)

        assert isinstance(validation_result, pd.DataFrame)
        return check_obj

    @st.strategy_import_error
    # NOTE: remove these ignore statements as part of
    # https://github.com/pandera-dev/pandera/issues/403
    # pylint: disable=arguments-differ
    def strategy(self, *, size=None):  # type: ignore
        return st.multiindex_strategy(indexes=self.indexes, size=size)

    # NOTE: remove these ignore statements as part of
    # https://github.com/pandera-dev/pandera/issues/403
    # pylint: disable=arguments-differ
    def example(self, size=None) -> pd.MultiIndex:  # type: ignore
        # pylint: disable=import-outside-toplevel,cyclic-import,import-error
        import hypothesis

        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                category=hypothesis.errors.NonInteractiveExampleWarning,
            )
            return self.strategy(size=size).example()

    def __repr__(self):
        return (
            f"<Schema {self.__class__.__name__}("
            f"indexes={self.indexes}, "
            f"coerce={self.coerce}, "
            f"strict={self.strict}, "
            f"name={self.name}, "
            f"ordered={self.ordered}"
            ")>"
        )

    def __str__(self):
        indent = " " * 4

        indexes_str = "[\n"
        for index in self.indexes:
            indexes_str += f"{indent * 2}{index}\n"
        indexes_str += f"{indent}]"

        return (
            f"<Schema {self.__class__.__name__}(\n"
            f"{indent}indexes={indexes_str}\n"
            f"{indent}coerce={self.coerce},\n"
            f"{indent}strict={self.strict},\n"
            f"{indent}name={self.name},\n"
            f"{indent}ordered={self.ordered}\n"
            ")>"
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
