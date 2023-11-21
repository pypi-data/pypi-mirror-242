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
from dataclasses import dataclass
from typing import Dict, Optional, Union, Type, Callable, List
from contextlib import contextmanager
import datetime

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dataclasses_json import LetterCase, dataclass_json

import xpressinsight.entities as xi_types
from xpressinsight.table_connector import TableConnector, SingleValueDict

PARQUET_DIR = "parquet"

EXPORT_TYPE_MAP: Dict[Type[xi_types.BasicType], pa.DataType] = {
    xi_types.boolean: pa.bool_(),
    xi_types.integer: pa.int32(),
    xi_types.string: pa.utf8(),
    xi_types.real: pa.float64(),
}


class ParquetConnector(TableConnector):
    """TableConnector implementation that reads/writes Parquet files. Further subclasses will add behaviours specific
     to interactions with Mosel/mmarrow or with Insight Worker."""
    def __init__(self, data_container, parquet_dir: str, fetch_individual_series: bool = True):
        super().__init__(data_container, fetch_individual_series=fetch_individual_series)
        self._parquet_dir = parquet_dir

    def _get_export_type(self, src_type: Type[xi_types.BasicType]) -> pa.DataType:
        return EXPORT_TYPE_MAP[src_type]

    def _encode_column_name(self, ident: str) -> str:
        return ident

    def _decode_column_name(self, ident: str) -> str:
        return ident

    def clean(self):
        """ Creates directory structure for parquet data repository if it does not exist.
        If parquet folder contains parquet files, delete all of them. """
        #
        #
        try:
            os.makedirs(self._parquet_dir, exist_ok=True)
            files = os.listdir(self._parquet_dir)

            for file in files:
                if file.endswith(".parquet"):
                    os.remove(os.path.join(self._parquet_dir, file))
        except OSError as err:
            raise OSError(f'Could not clean data repository directory: "{self._parquet_dir}".\nOSError: {err}') from err

    def _does_db_exist(self) -> bool:
        """Returns True iff data repository directory exists"""
        return os.path.isdir(self._parquet_dir)

    def _check_db_exists(self):
        """Checks if the SQLite database files exists, if it does not, raises and exception"""

        if not self._does_db_exist():
            raise FileNotFoundError(f'Cannot find data repository directory: "{self._parquet_dir}".')

    def is_empty(self) -> bool:
        return not self._does_db_exist()

    def _save_single_values_db(self, prefix: str, values: SingleValueDict):
        """Saves SingleValueDict to the database"""

        assert prefix in ("SCALAR", "PARAM", "META")

        for dtype in xi_types.ALL_BASIC_TYPE:
            #
            if dtype in values and values[dtype]:
                #
                #
                #
                #
                table_name = f"{prefix}_{dtype.__name__}"
                schema = pa.schema([
                    pa.field('Name', pa.utf8(), False),
                    pa.field('Value', EXPORT_TYPE_MAP[dtype], False)
                ])
                #
                arrow_table = pa.Table.from_pydict({
                    'Name': values[dtype].keys(),
                    'Value': values[dtype].values()
                }, schema=schema)
                self._export_table(arrow_table, table_name, dtype={})
                del arrow_table

    def _get_pq_file_name(self, table_name):
        return table_name + '.parquet'

    def _get_pq_file_path(self, table_name):
        return os.path.join(self._parquet_dir, self._get_pq_file_name(table_name))

    def _has_table(self, table_name: str) -> bool:
        return os.path.isfile(self._get_pq_file_path(table_name))

    @staticmethod
    def _int64_conversion(table: pd.DataFrame, schema: pa.Schema):
        for field in schema:
            if pa.types.is_integer(field.type) and table[field.name].dtype != np.int64:
                table[field.name] = table[field.name].astype(np.int64, copy=False)

    def _import_table(self, table_name: str) -> pd.DataFrame:
        """Import parquet file as flat DataFrame with indices as normal columns."""
        #
        start_time = datetime.datetime.utcnow()

        #
        #
        arrow_table = pq.read_table(self._get_pq_file_path(table_name))
        #
        table = arrow_table.to_pandas(ignore_metadata=True)

        #
        #
        ParquetConnector._int64_conversion(table, arrow_table.schema)
        del arrow_table

        if self._verbose:
            end_time = datetime.datetime.utcnow()
            print(f'Imported {table_name}: {end_time - start_time}')

        return table

    @staticmethod
    def _get_schema(df: pd.DataFrame, dtype: Dict[str, pa.DataType], data_col_nullable: bool):
        #
        return pa.schema(
            #
            #
            [pa.field(f_name, f_type, f_name not in df.index.names and data_col_nullable)
             for f_name, f_type in dtype.items()]
        )

    def _export_table(self, df: Union[pa.Table, pd.DataFrame, pd.Series], table_name: str,
                      dtype: Dict[str, pa.DataType], index: bool = True, data_col_nullable: bool = False):
        start_time = datetime.datetime.utcnow()

        #
        if isinstance(df, pd.Series):
            #
            df = df.to_frame()

        if isinstance(df, pd.DataFrame):
            #
            schema = self._get_schema(df, dtype, data_col_nullable)
            #
            arrow_table = pa.Table.from_pandas(df, schema=schema, preserve_index=index)
        elif isinstance(df, pa.Table):
            #
            arrow_table = df
        else:
            raise TypeError(f'Unexpected table type. Cannot export: {type(df)}.')

        #
        #
        pq.write_table(arrow_table, where=self._get_pq_file_path(table_name), compression='NONE')
        del arrow_table

        if self._verbose:
            end_time = datetime.datetime.utcnow()
            print(f'Exported {table_name}: {end_time - start_time}')

    @contextmanager
    def _connect(self):
        """ Check if parquet directory exists. """
        self._check_db_exists()
        try:
            yield self._parquet_dir
        finally:
            pass


