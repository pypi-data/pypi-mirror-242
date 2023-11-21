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

#
from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum

import sys
import re
from typing import (Type, Dict, Union, Tuple, List, Iterable, Any, Optional, Set, TypeVar, Generic, Mapping,
                    get_args, get_origin)
import pandas as pd
import numpy as np

from xpressinsight.mosel_keywords import MOSEL_KEYWORDS

if sys.version_info < (3, 9):
    from typing_extensions import get_type_hints
else:
    from typing import get_type_hints

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

MAX_STR_LENGTH_BYTES = 1000000
MAX_STR_LENGTH_CHARS = int(MAX_STR_LENGTH_BYTES / 4)

VALID_IDENT_REGEX_STR = "[_a-zA-Z][_a-zA-Z0-9]*"
VALID_IDENT_REGEX = re.compile(VALID_IDENT_REGEX_STR)
VALID_IDENT_MAX_LENGTH = 1000

VALID_ANNOTATION_STR_REGEX_STR = "[\n\r\0]"
VALID_ANNOTATION_STR_REGEX = re.compile(VALID_ANNOTATION_STR_REGEX_STR)
VALID_ANNOTATION_STR_MAX_LENGTH = 5000

ENTITY_CLASS_NAMES = {'Param', 'Scalar', 'Index', 'Series', 'DataFrame', 'Column'}


def is_valid_identifier(ident: str, max_length: int = VALID_IDENT_MAX_LENGTH) -> bool:
    """ Checks if a string is a valid identifier for an Xpress Insight entity. """

    if len(ident) > max_length:
        raise ValueError("The identifier {} must not be longer than {} characters."
                         .format(repr(ident), max_length))

    return VALID_IDENT_REGEX.fullmatch(ident) is not None


def validate_ident(ident: str, ident_for: str = None, ident_name: str = "identifier") -> str:
    if not is_valid_identifier(ident):
        if ident_for is None:
            err_msg = "Invalid {0} {1}. Identifier must satisfy regex {3}."
        else:
            err_msg = "Invalid {0} {1} for {2}. Identifier must satisfy regex {3}."
        raise ValueError(err_msg.format(ident_name, repr(ident), ident_for, repr(VALID_IDENT_REGEX_STR)))

    if ident in MOSEL_KEYWORDS:
        if ident_for is None:
            err_msg = "Invalid {0} {1}. Identifier must not be a reserved keyword."
        else:
            err_msg = "Invalid {0} {1} for {2}. Identifier must not be a reserved keyword."
        raise ValueError(err_msg.format(ident_name, repr(ident), ident_for))

    return ident


def validate_raw_ident(ident: str, ident_name: str = "identifier") -> str:
    """ Check whether a string is a valid identifier in an annotation. """
    if not is_valid_identifier(ident):
        raise ValueError('{} is not a valid {}. Identifier must satisfy regex {}.'
                         .format(repr(ident), ident_name, repr(VALID_IDENT_REGEX_STR)))
    return ident


def validate_annotation_str(s: str,
                            str_name: str = 'annotation string',
                            max_length: int = VALID_ANNOTATION_STR_MAX_LENGTH) -> str:
    """ Check whether annotation string contains unsupported characters or is too long. """
    if "!)" in s:
        raise ValueError('The {} must not contain the substring "!)": {}.'.format(str_name, repr(s)))
    if len(s) > max_length:
        raise ValueError("The {} must not be longer than {} characters: {}.".format(str_name, max_length, repr(s)))
    if VALID_ANNOTATION_STR_REGEX.search(s) is not None:
        raise ValueError("The {} {} contains unsupported characters. It must not match the regular expression {}"
                         .format(str_name, repr(s), repr(VALID_ANNOTATION_STR_REGEX_STR)))
    return s


def is_value_of_type(val: Any, expected_type: Type) -> bool:
    """ Check whether the given value is of the expected type.
        Supports expected_type being a Union or an Optional or a BASIC_TYPE as well as other types that
        can be evaluated using isinstance."""

    if get_origin(expected_type) is Union:
        for possible_type in get_args(expected_type):
            if is_value_of_type(val, possible_type):
                return True

        return False

    if expected_type == BASIC_TYPE:
        return isinstance(val, type) and issubclass(val, (boolean, integer, string, real))

    return isinstance(val, expected_type)


def check_simple_python_type(attr: Any, attr_name: str, attr_type: Type, parent: Type = None):
    if not is_value_of_type(attr, attr_type):
        attr_name = re.sub(r'_.*__', '', attr_name)
        parent = f"of {parent.__name__} " if parent is not None else ""
        raise TypeError(f'The "{attr_name}" parameter {parent}must be a "{attr_type.__name__}" object, '
                        f'but it is a "{type(attr).__name__}" and has value "{attr}".')


def check_instance_attribute_types(class_instance: Any):
    """ Type check for all instance attributes with class level type hints. """
    class_type = type(class_instance)
    none_type = type(None)

    for attr_name, attr_type in get_type_hints(class_type).items():
        attr = getattr(class_instance, attr_name)

        #
        #
        if get_origin(attr_type) is Union:
            non_none_types = [arg for arg in get_args(attr_type) if arg is not none_type]

            if len(non_none_types) == 1:
                if attr is None:
                    continue

                attr_type = non_none_types[0]

        if attr_type == BASIC_TYPE:
            if not issubclass(attr, (boolean, integer, string, real)):
                type_err_msg = 'The "{}" parameter of {} must be the {}, but it is a "{}" and has value "{}".'
                attr_name = re.sub(r'_.*__', '', attr_name)
                raise TypeError(type_err_msg.format(attr_name, class_type.__name__,
                                                    'Insight type string, integer, boolean, or real',
                                                    type(attr).__name__, attr))
        else:
            check_simple_python_type(attr, attr_name, attr_type, class_type)


class XiEnum(Enum):
    """
    The base class for `Enum` types in the `xpressinsight` package.
    """

    def __repr__(self):
        #
        #
        return f"{self.__class__.__name__}.{self._name_}"


class Manage(XiEnum):
    """
    How and whether Insight handles an entity.

    Attributes
    ----------
    INPUT : str
        Included in the scenario input data.
    RESULT : str
        Included in the scenario results data.

    Examples
    --------
    Manage a scalar entity as an input

    >>> MyInteger: xi.types.Scalar(dtype=xi.integer,
    ...                            alias='My Integer',
    ...                            manage=xi.Manage.INPUT)
    """

    INPUT = "input"
    RESULT = "result"


