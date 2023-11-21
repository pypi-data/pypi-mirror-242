"""
    Xpress Insight Python package
    =============================

    This is an internal file of the 'xpressinsight' package. Do not import it directly.

    This material is the confidential, proprietary, unpublished property
    of Fair Isaac Corporation.  Receipt or possession of this material
    does not convey rights to divulge, reproduce, use, or allow others
    to use it without the specific written authorization of Fair Isaac
    Corporation and use must conform strictly to the license agreement.

    Copyright (c) 2020-2023 Fair Isaac Corporation. All rights reserved.
"""

import os
import sys
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Dict, Union, Type, ValuesView, List, Callable, Iterable, Optional

import numpy as np
import pandas as pd

import xpressinsight.entities as xi_types
from xpressinsight.entities_config import EntitiesContainer
from xpressinsight.interface_rest import AppRestInterface

#
#
#
TABLE_PREFIX_ENTITY = "ENTITY_"

SingleValueDict = Dict[Type[xi_types.BasicType], Dict[str, Any]]
SPType = Union[Type[xi_types.Scalar], Type[xi_types.Param]]

ERR_ABSTRACT = "Cannot call abstract method of base class."


class DataConnector(ABC):
    """
    DataConnector manages interactions between an entity data container (e.g. an application instance) and
    some data store.
    """

    #
    @abstractmethod
    def __init__(self, data_container: EntitiesContainer):
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """ Check if the data store is empty. """

    @abstractmethod
    def clean(self):
        """ Cleans the data store, removing any locally saved files. """

    @abstractmethod
    def initialize_entities(self, entity_filter: Callable[[xi_types.Entity], bool]):
        """ Initialize all entities matching the given filter to suitable default values. """

    @abstractmethod
    def load_entities(self, entity_filter: Callable[[xi_types.Entity], bool]):
        """ Load all entities matching the filter from the data-store. """

    @abstractmethod
    def save_entities(self, entity_filter: Callable[[xi_types.Entity], bool]):
        """ Save all entities matching the filter to the data-store. """

    @abstractmethod
    def load_meta(self) -> SingleValueDict:
        """ Returns the meta-data from the data store. """