class MoselParquetConnector(ParquetConnector):
    """ Variant of the ParquetConnector that reads/writes Parquet files written by Mosel. """

    def __init__(self, app, parquet_dir: Optional[str] = None):
        super().__init__(app,
                         parquet_dir=os.path.join(app.insight.work_dir, PARQUET_DIR)
                                     if parquet_dir is None else parquet_dir,
                         fetch_individual_series=True)


#
INSIGHT_WORKER_VALUE_TYPES_FOR_BASIC_TYPES: Dict[Optional[Type[xi_types.BasicType]], Optional[str]] = {
    xi_types.integer: 'INTEGER',
    xi_types.real: 'REAL',
    xi_types.string: 'STRING',
    xi_types.boolean: 'BOOLEAN',
    None: None
}


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ArraysTableColumn:
    """ Python implementation of Insight DTO class
        com.fico.xpress.insight.shared.parquet.converter.ArraysTableDescription.Array """
    entity_name: str
    column_name: Optional[str]
    value_type: Optional[str]
    empty_value: Optional[Union[int, float, str, bool]]
    use_default_empty_value: Optional[bool]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ArraysTableIndex:
    """ Python implementation of Insight DTO class
        com.fico.xpress.insight.shared.parquet.converter.ArraysTableDescription.Index """
    column_name: Optional[str]
    value_type: Optional[str]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ArraysTableDescription:
    """ Python implementation of Insight DTO class
        com.fico.xpress.insight.shared.parquet.converter.ArraysTableDescription """
    arrays: List[ArraysTableColumn]
    indexes: Optional[List[ArraysTableIndex]]
    type: str = "ARRAYS"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ScalarsTableEntry:
    """ Python implementation of Insight DTO class
        com.fico.xpress.insight.shared.parquet.converter.ScalarsTableDescription.Scalar """
    entity_name: str
    value_type: Optional[str]
    skip_on_type_mismatch: bool = False


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ScalarsTableDescription:
    """ Python implementation of Insight DTO class
        com.fico.xpress.insight.shared.parquet.converter.ScalarsTableDescription """
    scalars: List[ScalarsTableEntry]
    type: str = "SCALARS"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SetTableDescription:
    """ Python implementation of Insight DTO class
        com.fico.xpress.insight.shared.parquet.converter.SetTableDescription """
    entity_name: str
    column_name: Optional[str]
    value_type: Optional[str]
    type: str = "SET"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ConversionDescription:
    """ Python implementation of Insight DTO class
        com.fico.xpress.insight.shared.parquet.converter.ConversionDescription """
    tables: Dict[str, Union[ScalarsTableDescription, SetTableDescription, ArraysTableDescription]]