class Hidden(XiEnum):
    """
    Possible values of whether the UI should hide an entity where appropriate.

    Attributes
    ----------
    ALWAYS : str
        Indicates that the UI should hide the entity always.
    TRUE : str
        Indicates that the UI should hide the entity where appropriate.
    FALSE : str
        Indicates that the UI should show the entity where appropriate.

    Examples
    --------
    Always hide an entity in the Insight UI

    >>> MyInteger: xi.types.Scalar(dtype=xi.integer,
    ...                            alias='My Integer',
    ...                            hidden=xi.Hidden.ALWAYS)
    """

    ALWAYS = "always"
    TRUE = "true"
    FALSE = "false"


BASIC_TYPE_VALUE = TypeVar('BASIC_TYPE_VALUE', bool, int, str, float)


class BasicType(Generic[BASIC_TYPE_VALUE]):
    pass


#
class boolean(BasicType[bool]):
    """
    Declare the entity to be (or to contain) boolean (`True` or `False`) values.
    If not specified, the default value is `False`.

    Examples
    --------
    Example of declaring a scalar entity to be boolean.

    >>> my_bool: xi.types.Scalar(dtype=xi.boolean)
    ... my_bool: xi.types.Scalar(False)
    ... my_bool: xi.types.Scalar(True)

    See Also
    --------
    Scalar
    Param
    Index
    Series
    Column
    """

    pass


#
class integer(BasicType[int]):
    """
    Declare the entity to be (or to contain) integer (whole number) values.
    Each value must fit into a signed 32-bit integer.
    If not specified, the default value is `0`.

    Examples
    --------
    Example of declaring a scalar entity to be integer.

    >>> my_int: xi.types.Scalar(dtype=xi.integer)
    ... my_int: xi.types.Scalar(0)
    ... my_int: xi.types.Scalar(100)
    ... my_int: xi.types.Scalar(-10)

    See Also
    --------
    Scalar
    Param
    Index
    Series
    Column
    """

    pass


#
#
class string(BasicType[str]):
    """
    Declare the entity to be (or to contain) string (UTF-8 encoded) values. The length
    (in bytes) of a string scalar (Scalar or Param) must not exceed 1,000,000 bytes.
    The length of a string in a container (Index, Series, or DataFrame) must not exceed
    250,000 characters. A string must not contain the null character.
    If not specified, the default value of a string scalar is the empty string `""`.

    Examples
    --------
    Example of declaring a scalar entity to be a string.

    >>> my_string: xi.types.Scalar(dtype=xi.string)
    ... my_string: xi.types.Scalar("Hello World!")

    See Also
    --------
    Scalar
    Param
    Index
    Series
    Column
    """

    pass


#
class real(BasicType[float]):
    """
    Declare the entity to be (or to contain) floating-point (whole number) values.
    If not specified, the default value is `0.0`.

    Examples
    --------
    Example of declaring a scalar entity to be a floating-point value.

    >>> my_real: xi.types.Scalar(dtype=xi.real)
    >>> my_real: xi.types.Scalar(100.0)
    >>> my_real: xi.types.Scalar(123.456)

    See Also
    --------
    Scalar
    Param
    Index
    Series
    Column
    """

    pass


ALL_BASIC_TYPE = [boolean, integer, string, real]

BASIC_TYPE = Type[BasicType]

#
BASIC_TYPE_MAP: Dict[Type[BasicType], Type] = {
    boolean: bool,
    integer: int,
    string: str,
    real: float,
    #
    None: Union[bool, int, str, float]
}

#
BASIC_PANDAS_DTYPE_MAP: Dict[Type[BasicType], Type] = {
    boolean: np.bool_,
    integer: np.int64,
    string: str,
    real: np.float64,
}

#
SCALAR_DEFAULT_VALUES: Dict[Type[BasicType], Union[bool, int, str, float]] = {
    boolean: False,
    integer: 0,
    string: "",
    real: 0.0,
}


def get_basic_type_for_python_type(src_type: Type) -> Type[BasicType]:
    """ Given some value type, get the appropriate basic type value. """
    pd_dtype = pd.api.types.pandas_dtype(src_type)

    if pd.api.types.is_bool_dtype(pd_dtype):
        return boolean

    if pd.api.types.is_integer_dtype(pd_dtype):
        return integer

    if pd.api.types.is_float_dtype(pd_dtype):
        return real

    if pd.api.types.is_string_dtype(pd_dtype):
        return string

    raise TypeError(f"Unable to determine XpressInsight data type for source type {src_type}.")


def python_int_to_bool(value: int, name: str = None) -> bool:
    if value == int(True):
        return True
    elif value == int(False):
        return False
    else:
        if name is None:
            msg = "Invalid boolean, expecting {} (True) or {} (False) but got {}.".format(
                int(True), int(False), value
            )
        else:
            msg = "{} invalid boolean, expecting {} (True) or {} (False) but got {}.".format(
                name, int(True), int(False), value
            )
        raise ValueError(msg)


class EntityBase(ABC):
    """
    Abstract base class of all Insight entities, including composed entities like *DataFrames*.

    See Also
    --------
    AppConfig.entities
    """
    __name: str

    def __init__(self):
        self.__name = ''

    def _init_app_entity(self, entities: Mapping[str, Self]):
        """ Initialize this entity, creating links to other entities as given. """
        pass

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if self.__name == '':
            self.__name = validate_ident(name, type(self).__name__, 'name')
        else:
            raise AttributeError('Cannot set name of {} to "{}" because it has already been initialized to "{}".'
                                 .format(type(self).__name__, name, self.__name))

    @property
    @abstractmethod
    def update_progress(self) -> bool:
        pass

    @abstractmethod
    def is_managed(self, manage: Manage) -> bool:
        pass

    @property
    @abstractmethod
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        pass

    def _check_valid_app_entity(self):
        """ Verifies that this entity is valid for use in an app. """
        pass

    def _check_valid_scenario_data_entity(self):
        """ Verifies that this entity is valid for use in a ScenarioData container. """
        pass