class TableConnector(DataConnector):
    """
    TableConnector - DataConnector implementation in which all the entity data is read from/written to flat tables.
    """

    def __init__(self, data_container: EntitiesContainer, fetch_individual_series=True):
        super().__init__(data_container)
        self._data_container = data_container
        self._verbose: bool = False
        #
        #
        self._fetch_individual_series: bool = fetch_individual_series

    @staticmethod
    def _encode_identifier(ident: str) -> str:
        """
        Encode a valid identifier (table or column name) so that it can be used in a case-insensitive environment
        (e.g. as an NTFS file name or in an SQL database).
        """
        tail = (
            np.packbits([int(c.isupper()) for c in ident], bitorder="little").tobytes().hex()
        )
        return f"{ident}_{tail}"

    @abstractmethod
    def _get_export_type(self, src_type: Type[xi_types.BasicType]) -> str:
        raise RuntimeError(ERR_ABSTRACT)

    @staticmethod
    def _get_import_type(dtype):
        #
        if pd.api.types.is_integer_dtype(dtype):
            return xi_types.BASIC_PANDAS_DTYPE_MAP[xi_types.integer]
        if pd.api.types.is_bool_dtype(dtype):
            return xi_types.BASIC_PANDAS_DTYPE_MAP[xi_types.boolean]
        if pd.api.types.is_float_dtype(dtype):
            return xi_types.BASIC_PANDAS_DTYPE_MAP[xi_types.real]
        if pd.api.types.is_string_dtype(dtype):
            return xi_types.BASIC_PANDAS_DTYPE_MAP[xi_types.string]

        raise RuntimeError(f"Unrecognized index type {dtype}")

    @abstractmethod
    def _encode_column_name(self, ident: str) -> str:
        raise RuntimeError(ERR_ABSTRACT)

    @abstractmethod
    def _decode_column_name(self, ident: str) -> str:
        raise RuntimeError(ERR_ABSTRACT)

    def _encode_table_name(self, name) -> str:
        return TABLE_PREFIX_ENTITY + self._encode_identifier(name)

    def _encode_df_table_name(self, name: str, column: str) -> str:
        """Encode the table name for a DataFrame column"""
        return TABLE_PREFIX_ENTITY + self._encode_identifier(name + "_" + column)

    def _encode_df_column_name(self, name: str, column: str) -> str:
        """Encode the name of the column for a DataFrame"""
        return self._encode_column_name(name + "_" + column)

    @staticmethod
    def _sp_table_name(sp_type: SPType, dtype: Type[xi_types.BasicType]) -> str:
        """Returns the table name"""
        return sp_type.__name__.upper() + "_" + dtype.__name__

    @staticmethod
    def _get_entities(data_container, entity_filter: Callable[[xi_types.Entity], bool] = None
                      ) -> Iterable[xi_types.EntityBase]:
        """
        Get the entities list for the given container.  Error if it doesn't have one.
        If filter is supplied, returns list of entities that pass the filter.
        A DataFrame entity will pass the filter if any of its columns pass the filter.
        """
        if not entity_filter:
            return data_container.get_entities_cfg().entities

        entities: List[xi_types.EntityBase] = []
        for entity in data_container.get_entities_cfg().entities:
            if isinstance(entity, xi_types.DataFrame):
                if any(entity_filter(col) for col in entity.columns):
                    entities.append(entity)
            elif entity_filter(entity):
                entities.append(entity)

        return entities

    def _get_empty_index_for_frame_with_undeclared_indices(self, df: pd.DataFrame,
                                                           columns: Iterable[xi_types.Column]) -> pd.Index:
        """ Given an entity which doesn't declare index names, create a suitable empty index from the columns
            of the input frame that do not match entries in the 'columns' array """
        non_index_column_names = {self._encode_column_name(c.name) for c in columns}
        index_names = [self._decode_column_name(name) for name in df.columns.to_list()
                       if name not in non_index_column_names]

        index_list = [
            pd.Index([], dtype=TableConnector._get_import_type(df[index_name].dtype), name=index_name)
            for index_name in index_names
        ]

        if len(index_list) == 1:
            pd_index = index_list[0]
        else:
            pd_index = pd.MultiIndex.from_product(index_list)

        return pd_index

    def _load_single_values_db(self, prefix: str) -> SingleValueDict:
        """Loads from the database and returns SingleValueDict"""

        assert prefix in ("SCALAR", "PARAM", "META")

        values = {}

        for dtype in xi_types.ALL_BASIC_TYPE:
            table_name = f"{prefix}_{dtype.__name__}"

            if self._has_table(table_name):
                df = self._import_table(table_name)

                if ("Name" not in df.columns) or ("Value" not in df.columns):
                    raise KeyError(f"Table {table_name} must have 'Name' and 'Value' columns, it has {df.columns}.")

                values[dtype] = dict(zip(df["Name"], df["Value"]))
            else:
                values[dtype] = {}

        #
        values[xi_types.boolean] = {
            name: xi_types.python_int_to_bool(value)
            for name, value in values[xi_types.boolean].items()
        }

        return values

    def _save_single_values_db(self, prefix: str, values: SingleValueDict):
        """Saves SingleValueDict to the database"""

        assert prefix in ("SCALAR", "PARAM", "META")

        for dtype in xi_types.ALL_BASIC_TYPE:
            #
            if dtype in values and values[dtype]:
                table_name = f"{prefix}_{dtype.__name__}"

                df = pd.DataFrame(
                    values[dtype].items(), columns=["Name", "Value"]
                ).set_index("Name")
                dtypes = {
                    "Name": self._get_export_type(xi_types.string),
                    "Value": self._get_export_type(dtype),
                }
                self._export_table(df, table_name, dtype=dtypes, data_col_nullable=False)

    def initialize_entities(self, entity_filter: Callable[[xi_types.Entity], bool]):
        """
        Initializes the values of the entities of the given container that match the given filter, to the
        appropriate default value.
        Currently only supports initializing scalar entities.
        """
        for entity in TableConnector._get_entities(self._data_container, entity_filter):
            if isinstance(entity, xi_types.ScalarBase):
                self._data_container.__dict__[entity.name] = entity.default
            else:
                #
                raise RuntimeError("Initialize non-scalar entities not supported at this time.")

    def load_meta(self) -> SingleValueDict:
        return self._load_single_values_db('META')

    def _load_scalars(self, data_container, entities: Iterable[xi_types.ScalarBase], table_prefix: str):
        """
        Given a collection of scalar-type entities, load the values from the given table prefix
        """
        values_by_type = self._load_single_values_db(table_prefix)

        #
        values: Dict[str, Any] = {}
        for values_of_type in values_by_type.values():
            for (name, value) in values_of_type.items():
                if name in values:
                    raise KeyError(f"Multiple values found for {name} in single-values db")

                values[name] = value

        #
        for entity in entities:
            if entity.entity_name not in values:
                raise ValueError(f"{'Parameter' if entity.dtype == xi_types.Param else 'Scalar'} "
                                 f"{entity.entity_name} (of type {entity.dtype.__name__}) does not exist in the "
                                 f"data store.")

            value = values[entity.entity_name]

            xi_types.check_type(value, entity)
            data_container.__dict__[entity.name] = value

    def _load_index(self, data_container, entity: xi_types.Index):
        """ Load a given index-type entity into the data container. """
        table_name = self._encode_table_name(entity.name)
        df = self._import_table(table_name)
        df.columns = [self._decode_column_name(c) for c in df.columns]

        value = df.set_index(entity.name).index
        xi_types.check_type(value, entity)
        data_container.__dict__[entity.name] = value

    def _load_series(self, data_container, entity: xi_types.Series):
        """ Load a given series-type entity into the data container. """
        table_name = self._encode_table_name(entity.name)
        df = self._import_table(table_name)
        df.columns = [self._decode_column_name(c) for c in df.columns]

        #
        #
        index_names = entity.unique_index_names or\
            [col for col in df.columns if col != entity.series_name]

        value = df.set_index(index_names)[entity.series_name]
        xi_types.check_type(value, entity)
        data_container.__dict__[entity.name] = value

    @staticmethod
    def _get_column_default_value(col: xi_types.Column, series: pd.Series) -> Optional[Union[bool, int, str, float]]:
        """ Determine the default value to use for the given column. """
        #
        if col.default is not None:
            return col.default

        #
        assert col.dtype is None

        #
        if pd.api.types.is_bool_dtype(series.dtype):
            return xi_types.SCALAR_DEFAULT_VALUES[xi_types.boolean]

        if pd.api.types.is_float_dtype(series.dtype):
            return xi_types.SCALAR_DEFAULT_VALUES[xi_types.real]

        if pd.api.types.is_string_dtype(series.dtype):
            return xi_types.SCALAR_DEFAULT_VALUES[xi_types.string]

        if pd.api.types.is_integer_dtype(series.dtype):
            return xi_types.SCALAR_DEFAULT_VALUES[xi_types.integer]

        return None  #

    def _import_data_frame_from_single_table(self, entity: xi_types.DataFrame,
                                             columns: Iterable[xi_types.Column]) -> pd.DataFrame:
        """ Import a data from from a single, multi-column table. """
        table_name = self._encode_table_name(entity.name)
        df = self._import_table(table_name)

        #
        if entity.index_names:
            encoded_index_names = [self._encode_column_name(name) for name in entity.unique_index_names]

        #
        else:
            non_index_column_names = {self._encode_column_name(c.name) for c in columns}
            encoded_index_names = [name for name in df.columns.to_list()
                                   if name not in non_index_column_names]

        #
        df.set_index(encoded_index_names, inplace=True)

        #
        return df

    def _import_data_frame_from_multiple_tables(self, entity: xi_types.DataFrame,
                                                columns: Iterable[xi_types.Column]) -> pd.DataFrame:
        """ Import a data frame from multiple tables, each containing a single series. """
        #
        if entity.index_names:
            #
            index_rename_map = {
                self._encode_column_name(index_name): index_name for index_name in entity.unique_index_names
            }
            pd_index = xi_types.data_frame_get_empty_index(entity)
            index_names = pd_index.names

        else:
            #
            #
            index_rename_map = {}
            pd_index = None
            index_names = None

        #
        data: dict[str, pd.Series] = {}
        for c in columns:
            table_name = self._encode_df_table_name(entity.name, c.name)
            encoded_data_col_name = self._encode_df_column_name(entity.name, c.name)

            df = self._import_table(table_name)

            #
            if pd_index is None:
                pd_index = self._get_empty_index_for_frame_with_undeclared_indices(df, columns)
                index_names = pd_index.names
                index_rename_map = {
                    index_name: self._decode_column_name(index_name) for index_name in index_names
                }

            if index_rename_map:
                df.rename(columns=index_rename_map, inplace=True)

            #
            df.set_index(index_names, inplace=True)

            #
            data[c.name] = df[encoded_data_col_name]

        #
        for c in columns:
            pd_index = pd_index.union(data[c.name].index)

        #
        #
        #
        for c in columns:
            data[c.name] = data[c.name].reindex(pd_index,
                                                fill_value=TableConnector._get_column_default_value(c, data[c.name]))

        #
        df_full = pd.DataFrame(data, index=pd_index)
        return df_full

    def _load_data_frame(self, data_container, entity: xi_types.DataFrame, columns: Iterable[xi_types.Column]):
        if self._fetch_individual_series:
            df = self._import_data_frame_from_multiple_tables(entity, columns)
        else:
            df = self._import_data_frame_from_single_table(entity, columns)

        #
        unique_index_names = entity.unique_index_names
        if unique_index_names:
            df.index.rename(list(unique_index_names)[0] if len(unique_index_names) == 1 else unique_index_names,
                            inplace=True)

        #
        column_rename_map = {
            df_col_name: entity_col.name for (df_col_name, entity_col) in zip(df.columns, columns)
        }
        df.rename(columns=column_rename_map, inplace=True)

        #
        #
        if entity.name in self._data_container.__dict__:
            df_org = self._data_container.__dict__[entity.name]

            if isinstance(df_org, pd.DataFrame):
                for col_label, col in df_org.items():
                    #
                    if col_label not in df.columns:
                        #
                        #
                        #
                        #
                        df[col_label] = col

        #
        xi_types.check_type(df, entity, columns=columns)
        data_container.__dict__[entity.name] = df

    def load_entities(self, entity_filter: Callable[[xi_types.Entity], bool]):
        """
        Load the given entities into the given data container into the given data store.
        """
        with self._connect():
            param_entities: List[xi_types.Param] = []
            scalar_entities: List[xi_types.Scalar] = []
            for entity in TableConnector._get_entities(self._data_container, entity_filter):
                if isinstance(entity, xi_types.Param):
                    #
                    param_entities.append(entity)

                elif isinstance(entity, xi_types.Scalar):
                    #
                    scalar_entities.append(entity)

                elif isinstance(entity, xi_types.Index):
                    self._load_index(self._data_container, entity)

                elif isinstance(entity, xi_types.Series):
                    self._load_series(self._data_container, entity)

                elif isinstance(entity, xi_types.DataFrame):
                    self._load_data_frame(self._data_container, entity,
                                          [col for col in entity.columns if entity_filter(col)])

                else:
                    raise RuntimeError(f"Unable to load unrecognized entity type {entity.__class__.name} "
                                       f"for entity {entity.name}")

            #
            if param_entities:
                self._load_scalars(self._data_container, param_entities, 'PARAM')
            if scalar_entities:
                self._load_scalars(self._data_container, scalar_entities, 'SCALAR')

    @abstractmethod
    def _does_db_exist(self) -> bool:
        """ Returns True iff data repository directory exists. """
        raise RuntimeError(ERR_ABSTRACT)

    @abstractmethod
    def _check_db_exists(self):
        raise RuntimeError(ERR_ABSTRACT)

    @abstractmethod
    def _has_table(self, table_name: str) -> bool:
        """ Returns True iff given table exists in data repository. """
        raise RuntimeError(ERR_ABSTRACT)

    @abstractmethod
    def _import_table(self, table_name: str) -> pd.DataFrame:
        raise RuntimeError(ERR_ABSTRACT)

    @abstractmethod
    def _export_table(self, df: Union[pd.DataFrame, pd.Series], table_name: str, dtype: Dict[str, str],
                      index: bool = True, data_col_nullable: bool = False):
        raise RuntimeError(ERR_ABSTRACT)

    def _save_scalars(self, entity_values: SingleValueDict, table_prefix: str):
        """
        Given a collection of values from scalar-type entities (Scalar or Param), save these values to the given
        table prefix.
        The caller will already have populated `entity_values` with the values for the entities they want to save.
        """
        self._save_single_values_db(table_prefix, entity_values)

    def _save_index(self, entity: xi_types.Index, value: pd.Index):
        """ Write the value of the given index entity to the data store. """
        ser = value.to_series()
        ser.name = self._encode_column_name(entity.name)
        dtype = {ser.name: self._get_export_type(entity.dtype)}
        table_name = self._encode_table_name(entity.name)

        self._export_table(ser, table_name, index=False, dtype=dtype, data_col_nullable=False)

    def _save_series(self, entity: xi_types.Series, value: pd.Series):
        """ Write the value of the given series to the data store. """
        original_name = value.name
        original_index_names = value.index.names
        try:
            enc_col_name = self._encode_column_name(entity.name)
            value.name = enc_col_name
            value.index.names = [self._encode_column_name(index_label) for index_label in entity.unique_index_names]
            dtype = {
                self._encode_column_name(index_label): self._get_export_type(ind.dtype)
                for (index_label, ind) in zip(entity.unique_index_names, entity.index)
            }
            dtype[enc_col_name] = self._get_export_type(entity.dtype)
            table_name = self._encode_table_name(entity.name)

            self._export_table(value, table_name, dtype=dtype, data_col_nullable=True)
        finally:
            value.name = original_name
            value.index.names = original_index_names

    def _save_data_frame(self, entity: xi_types.DataFrame, value: pd.DataFrame, columns: Iterable[xi_types.Column]):
        """ Write the value of the given columns of the given data-frame to the data store. """
        if not self._fetch_individual_series:
            #
            #
            #
            raise RuntimeError("Frames may only be stored as one series per table.")

        for c in columns:
            #
            ser = value[c.name]
            original_name = ser.name
            original_index_names = ser.index.names

            try:
                #
                enc_col_name = self._encode_df_column_name(entity.name, c.name)
                ser.name = enc_col_name
                ser.index.names = [self._encode_column_name(index_label) for index_label in entity.unique_index_names]
                dtype = {
                    self._encode_column_name(index_label): self._get_export_type(ind.dtype)
                    for (index_label, ind) in zip(entity.unique_index_names, entity.index)
                }
                dtype[enc_col_name] = self._get_export_type(c.dtype)
                table_name = self._encode_table_name(c.entity_name)

                self._export_table(ser, table_name, dtype=dtype, data_col_nullable=True)
            finally:
                ser.name = original_name
                ser.index.names = original_index_names

    def save_entities(self, entity_filter: Callable[[xi_types.Entity], bool]):
        """ Write the given entities of the given container to the data store. """
        #
        exceptions: List[BaseException] = []

        with self._connect():
            #
            scalar_values: SingleValueDict = {dtype: {} for dtype in xi_types.ALL_BASIC_TYPE}
            parameter_values: SingleValueDict = {dtype: {} for dtype in xi_types.ALL_BASIC_TYPE}

            for entity in TableConnector._get_entities(self._data_container, entity_filter):
                try:
                    if entity.name not in self._data_container.__dict__:
                        raise KeyError(f"Entity {entity.name} declared but not initialized.")

                    entity_value = self._data_container.__dict__[entity.name]

                    if isinstance(entity, xi_types.Param):
                        xi_types.check_type(entity_value, entity)
                        parameter_values[entity.dtype][entity.name] = entity_value

                    elif isinstance(entity, xi_types.Scalar):
                        xi_types.check_type(entity_value, entity)
                        scalar_values[entity.dtype][entity.name] = entity_value

                    elif isinstance(entity, xi_types.Index):
                        xi_types.check_type(entity_value, entity)
                        self._save_index(entity, entity_value)

                    elif isinstance(entity, xi_types.Series):
                        xi_types.check_type(entity_value, entity)
                        self._save_series(entity, entity_value)

                    elif isinstance(entity, xi_types.DataFrame):
                        columns = [col for col in entity.columns if entity_filter(col)]
                        xi_types.check_type(entity_value, entity, columns=columns)
                        self._save_data_frame(entity, entity_value, columns)

                except BaseException as e:  #
                    #
                    #
                    print(f"ERROR: {type(self).__name__} failed to save entity {entity.name} for reason: "
                          f"{e.__class__}: {e}", file=sys.stderr)
                    exceptions.append(e)

            #
            try:
                self._save_scalars(parameter_values, 'PARAM')
            except BaseException as e:  #
                #
                #
                print(f"ERROR: {type(self).__name__} failed to save parameters for reason: "
                      f"{e.__class__}: {e}", file=sys.stderr)
                exceptions.append(e)

            try:
                self._save_scalars(scalar_values, 'SCALAR')
            except BaseException as e:  #
                #
                #
                print(f"ERROR: {type(self).__name__} failed to save scalars for reason: "
                      f"{e.__class__}: {e}", file=sys.stderr)
                exceptions.append(e)

        #
        if exceptions:
            raise exceptions[0]

    @abstractmethod
    @contextmanager
    def _connect(self):
        raise RuntimeError(ERR_ABSTRACT)