class InsightWorkerParquetConnector(ParquetConnector):
    """ Variant of the ParquetConnector that reads scenario data for the given scenario directly from the
        Insight worker. """
    def __init__(self, app, data_container, scenario_path_or_id: str, parquet_dir: str, fetch_individual_series: bool):
        super().__init__(data_container, parquet_dir=parquet_dir, fetch_individual_series=fetch_individual_series)
        self._app = app
        self._scenario_path_or_id = scenario_path_or_id

    def _encode_df_column_name(self, name: str, column: str) -> str:
        #
        return self._encode_column_name(column)

    def _make_conversion_description(self, entity_filter: Callable[[xi_types.Entity], bool]) -> ConversionDescription:
        """ Creates a conversion description to describe to the Insight worker which entities need to be written into
            which Parquet files """
        #
        scalar_entries_by_type: Dict[Type[xi_types.BASIC_TYPE], List[ScalarsTableEntry]] = {
            dtype: [] for dtype in xi_types.ALL_BASIC_TYPE
        }
        #
        tables: Dict[str, Union[ScalarsTableDescription, SetTableDescription, ArraysTableDescription]] = {}

        for entity in ParquetConnector._get_entities(self._data_container, entity_filter):
            if isinstance(entity, xi_types.Param):
                raise RuntimeError("Fetching parameter entities is not supported, use 'parameters' array instead")

            elif isinstance(entity, xi_types.Scalar):
                if entity.dtype:
                    scalar_entries_by_type[entity.dtype].append(ScalarsTableEntry(
                        entity_name=entity.entity_name,
                        value_type=INSIGHT_WORKER_VALUE_TYPES_FOR_BASIC_TYPES[entity.dtype]
                    ))

                else:
                    #
                    for dtype in xi_types.ALL_BASIC_TYPE:
                        scalar_entries_by_type[dtype].append(ScalarsTableEntry(
                            entity_name=entity.entity_name,
                            value_type=INSIGHT_WORKER_VALUE_TYPES_FOR_BASIC_TYPES[dtype],
                            skip_on_type_mismatch=True
                        ))

            elif isinstance(entity, xi_types.Index):
                tables[self._encode_table_name(entity.name)] = SetTableDescription(
                    entity_name=entity.entity_name,
                    column_name=entity.name,
                    value_type=INSIGHT_WORKER_VALUE_TYPES_FOR_BASIC_TYPES[entity.dtype])

            elif isinstance(entity, (xi_types.Series, xi_types.DataFrame)):
                #
                index_column_names = entity.index_names
                index_types = entity.index_types
                has_some_index_info = bool(index_column_names) or bool(index_types)
                if has_some_index_info:
                    num_indexes = len(index_column_names) if index_column_names else len(index_types)

                    if not index_column_names:
                        index_column_names = [None for _ in range(0, num_indexes)]
                    elif len(index_column_names) != num_indexes:
                        raise RuntimeError("Same numbers of index names and types must be given")

                    if not index_types:
                        index_types = [None for _ in range(0, num_indexes)]
                    elif len(index_types) != num_indexes:
                        raise RuntimeError("Same numbers of index names and types must be given")

                indexes = [
                    ArraysTableIndex(
                        column_name=name,
                        value_type=INSIGHT_WORKER_VALUE_TYPES_FOR_BASIC_TYPES[dtype]
                    ) for (name, dtype) in zip(index_column_names, index_types)
                ] if has_some_index_info else None

                if isinstance(entity, xi_types.Series):
                    tables[self._encode_table_name(entity.name)] = ArraysTableDescription(
                        arrays=[ArraysTableColumn(
                            entity_name=entity.entity_name,
                            column_name=entity.series_name,
                            value_type=INSIGHT_WORKER_VALUE_TYPES_FOR_BASIC_TYPES[entity.dtype],
                            #
                            empty_value=None,
                            use_default_empty_value=False)],
                        indexes=indexes
                    )

                else:
                    assert isinstance(entity, xi_types.DataFrame)
                    if self._fetch_individual_series:
                        for col in entity.columns:
                            if entity_filter(col):
                                tables[self._encode_df_table_name(entity.name, col.name)] = ArraysTableDescription(
                                    arrays=[ArraysTableColumn(
                                        entity_name=col.entity_name,
                                        column_name=self._encode_df_column_name(entity.name, col.name),
                                        value_type=INSIGHT_WORKER_VALUE_TYPES_FOR_BASIC_TYPES[col.dtype],
                                        #
                                        empty_value=None,
                                        use_default_empty_value=False)],
                                    indexes=indexes
                                )

                    else:
                        tables[self._encode_table_name(entity.name)] = ArraysTableDescription(
                            arrays=[
                                ArraysTableColumn(
                                    entity_name=col.entity_name,
                                    column_name=col.name,
                                    value_type=INSIGHT_WORKER_VALUE_TYPES_FOR_BASIC_TYPES[col.dtype],
                                    #
                                    #
                                    empty_value=col.default,
                                    use_default_empty_value=col.default is None
                                ) for col in entity.columns if entity_filter(col)],
                            indexes=indexes
                        )

            else:
                raise RuntimeError(f"Unrecognized type: {type(entity)}")

        #
        for (dtype, scalar_entries) in scalar_entries_by_type.items():
            if scalar_entries:
                tables[f"SCALAR_{dtype.__name__}"] = ScalarsTableDescription(scalars=scalar_entries)

        return ConversionDescription(tables={
            self._get_pq_file_name(table_name): table
            for (table_name, table) in tables.items()
        })

    def load_entities(self, entity_filter: Callable[[xi_types.Entity], bool]):
        #
        conversion_description = self._make_conversion_description(entity_filter)

        #
        conversion_description_file = os.path.join(self._parquet_dir, 'tables.json')
        #
        #
        #
        conversion_description_json = conversion_description.to_json()
        with open(conversion_description_file, 'w', encoding="utf-8") as f:
            f.write(conversion_description_json)

        #
        self._app.insight._fetch_scenario_data_parquet(scenario_path_or_id=self._scenario_path_or_id,
                                                       output_dir=self._parquet_dir,
                                                       conversion_description_file=conversion_description_file)

        #
        try:
            super().load_entities(entity_filter)
        except Exception as e:
            #
            print(f"ERROR: The {self.__class__.__name__} failed to restore entity data fetched from the Insight"
                  f"worker for reason '{e}'; the following description of the data fetched may be useful to Xpress"
                  f"Insight support in diagnosing this issue: {conversion_description_json}")
            raise e

    def save_entities(self, entity_filter: Callable[[xi_types.Entity], bool]):
        raise RuntimeError("Saving entities directly to the Insight worker is not supported at this time.")