class Entity(EntityBase, ABC):
    """
    Abstract base class of all native Insight entities, excluding composed entities like *DataFrames*. This class
    is used both for entities of the current app in classes decorated with `xi.AppConfig` and entities defined for
    scenario data in classes decorated with `ScenarioData`.
    """

    __dtype: Optional[BASIC_TYPE]
    __alias: str
    __format: str
    __hidden: Hidden
    __manage: Manage
    __read_only: bool
    __transform_labels_entity: str
    __update_after_execution: bool
    __update_progress: bool
    __entity_name: Optional[str]

    #
    def __init__(self,
                 dtype: BASIC_TYPE = None,
                 #
                 alias: str = "",
                 format: str = "",
                 hidden: Hidden = Hidden.FALSE,
                 manage: Manage = Manage.INPUT,
                 read_only: bool = False,
                 transform_labels_entity: str = "",
                 update_after_execution: bool = False,
                 *,
                 update_progress: bool = False,
                 entity_name: str = None
                 #
                 ):
        """
        The constructor.

        Parameters
        ----------
        dtype : BASIC_TYPE
            The data type.
        alias : str = ""
            Used to provide an alternative name for an entity in the UI.
            The value is used in place of the entity name where appropriate in the UI.
        format : str = ""
            The formatting string used for displaying numeric values.
        hidden : Hidden = Hidden.FALSE
            Indicates whether the UI should hide the entity where appropriate.
        manage : Manage = Manage.INPUT
            How and whether Insight handles an entity. Defines how the system manages the entity data.
        read_only : bool = False
            Whether an entity is readonly. Specifies that the value(s) of the entity cannot be modified. See also
            `hidden`.
        transform_labels_entity : str = ""
            The name of an entity in the schema from which to read labels for values of this entity.
            The type of the index set of the labels entity must match the data type of this entity.
            The data type of the labels entity can be any primitive type.
        update_after_execution : bool = False
            Whether the value of the entity in the scenario is updated with the value of
            the corresponding model entity at the end of the scenario execution.
            If `True` the value of the entity is updated to correspond with the model entity after execution.
        update_progress : bool = False
            Whether the value of the entity in the scenario is sent on progress updates.
            If `True` the value of the entity will be written back to the Insight repository when
            :fct-ref:`insight.send_progress_update` is called from an execution mode where the `send_progress`
            attribute is `True`.
        entity_name : str = None
            The entity name. If not given, the name of the class attribute will be used instead.
            Only valid for entities in an `xi.ScenarioData`-decorated class.

        Notes
        -----
        Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
        but it's recommended that you always use named arguments if you're specifying parameters other than
        `dtype` and `alias`.
        """
        super().__init__()
        self.__dtype = dtype
        #
        self.__alias = alias
        self.__format = format
        self.__hidden = hidden
        self.__manage = manage
        self.__read_only = read_only
        self.__transform_labels_entity = transform_labels_entity.replace('.', '_')
        self.__update_after_execution = update_after_execution
        self.__update_progress = update_progress
        self.__entity_name = entity_name
        #
        check_instance_attribute_types(self)
        validate_annotation_str(alias, 'entity alias')
        validate_annotation_str(format, 'entity format')

        if transform_labels_entity != "":
            validate_ident(self.__transform_labels_entity, "transform labels entity")

        if update_after_execution and manage == Manage.RESULT:
            raise ValueError('Cannot set parameter update_after_execution to True for a result entity. '
                             'This parameter is only valid for input entities.')

        if update_progress and manage == Manage.INPUT and not update_after_execution:
            raise ValueError('Cannot set parameter update_progress to True for an input entity if '
                             'update_after_execution is not also True.')

    @property
    def dtype(self) -> Optional[BASIC_TYPE]:
        return self.__dtype

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def format(self) -> str:
        return self.__format

    @property
    def hidden(self) -> Hidden:
        return self.__hidden

    @property
    def manage(self) -> Manage:
        return self.__manage

    @property
    def read_only(self) -> bool:
        return self.__read_only

    @property
    def transform_labels_entity(self) -> str:
        return self.__transform_labels_entity

    @property
    def update_after_execution(self) -> bool:
        return self.__update_after_execution

    @property
    def update_progress(self) -> bool:
        return self.__update_progress

    def is_managed(self, manage: Manage) -> bool:
        """ Check whether the entity is managed as the given management type: input/result. """
        return self.__manage == manage or (self.__update_after_execution and manage == Manage.RESULT)

    @property
    def entity_name(self) -> str:
        return self.__entity_name if self.__entity_name else self._default_entity_name

    @property
    def _default_entity_name(self) -> str:
        """ Entity name to use if none is specified in `entity_name` attribute. """
        return self.name

    def _check_valid_app_entity(self):
        super()._check_valid_app_entity()

        #
        if self.dtype is None:
            raise TypeError(f'No "dtype" was configured for entity {self.name}.')

        #
        if self.entity_name != self._default_entity_name:
            raise TypeError("An app entity cannot have an entity name different from the attribute name.")


class ScalarBase(Entity):
    #
    def __init__(
            self,
            default: BASIC_TYPE_VALUE = None,
            dtype: Type[BasicType[BASIC_TYPE_VALUE]] = None,
            #
            alias: str = "",
            format: str = "",
            hidden: Hidden = Hidden.FALSE,
            manage: Manage = Manage.INPUT,
            read_only: bool = False,
            transform_labels_entity: str = "",
            update_after_execution: bool = False,
            *,
            update_progress: bool = False,
            entity_name: str = None
            #
    ):
        """
        The constructor.

        Parameters
        ----------
        default : BASIC_TYPE_VALUE = None
            The default value; if specified, must be a value of the appropriate type for the `dtype` of this entity
            (e.g. a `str` if `dtype` is `xi.string`).
        dtype : Type[BasicType[BASIC_TYPE_VALUE]]
            The data type; one of `xi.boolean`, `xi.real`, `xi.integer` or `xi.string`.
        alias : str = ""
            Used to provide an alternative name for an entity in the UI.
            The value is used in place of the entity name where appropriate in the UI.
        format : str = ""
            The formatting string used for displaying numeric values.
        hidden : Hidden = Hidden.FALSE
            Indicates whether the UI should hide the entity where appropriate.
        manage : Manage = Manage.INPUT
            How and whether Insight handles an entity. Defines how the system manages the entity data.
        read_only : bool = False
            Whether an entity is readonly. Specifies that the value(s) of the entity cannot be modified. See also
            `hidden`.
        transform_labels_entity : str = ""
            The name of an entity in the schema from which to read labels for values of this entity.
            The type of the index set of the labels entity must match the data type of this entity.
            The data type of the labels entity can be any primitive type.
        update_after_execution : bool = False
            Whether the value of the entity in the scenario is updated with the value of
            the corresponding model entity at the end of the scenario execution.
            If `True` the value of the entity is updated to correspond with the model entity after execution.
        update_progress : bool = False
            Whether the value of the entity in the scenario is sent on progress updates.
            If `True` the value of the entity will be written back to the Insight repository when
            :fct-ref:`insight.send_progress_update` is called from an execution mode where the `send_progress`
            attribute is `True`.
        entity_name : str = None
            The entity name. If not given, the name of the class attribute will be used instead.
            Only valid for entities in an `xi.ScenarioData`-decorated class.

        Notes
        -----
        Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
        but it's recommended that you always use named arguments if you're specifying parameters other than `default`,
        `dtype` and `alias`.
        """
        #
        if dtype is None and default is not None:
            #
            if isinstance(default, str):
                dtype = string
            elif isinstance(default, bool):
                dtype = boolean
            elif isinstance(default, int):
                dtype = integer
            elif isinstance(default, float):
                dtype = real
            else:
                raise TypeError('The default value of a scalar or parameter must be a str, int, bool, '
                                'or float, but it is a "{}".'.format(type(default)))

        #
        super().__init__(
            dtype=dtype,
            #
            alias=alias,
            format=format,
            hidden=hidden,
            manage=manage,
            read_only=read_only,
            transform_labels_entity=transform_labels_entity,
            update_after_execution=update_after_execution,
            update_progress=update_progress,
            entity_name=entity_name
            #
        )

        if default is None and self.dtype is not None:
            self.__default = SCALAR_DEFAULT_VALUES[dtype]
            assert self.__default is not None
        elif default is not None:
            self.check_type(default)
            self.__default = default
        else:
            self.__default = None

    def _check_valid_app_entity(self):
        if self.default is None and self.dtype is None:
            raise TypeError('It is necessary to specify at least one of the following parameters: '
                            'dtype (data type), default (default value).')

        super()._check_valid_app_entity()

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        return BASIC_TYPE_MAP.get(self.dtype)

    def check_type(self, value: Any):
        """ Check if the type is correct and check the bounds. """
        check_basic_type_value(self.dtype, value, self.name)

    @property
    def default(self) -> Union[str, int, bool, float]:
        return self.__default