def input_scalars_filter(entity: xi_types.EntityBase) -> bool:
    """ Filter that accepts only scalar entities that are input and not update-after-execution. """
    return (isinstance(entity, xi_types.Scalar) and
            entity.is_managed(xi_types.Manage.INPUT) and
            not entity.update_after_execution)


class AppDataConnector:
    """
    AppDataConnector performs the requests to load / save the data for the application class as a whole.
    It does not subclass DataConnector, but rather wraps one and converts the higher-level requests made of the
    app (e.g. load input entities) to lower-level requests to the table connector (e.g. load these specific
    entities).
    """

    def __init__(self, app, base: DataConnector):
        self._app = app
        self._entities: ValuesView[xi_types.EntityBase] = app.app_cfg.entities
        self._base = base
        self._original_input_only_scalar_values: Optional[Dict[str, Any]] = None

    def _load_meta(self):
        meta_values = self._base.load_meta()

        if isinstance(self._app.insight, AppRestInterface):
            rest_port = meta_values[xi_types.integer]['http_port']
            rest_token = meta_values[xi_types.string]['http_token']
            #
            self._app.insight._init_rest(rest_port, rest_token)

        if 'app_id' in meta_values:
            self._app.insight._app_id = meta_values[xi_types.string]['app_id']

        if 'app_name' in meta_values:
            self._app.insight._app_name = meta_values[xi_types.string]['app_name']

        if 'scenario_id' in meta_values:
            self._app.insight._scenario_id = meta_values[xi_types.string]['scenario_id']

        if 'scenario_name' in meta_values:
            self._app.insight._scenario_name = meta_values[xi_types.string]['scenario_name']

        if 'scenario_path' in meta_values:
            self._app.insight._scenario_path = meta_values[xi_types.string]['scenario_path']

    def _warn_about_work_dir(self):
        if os.path.isdir(self._app.insight.work_dir):
            print("Test mode: Using existing Insight working directory.")

    def _check_base_exists(self):
        if self._base.is_empty():
            raise FileNotFoundError(f'Cannot find data store: "{self._base}".')

    def _get_input_only_scalar_values(self) -> Dict[str, any]:
        """ Capture a dictionary of the input-only scalar values (excluding update-after-execution scalars) in
        the app """
        input_scalar_values = {}
        for e in self._app.app_cfg.entities:
            if input_scalars_filter(e) and e.name in self._app.__dict__:
                input_scalar_values[e.name] = self._app.__dict__[e.name]

        return input_scalar_values

    def clear_input(self):
        """ Clear values of input entities, setting parameters/scalars to default values. """
        if self._app.insight.test_mode:
            self._warn_about_work_dir()
            is_empty_data_repo = self._base.is_empty()

            if is_empty_data_repo:
                print(f'Test mode: Creating new data repository in: "{self._app.insight.work_dir}".\n'
                      'Test mode: Setting uninitialized parameters and scalars to default value.\n')

            else:
                print(f'Test mode: Loading parameters from data repository in: "{self._app.insight.work_dir}".\n'
                      'Test mode: Setting uninitialized scalars to default value.\n')
                #
                self._load_meta()
                #
                self._base.load_entities(lambda entity: isinstance(entity, xi_types.Param))

            #
            self._base.initialize_entities(lambda entity: (isinstance(entity, xi_types.Param) and
                                                           entity.name not in self._app.__dict__))

            #
            self._base.initialize_entities(lambda entity: (isinstance(entity, xi_types.Scalar) and
                                                           (entity.manage == xi_types.Manage.RESULT or
                                                            entity.name not in self._app.__dict__)))

            #
            self._base.clean()

            #
            self._base.save_entities(lambda entity: isinstance(entity, xi_types.Param))

            #
            self._original_input_only_scalar_values = self._get_input_only_scalar_values()

        else:
            self._check_base_exists()

            #
            self._load_meta()
            #
            self._base.load_entities(lambda entity: isinstance(entity, xi_types.Param))
            #
            self._base.initialize_entities(lambda entity: (isinstance(entity, xi_types.Scalar) and
                                                           (entity.is_managed == xi_types.Manage.RESULT or
                                                            entity.name not in self._app.__dict__)))

    def save_input(self):
        """ Save values of input entities. """
        self._base.save_entities(lambda entity: entity.is_managed(xi_types.Manage.INPUT))

    def load_input(self):
        """ Load values of input entities. """
        if self._app.insight.test_mode:
            self._warn_about_work_dir()
            if self._base.is_empty():
                print(f'Test mode: Creating new data repository: "{self._app.insight.work_dir}".\n'
                      'Test mode: Setting uninitialized parameters and scalars to default value.\n'
                      'Test mode: Inputs have to be initialized manually before calling this execution mode.\n')
                self._base.clean()
                self._base.initialize_entities(lambda entity: (isinstance(entity, xi_types.ScalarBase) and
                                                               entity.is_managed(xi_types.Manage.INPUT) and
                                                               entity.name not in self._app.__dict__))
                self.save_input()

            else:
                print(f'Test mode: Loading parameters and input from data repository: "{self._app.insight.work_dir}".\n')
                self._load_meta()
                self._base.load_entities(lambda entity: entity.is_managed(xi_types.Manage.INPUT))

            #
            self._original_input_only_scalar_values = self._get_input_only_scalar_values()

        else:
            self._check_base_exists()
            self._load_meta()
            self._base.load_entities(lambda entity: entity.is_managed(xi_types.Manage.INPUT))

        #
        self._base.initialize_entities(lambda entity: (isinstance(entity, xi_types.Scalar) and
                                                       entity.manage == xi_types.Manage.RESULT))

    def save_result(self):
        """ Save values of result and update-after-execution entities. """
        if self._app.insight.test_mode:
            #
            #
            #
            input_scalar_values = self._get_input_only_scalar_values()

            #
            if self._original_input_only_scalar_values:
                for (name, value) in self._original_input_only_scalar_values.items():
                    self._app.__dict__[name] = value

            #
            #
            self._base.save_entities(lambda entity: (entity.is_managed(xi_types.Manage.RESULT) or
                                                     isinstance(entity, xi_types.Scalar)))

            #
            #
            for (name, value) in input_scalar_values.items():
                self._app.__dict__[name] = value

        else:
            #
            self._base.save_entities(lambda entity: entity.is_managed(xi_types.Manage.RESULT))

    def save_progress(self):
        """ Save values of progress entities. """
        self._base.save_entities(lambda entity: entity.update_progress)

    @property
    def base(self):
        """ Generic DataContainer being used by the app. """
        return self._base