class Scalar(ScalarBase):
    """
    The configuration of a *scalar* entity. Rather than instantiating `xpressinsight.Scalar` directly, you should
    use the helper function `xpressinsight.types.Scalar` or `xpressinsight.data.Scalar` to declare a scalar entity in
    an app or scenario data container, as appropriate.

    Notes
    -----
    In older versions of `xpressinsight`, it was possible to use the `xi.Scalar` as the annotation for an entity.
    This syntax is now deprecated and should not be used in new apps; it will not be supported in Python 3.12 and
    above.

    See Also
    --------
    types.Scalar
    data.Scalar
    Param
    """

    pass


class Param(ScalarBase):
    """
    The configuration of a *parameter* entity. Parameters can be used to configure an Xpress Insight app. When
    parameters are declared, their name, data type, and default value must be specified. Parameters are typically
    read-only. Use the helper function `xpressinsight.types.Param` to declare a parameter entity in an app, rather than
    instantiating `xpressinsight.Param` directly.

    Notes
    -----
    In older versions of `xpressinsight`, it was possible to use the `xi.Param` as the annotation for an entity.
    This syntax is now deprecated and should not be used in new apps; it will not be supported in Python 3.12 and
    above.

    See Also
    --------
    types.Param
    Scalar
    """

    def __init__(
            self,
            default: BASIC_TYPE_VALUE = None,
            dtype: Type[BasicType[BASIC_TYPE_VALUE]] = None,
    ):
        """
        Initializes `Param` with the data type or a default value (in which case data type is inferred).

        Parameters
        ----------
        default: BASIC_TYPE_VALUE
            The default value; if specified, must be of the appropriate value for the `dtype` of this entity (e.g.
            a `str` if `dtype` is `xi.string`).
        dtype: Type[BasicType[BASIC_TYPE_VALUE]]
            The data type; one of `xi.boolean`, `xi.real`, `xi.integer` or `xi.string`.
        """

        super().__init__(
            default,
            dtype=dtype,
        )

    def _check_valid_scenario_data_entity(self):
        raise TypeError("Parameter entities are not supported in ScenarioData classes at this time.")


class Index(Entity):
    """
    The configuration of an *index* entity. Use the helper function `xpressinsight.types.Index` to declare an index
    entity in an app, rather than instantiating `xpressinsight.Index` directly.

    Notes
    -----
    In older versions of `xpressinsight`, it was possible to use the `xi.Index` as the annotation for an entity.
    This syntax is now deprecated and should not be used in new apps; it will not be supported in Python 3.12 and
    above.

    See Also
    --------
    types.Index
    Series
    DataFrame
    """

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        return pd.Index

    def check_type(self, value: Any, name: str):
        check_index_type_value(value, self.dtype, name)


def __get_parent_name(parent_obj_or_none: Any) -> str:
    return '' if parent_obj_or_none is None else ' of ' + type(parent_obj_or_none).__name__


T = TypeVar("T")


def validate_list(parent_obj_or_none: Any, attr_name: str, item_type: Type[T], item_type_name: str,
                  value: Union[T, List[T], Tuple[T]]) -> Tuple[T]:
    """
    Given a list/tuple, verify all the values are of the expected type and convert to an immutable tuple.
    If the given value is a single item, return that item.validate_list

    Parameters
    ----------
    parent_obj_or_none : Any
        Parent object, used in error messages only.
    attr_name : str
        Name of attribute being validated, used in error messages only.
    item_type: Type[T]
        Type of items expected in list.
    item_type_name:
        Name of expected item type
    value:
        Collection of items to evaluate
    """

    if is_value_of_type(value, item_type):
        return (value,)

    error_msg = 'The "{0}" parameter{1} must be a {2} object or a list of {2} objects, '

    if isinstance(value, list):
        value = tuple(value)

    if isinstance(value, tuple):
        if len(value) == 0:
            raise TypeError((error_msg + 'but the {0} list is empty.')
                            .format(attr_name, __get_parent_name(parent_obj_or_none), item_type_name))

        for item in value:
            if not is_value_of_type(item, item_type):
                raise TypeError((error_msg + 'but the {0} list contains an object of type "{3}" and value: {4}.')
                                .format(attr_name, __get_parent_name(parent_obj_or_none), item_type_name,
                                        type(item).__name__, repr(item)))
    else:
        raise TypeError((error_msg + 'but the {0} parameter has type "{3}" and value: {4}.')
                        .format(attr_name, __get_parent_name(parent_obj_or_none), item_type_name,
                                type(value).__name__, repr(value)))
    return value


def validate_index_names(parent_obj: EntityBase, attr_name: str, index: Any) -> Tuple[str]:
    """ Validate and normalize list of names of Indexes -> convert it to immutable tuple """
    return validate_list(parent_obj, attr_name, str, 'string', index)


def get_index_tuple(parent_obj: EntityBase, index_names: Tuple[str], entities: Mapping[str, EntityBase]) ->\
        Tuple[Index]:
    result: List[Index] = []

    for index_name in index_names:
        index = entities.get(index_name, None)

        if isinstance(index, Index):
            result.append(index)
        else:
            if index is None:
                raise KeyError(f'Invalid index "{index_name}" for xpressinsight.{type(parent_obj).__name__} '
                               f'"{parent_obj.name}". Entity "{index_name}" not declared.')
            else:
                raise KeyError(f'Invalid index "{index_name}" for xpressinsight.{type(parent_obj).__name__} '
                               f'"{parent_obj.name}". Entity "{index_name}" is a {type(index)}, but must be an '
                               f'xpressinsight.Index.')

    return tuple(result)


def get_index_level_names(index_entity_names: Iterable[str]) -> List[str]:
    """
    Generate a unique name for each index level. The level name for an index will be the name of the index entity
    unless the same index entity is used in multiple levels, in which case duplicate names will be decorated with the
    level number (e.g. ".2", ".3").
    """
    levels_with_names: List[str] = []
    names_used_so_far: Set[str] = set()

    for name in index_entity_names:
        if name in names_used_so_far:
            name_with_level = f"{name}.{len(levels_with_names) + 1}"
        else:
            name_with_level = name

        levels_with_names.append(name_with_level)
        names_used_so_far.add(name_with_level)

    return levels_with_names


class Series(Entity):
    """
    The configuration of a *Series* entity, a declaration of a pandas `Series` data structure. Use the helper function
    `xpressinsight.types.Series` to declare a Series entity in an app, rather than instantiating
    `xpressinsight.Series` directly.

    Notes
    -----
    In older versions of `xpressinsight`, it was possible to use the `xi.Series` as the annotation for an entity.
    This syntax is now deprecated and should not be used in new apps; it will not be supported in Python 3.12 and
    above.

    See Also
    --------
    types.Series
    """

    __series_name: Optional[str]

    #
    def __init__(
            self,
            index: Union[str, List[str]] = None,
            dtype: BASIC_TYPE = None,
            #
            alias: str = "",
            format: str = "",
            hidden: Hidden = Hidden.FALSE,
            manage: Manage = Manage.INPUT,
            read_only: bool = False,
            transform_labels_entity: str = "",
            update_after_execution: bool = False,
            *,
            update_progress: bool = False,
            entity_name: str = None,
            series_name: str = None,
            index_types: List[BASIC_TYPE] = None
            #
    ):
        """
        Initializes `Series`.

        Parameters
        ----------
        index : Union[str, List[str]]
            The name of the index to use, or list of names for multiple indices. Where entity is used in an app
            definition, the same index may appear in the list multiple times.
        dtype : BASIC_TYPE
            The data type.
        alias : str = ""
            Used to provide an alternative name for an entity in the UI.
            The value is used in place of the entity name where appropriate in the UI.
        format : str = ""
            The formatting string used for displaying numeric values.
        hidden : Hidden = Hidden.FALSE
            Indicates whether the UI should hide the entity where appropriate.
        manage : Manage = Manage.INPUT
            How and whether Insight handles an entity. Defines how the system manages the entity data.
        read_only : bool = False
            Whether an entity is readonly. Specifies that the value(s) of the entity cannot be modified. See also
            `hidden`.
        transform_labels_entity : str = ""
            The name of an entity in the schema from which to read labels for values of this entity.
            The type of the index set of the labels entity must match the data type of this entity.
            The data type of the labels entity can be any primitive type.
        update_after_execution : bool = False
            Whether the value of the entity in the scenario is updated with the value of
            the corresponding model entity at the end of the scenario execution.
            If `True` the value of the entity is updated to correspond with the model entity after execution.
        update_progress : bool = False
            Whether the value of the entity in the scenario is sent on progress updates.
            If `True` the value of the entity will be written back to the Insight repository when
            :fct-ref:`insight.send_progress_update` is called from an execution mode where the `send_progress`
            attribute is `True`.
        entity_name : str = None
            The entity name. If not given, the name of the class attribute will be used instead.
            Only valid for entities in an `xi.ScenarioData`-decorated class.
        series_name : str = None
            The name to use for the values in the resultant series. If not given, the entity name will
            be used.
            Only valid for entities in an `xi.ScenarioData`-decorated class.
        index_types : List[BASIC_TYPE] = None
            The names of the columns to use for the index(es) in the resultant series. If not given, names derived from
            the index entities in the other scenario will be used. If given, the names must be unique and there must be
            one for each index column.
            Only valid for entities in an `xi.ScenarioData`-decorated class.

        Notes
        -----
        Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
        but it's recommended that you always use named arguments if you're specifying parameters other than `index`,
        `dtype` and `alias`.
        """

        #
        #
        self.__series_name = series_name

        super().__init__(
            dtype=dtype,
            #
            alias=alias,
            format=format,
            hidden=hidden,
            manage=manage,
            read_only=read_only,
            transform_labels_entity=transform_labels_entity,
            update_after_execution=update_after_execution,
            update_progress=update_progress,
            entity_name=entity_name
            #
        )

        self.__index_names: Optional[Tuple[str]] = validate_index_names(self, 'index', index)\
            if index else None
        self.__index_types: Optional[Tuple[BASIC_TYPE]] =\
            validate_list(self, 'index_types', BASIC_TYPE, 'BASIC_TYPE', index_types)\
            if index_types else None
        self.__index: Optional[Tuple[Index]] = None

    def _init_app_entity(self, entities: Mapping[str, EntityBase]):
        if self.__index is not None:
            raise RuntimeError(f'The {type(self).__name__} "{self.name}" has already been initialized.')

        if self.__index_names is not None:
            self.__index = get_index_tuple(self, self.__index_names, entities)

    def _check_valid_app_entity(self):
        super()._check_valid_app_entity()

        #
        if not self.index_names:
            raise TypeError("A Series entity in an App must have index names.")

        #
        if self.__index_types:
            raise TypeError('A Series entity in an App must have not set the "index_types" attribute.')

        #
        if self.__series_name:
            raise TypeError('A Series entity in an App must have not set the "series_name" attribute.')

    def _check_valid_scenario_data_entity(self):
        super()._check_valid_scenario_data_entity()

        #
        if self.__index_names and self.__index_types and len(self.__index_names) != len(self.__index_types):
            raise TypeError("A Series entity in a ScenarioData class must not specify different numbers of index names "
                            "and types.")

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        return pd.Series

    @property
    def index(self) -> Optional[Tuple[Index]]:
        return self.__index

    @property
    def index_names(self) -> Optional[Tuple[str]]:
        return self.__index_names

    @property
    def unique_index_names(self) -> Optional[List[str]]:
        """
        Index names, modified so that each is unique. Where an entity is indexed multiple times by the same index,
        duplicate names will be decorated with their index (e.g. ".2", ".3"). This will correspond to the labels
        of the indexes in the Pandas Series.
        """
        return get_index_level_names(self.index_names) if self.index_names else None

    @property
    def index_types(self) -> Optional[Tuple[BASIC_TYPE]]:
        if self.__index_types:
            return self.__index_types

        if self.index:
            #
            #
            dtypes: List[BASIC_TYPE] = []
            for ind in self.index:
                if not ind.dtype:
                    raise ValueError(f"No type configured for index entity {ind.name}")

                dtypes.append(ind.dtype)

            return tuple(dtypes)

        return None

    @property
    def series_name(self) -> Optional[str]:
        return self.__series_name if self.__series_name else self.name


class Column(Entity):
    """
    Represent a single column within a *DataFrame* entity. Outside the Python model (e.g. VDL, Tableau),
    the column will be represented as a separate entity whose name combines the names of the DataFrame and the Column,
    concatenated by an underscore, i.e. `MyDataFrame_MyColumnName`

    Examples
    --------
    Example of declaring two columns `NumDays` and `NumMonths` which will contain integer values within a DataFrame.

    >>> YearInfoFrame: xi.types.DataFrame(index='Years', columns=[
    ...     xi.types.Column("NumDays", dtype=xi.integer,
    ...                     alias="Number of days"),
    ...     xi.types.Column("NumMonths", dtype=xi.integer,
    ...                     alias="Number of years"),
    ... ])

    When accessing the Insight data model from outside the Python app (for example, in VDL or Tableau views, or using
    the Insight REST API), this DataFrame is represented as two entities, `YearInfoFrame_NumDays` and
    `YearInfoFrame_NumMonths`. If values are inserted into these individual column entities outside the Python
    app, it's possible their indexes may not be consistent (e.g. `YearInfoFrame_NumDays` having values for 2003, 2004
    and 2005 while `YearInfoFrame_NumMonths` has values for just 2003 and 2005). In this case, the empty cells in
    each column will be filled in with a default value when the DataFrame is loaded back into Python.

    See Also
    --------
    types.DataFrame
    """

    #
    def __init__(
            self,
            name: str,
            dtype: Optional[Type[BasicType[BASIC_TYPE_VALUE]]],
            #
            alias: str = "",
            format: str = "",
            hidden: Hidden = Hidden.FALSE,
            manage: Manage = Manage.INPUT,
            read_only: bool = False,
            transform_labels_entity: str = "",
            update_after_execution: bool = False,
            *,
            update_progress: bool = False,
            default: BASIC_TYPE_VALUE = None,
            entity_name: str = None
            #
    ):
        """
        Initializes `Column`.

        Parameters
        ----------
        name : str
            The name of the column.
        dtype : BASIC_TYPE
            The data type.
        alias : str = ""
            Used to provide an alternative name for an entity in the UI.
            The value is used in place of the entity name where appropriate in the UI.
        format : str = ""
            The formatting string used for displaying numeric values.
        hidden : Hidden = Hidden.FALSE
            Indicates whether the UI should hide the entity where appropriate.
        manage : Manage = Manage.INPUT
            How and whether Insight handles an entity. Defines how the system manages the entity data.
        read_only : bool = False
            Whether an entity is readonly. Specifies that the value(s) of the entity cannot be modified. See also
            `hidden`.
        transform_labels_entity : str = ""
            The name of an entity in the schema from which to read labels for values of this entity.
            The type of the index set of the labels entity must match the data type of this entity.
            The data type of the labels entity can be any primitive type.
        update_after_execution : bool = False
            Whether the value of the entity in the scenario is updated with the value of
            the corresponding model entity at the end of the scenario execution.
            If `True` the value of the entity is updated to correspond with the model entity after execution.
        update_progress : bool = False
            Whether the value of the entity in the scenario is sent on progress updates.
            If `True` the value of the entity will be written back to the Insight repository when
            :fct-ref:`insight.send_progress_update` is called from an execution mode where the `send_progress`
            attribute is `True`.
        default : Union[str, bool, int, float] = None
            The value to insert into any cells of this column that do not have a value when the DataFrame
            is loaded from the Insight scenario; optional. If specified, must be a value of the appropriate type for
            the `dtype` of this entity (e.g. a `str` if `dtype` is `xi.string`).
        entity_name : str = None
            The entity name. If not given, the name of the class attribute will be used instead.
            Only valid for entities in an `xi.ScenarioData`-decorated class.

        Notes
        -----
        Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
        but it's recommended that you always use named arguments if you're specifying parameters other than `name`,
        `dtype` and `alias`.
        """
        super().__init__(
            dtype=dtype,
            #
            alias=alias,
            format=format,
            hidden=hidden,
            manage=manage,
            read_only=read_only,
            transform_labels_entity=transform_labels_entity,
            update_after_execution=update_after_execution,
            update_progress=update_progress,
            entity_name=entity_name
            #
        )
        #
        self.name = name

        if default is None and dtype is not None:
            default = SCALAR_DEFAULT_VALUES[dtype]
            assert default is not None

        if default is not None:
            check_basic_type_value(dtype, default, name)

        self.__default = default

        self.__data_frame: Optional[EntityBase] = None

    def _init_column(self, data_frame: EntityBase):
        """
        Initializes the column to be part of the given frame.
        """
        if self.__data_frame is not None:
            raise TypeError("Column is already part of a frame")

        self.__data_frame = data_frame

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        #
        raise TypeError("A Column does not have a type hint")

    @property
    def default(self) -> Union[str, bool, int, float]:
        """
        The value used to fill empty cells in this column when the DataFrame is loaded from the Insight
        scenario.
        """
        return self.__default

    @property
    def _default_entity_name(self) -> str:
        return f"{self.__data_frame.name}_{self.name}"


class DataFrame(EntityBase):
    """
    The configuration of a *DataFrame* entity. Use the helper function `xpressinsight.types.DataFrame` to declare a
    DataFrame entity in an app, rather than  instantiating `xpressinsight.DataFrame` directly.

    Notes
    -----
    In older versions of `xpressinsight`, it was possible to use the `xi.DataFrame` as the annotation for an entity.
    This syntax is now deprecated and should not be used in new apps; it will not be supported in Python 3.12 and
    above.

    See Also
    --------
    types.DataFrame
    types.Index
    Column
    """

    def __init__(
            self,
            index: Optional[Union[str, List[str]]],
            columns: Union[Column, List[Column]],
            *,
            index_types: List[Type[BasicType]] = None
    ):
        """
        Initializes `DataFrame`.

        Parameters
        ----------
        index : Optional[Union[str, List[str]]] = None
            The name of the index to use, or list of names for multiple indices. The same index may appear in the list
            multiple times.
            Required for entities in an `xi.AppConfig`-decorated class, optional in an `xi.ScenarioData`-decorated
            class.
        columns : Union[Column, List[Column]]
            The columns which make up this data frame.
        index_types : Optional[List[Type[BasicType]]] = None
            The types of the columns to use for the index(es) in the resultant series.
            Only valid for entities in an `xi.ScenarioData`-decorated class, where it is optional.
        """
        super().__init__()
        self.__index_names: Tuple[str] = validate_index_names(self, 'index', index)\
            if index is not None else None
        self.__index: Optional[Tuple[Index]] = None
        self.__index_types: Optional[Tuple[BASIC_TYPE]] =\
            validate_list(self, 'index_types', BASIC_TYPE, 'BASIC_TYPE', index_types)\
            if index_types is not None else None
        self.__columns: Tuple[Column] = validate_list(self, 'columns', Column,
                                                      'xpressinsight.Column', deepcopy(columns))
        for col in self.__columns:
            col._init_column(self)

    def _init_app_entity(self, entities: Mapping[str, EntityBase]):
        if self.__index is not None:
            raise RuntimeError(f'The {type(self).__name__} "{self.name}" has already been initialized.')

        if self.__index_names is not None:
            self.__index = get_index_tuple(self, self.__index_names, entities)

    def _check_valid_app_entity(self):
        super()._check_valid_app_entity()

        #
        if not self.index_names:
            raise TypeError("A DataFrame entity in an App must have index names.")

        #
        if self.__index_types:
            raise TypeError('A DataFrame entity in an App must have not set the "index_types" attribute.')

        for col in self.columns:
            col._check_valid_app_entity()

    def _check_valid_scenario_data_entity(self):
        super()._check_valid_scenario_data_entity()

        #
        if self.__index_names and self.__index_types and len(self.__index_names) != len(self.__index_types):
            raise TypeError("A DataFrame entity in a ScenarioData class must not specify different numbers of index "
                            "names and types.")

        for col in self.columns:
            col._check_valid_scenario_data_entity()

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        return pd.DataFrame

    @property
    def index(self) -> Optional[Tuple[Index]]:
        return self.__index

    @property
    def index_names(self) -> Optional[Tuple[str]]:
        return self.__index_names

    @property
    def unique_index_names(self) -> Optional[List[str]]:
        """
        Index names, modified so that each is unique. Where an entity is indexed multiple times by the same index,
        duplicate names will be decorated with their index (e.g. ".2", ".3"). This will correspond to the labels
        of the indexes in the Pandas DataFrame.
        """
        return get_index_level_names(self.index_names) if self.index_names else None

    @property
    def index_types(self) -> Optional[Tuple[BASIC_TYPE]]:
        if self.__index_types:
            return self.__index_types

        if self.index:
            #
            #
            dtypes: List[BASIC_TYPE] = []
            for ind in self.index:
                if not ind.dtype:
                    raise ValueError(f"No type configured for index entity {ind.name}")

                dtypes.append(ind.dtype)

            return tuple(dtypes)

        return None

    @property
    def columns(self) -> Tuple[Column]:
        return self.__columns

    @property
    def update_progress(self) -> bool:
        """ Check whether DataFrame has any columns where the `update_progress` attribute is `True`. """
        return any(column.update_progress for column in self.columns)

    def is_managed(self, manage: Manage) -> bool:
        """ Check whether the DataFrame has a column that is managed as the given management type. """
        return any(column.is_managed(manage) for column in self.columns)


def data_frame_get_empty_index(df: DataFrame) -> pd.Index:
    """ Creates an empty pandas Index or MultiIndex with dtype and name information. """
    index_list = [
        pd.Index([], dtype=BASIC_PANDAS_DTYPE_MAP[index_type], name=level_name)
        for (level_name, index_type) in zip(get_index_level_names(df.index_names), df.index_types)
    ]

    if len(index_list) == 1:
        pd_index = index_list[0]
    else:
        pd_index = pd.MultiIndex.from_product(index_list)

    return pd_index


def check_str(s: Any) -> bool:
    """ Check if a value is a valid exportable string. """
    return isinstance(s, str) and len(s) <= MAX_STR_LENGTH_CHARS and '\0' not in s


def check_type_np(x: np.ndarray, t: Type[BasicType], name: str):
    """ Check if type of NumPy array x is compatible with type t and check bounds."""
    if x.size == 0:
        return

    if t == string:
        #
        #
        if not np.all(np.vectorize(check_str)(x)):
            msg = r"""
            All values in {} must be strings,
            must not be longer than {} characters,
            and must not contain the null character "\0".
            """.format(name, MAX_STR_LENGTH_CHARS)
            raise TypeError(msg)

    elif t == integer:
        if x.dtype.kind != "i":
            msg = """
            All values in {} must be integers, but the data type is: {}.
            """.format(
                name, x.dtype
            )
            raise TypeError(msg)

        #
        int32_limits = np.iinfo(np.int32)
        values = x

        if not (
                np.all(int32_limits.min <= values) and np.all(values <= int32_limits.max)
        ):
            msg = """
            All values in {} must fit into signed 32-bit integers.
            """.format(
                name
            )
            raise TypeError(msg)

    elif t == real:
        if x.dtype.kind != "f":
            msg = """
            All values in {} must be floats, but the data type is: {}.
            """.format(
                name, x.dtype
            )
            raise TypeError(msg)

        if np.finfo(x.dtype).bits > 64:
            msg = """
            All values in {} must fit into 64-bit floats.
            """.format(
                name
            )
            raise TypeError(msg)

    elif t == boolean:
        if x.dtype.kind != "b":
            msg = """
            All values in {} must be Booleans, but the data type is: {}.
            """.format(
                name, x.dtype
            )
            raise TypeError(msg)

    else:
        raise ValueError("Unexpected type passed to check_type_np: {}".format(t))


def check_type(
        x: Any, e: EntityBase, columns: Iterable[Column] = None
):
    """ Verify that x is the same type as given by e. """

    if isinstance(e, (Scalar, Param, Series)):
        if e.dtype and not issubclass(e.dtype, BasicType):
            msg = f"dtype of {e} must be a subclass of BasicType."
            raise TypeError(msg)

    #
    #
    #

    if isinstance(e, (Scalar, Param)):
        e.check_type(x)

    elif isinstance(e, Index):
        e.check_type(x, e.name)

    elif isinstance(e, (Series, DataFrame)):
        if isinstance(e, Series) and not isinstance(x, pd.Series):
            msg = f"""
            Problem with entity "{e.name}":
                Expected: pandas Series
                Actual: {type(x)}.
            """
            raise TypeError(msg)

        if isinstance(e, DataFrame) and not isinstance(x, pd.DataFrame):
            msg = f"""
            Problem with entity "{e.name}":
                Expected: pandas DataFrame
                Actual: {type(x)}.
            """
            raise TypeError(msg)

        #
        if e.index_names and len(e.index_names) != x.index.nlevels:
            msg = (f'Problem with entity "{e.name}": dimension of index set is {x.index.nlevels} '
                   f'but expecting {len(e.index_names)}.')
            raise TypeError(msg)

        if e.index_types:
            index_names = e.index_names or ["unnamed" for _typ in e.index_types]

            for idx_id, (idx_name, idx_dtype) in enumerate(zip(index_names, e.index_types)):
                check_index_type_value(x.index.get_level_values(idx_id), idx_dtype,
                                       f'index {idx_id} ("{idx_name}") of entity "{e.name}"')

        #
        if isinstance(e, Series):
            if e.dtype:
                check_type_np(x.values, e.dtype, e.name)

        elif isinstance(e, DataFrame):
            #
            #
            for column in (columns or e.columns):
                if column.name not in x.columns:
                    raise TypeError(f"Missing column '{column.name}' in DataFrame '{e.name}'")

                if column.dtype:
                    check_type_np(
                        x.loc[:, column.name].values,
                        column.dtype,
                        f"{e.name}.{column.name}"
                    )

    else:
        raise ValueError(f"Unexpected type passed to check_type: {e}")


def check_basic_type_value(dtype: Optional[BASIC_TYPE], value: Any, entity_name: str = ''):
    """ Verify given value can be stored as a given basic type in Insight.
        If dtype is not null, will infer the basic type from the value and then check
        that the value is valid for that type. """
    #
    #
    #

    if dtype is None:
        dtype = get_basic_type_for_python_type(type(value))

    #
    if (dtype == integer and isinstance(value, bool)) or\
            not isinstance(value, BASIC_TYPE_MAP.get(dtype)):
        raise TypeError("Value {} has type {} but should have type {}{}.".format(
            value,
            type(value).__name__,
            BASIC_TYPE_MAP[dtype].__name__,
            f" for entity {entity_name}" if entity_name else ""
        ))

    #
    if isinstance(value, str):
        if not len(value.encode("utf-8")) <= MAX_STR_LENGTH_BYTES:
            raise ValueError("String must not take more space than {} bytes{}.".format(
                MAX_STR_LENGTH_BYTES,
                f" when used in entity {entity_name}" if entity_name else ""
            ))

        if '\0' in value:
            raise ValueError("String must not contain the null character '\\0'{}.".format(
                f" when used in entity {entity_name}" if entity_name else ""
            ))

    elif isinstance(value, int) and not isinstance(value, bool):

        #
        int32_limits = np.iinfo(np.int32)

        if not (
                (int32_limits.min <= value) and (value <= int32_limits.max)
        ):
            raise TypeError("Value {} must fit into signed 32-bit integer{}.".format(
                value,
                f" when used in entity {entity_name}" if entity_name else ""
            ))

    elif isinstance(value, float):

        #
        pass


def check_index_type_value(value: Any, expected_dtype: Optional[BASIC_TYPE], name: str):
    """ Check the value of an Index entity is as expected."""
    if not isinstance(value, pd.Index):
        msg = f"""
        Problem with {name}:
            Expected: pandas.Index
            Actual: {type(value)}.
        """
        raise TypeError(msg)

    if value.size == 0:
        return

    if expected_dtype == integer:
        #
        if not pd.api.types.is_integer_dtype(value.dtype):
            msg = f"""
            All values in {name} must be integers, but the data type is: {value.dtype}.
            """
            raise TypeError(msg)

        check_type_np(value.values, integer, name)

    elif expected_dtype == real:
        #
        check_type_np(value.values, real, name)

    elif expected_dtype == string:
        #
        check_type_np(value.values, string, name)

    elif expected_dtype == boolean:
        if not pd.api.types.is_bool_dtype(value):
            msg = f"""
            All values in {name} must be Booleans.
            """
            raise TypeError(msg)

    elif expected_dtype:
        raise ValueError(f"Unexpected type: {expected_dtype}")


class ResultDataDelete(XiEnum):
    #
    """
    When to delete scenario results data.

    Attributes
    ----------
    ON_CHANGE
        Delete scenario result data when the scenario input-data is edited, or when scenario is queued for execution.
    ON_EXECUTE
        Delete scenario result data when scenario starts to execute.
    ON_QUEUE
        Delete scenario result data when scenario is queued for execution.

    See Also
    --------
    ResultData
    """

    ON_CHANGE = "on-change"
    ON_EXECUTE = "on-execute"
    ON_QUEUE = "on-queue"


class ResultData:
    """
    Class which specifies how to handle result data within the Insight server.

    Examples
    --------
    Example showing how to configure Insight to delete the result data when the
    scenario is queued for execution.

    >>> @xi.AppConfig(name="My App",
    ...               version=xi.AppVersion(1, 0, 0),
    ...               result_data=xi.ResultData(
    ...                   delete=xi.ResultDataDelete.ON_QUEUE
    ...               ))
    ... class InsightApp(xi.AppBase):
    ...     pass

    See Also
    --------
    AppConfig
    ResultData.__init__
    ResultDataDelete
    """

    __delete: ResultDataDelete

    def __init__(self, delete: ResultDataDelete = ResultDataDelete.ON_CHANGE):
        """
        Initializes `ResultData` with delete strategy.

        Parameters
        ----------
        delete: ResultDataDelete
            When to delete scenario results data.
            Results data is deleted when a certain state change occurs for the scenario.
            This attribute identifies this state change as either whenever a scenario is modified,
            when it is queued, or when it begins execution.

        See Also
        --------
        AppConfig
        ResultData
        ResultDataDelete
        """

        self.__delete = delete
        check_instance_attribute_types(self)

    def __repr__(self):
        return "ResultData(delete={})".format(repr(self.delete))

    @property
    def delete(self) -> ResultDataDelete:
        return self.__delete
