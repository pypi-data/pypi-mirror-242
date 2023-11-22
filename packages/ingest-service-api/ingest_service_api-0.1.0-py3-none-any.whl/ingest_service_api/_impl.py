# coding=utf-8
from abc import (
    abstractmethod,
)
import builtins
from conjure_python_client import (
    ConjureBeanType,
    ConjureDecoder,
    ConjureEncoder,
    ConjureFieldDefinition,
    ConjureUnionType,
    OptionalTypeWrapper,
    Service,
)
from requests.adapters import (
    Response,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

class ingest_Influx2LogQuery(ConjureBeanType):
    """
    Filters are ANDed together. Any `tagsToInclude` which exist in the query result
will be included in the log set as properties.
    """

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'start': ConjureFieldDefinition('start', ingest_UtcTimestamp),
            'end': ConjureFieldDefinition('end', ingest_UtcTimestamp),
            'bucket_filter': ConjureFieldDefinition('bucketFilter', ingest_BucketName),
            'measurement_filter': ConjureFieldDefinition('measurementFilter', ingest_MeasurementName),
            'tag_filters': ConjureFieldDefinition('tagFilters', Dict[ingest_TagName, ingest_TagValue]),
            'log_field': ConjureFieldDefinition('logField', ingest_FieldName),
            'tags_to_include': ConjureFieldDefinition('tagsToInclude', List[ingest_TagName])
        }

    __slots__: List[str] = ['_start', '_end', '_bucket_filter', '_measurement_filter', '_tag_filters', '_log_field', '_tags_to_include']

    def __init__(self, bucket_filter: str, end: "ingest_UtcTimestamp", log_field: str, measurement_filter: str, start: "ingest_UtcTimestamp", tag_filters: Dict[str, str], tags_to_include: List[str]) -> None:
        self._start = start
        self._end = end
        self._bucket_filter = bucket_filter
        self._measurement_filter = measurement_filter
        self._tag_filters = tag_filters
        self._log_field = log_field
        self._tags_to_include = tags_to_include

    @builtins.property
    def start(self) -> "ingest_UtcTimestamp":
        return self._start

    @builtins.property
    def end(self) -> "ingest_UtcTimestamp":
        return self._end

    @builtins.property
    def bucket_filter(self) -> str:
        return self._bucket_filter

    @builtins.property
    def measurement_filter(self) -> str:
        return self._measurement_filter

    @builtins.property
    def tag_filters(self) -> Dict[str, str]:
        return self._tag_filters

    @builtins.property
    def log_field(self) -> str:
        return self._log_field

    @builtins.property
    def tags_to_include(self) -> List[str]:
        return self._tags_to_include


ingest_Influx2LogQuery.__name__ = "Influx2LogQuery"
ingest_Influx2LogQuery.__qualname__ = "Influx2LogQuery"
ingest_Influx2LogQuery.__module__ = "ingest_service_api.ingest"


class ingest_IngestLogsFromConnectionRequest(ConjureBeanType):
    """
    Throws IncompatibleConnectionTypeAndLogQuery if those 2 inputs don't match.
    """

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'connection_rid': ConjureFieldDefinition('connectionRid', ingest_ConnectionRid),
            'log_query': ConjureFieldDefinition('logQuery', ingest_LogQuery),
            'log_set_spec': ConjureFieldDefinition('logSetSpec', ingest_LogSetSpec)
        }

    __slots__: List[str] = ['_connection_rid', '_log_query', '_log_set_spec']

    def __init__(self, connection_rid: str, log_query: "ingest_LogQuery", log_set_spec: "ingest_LogSetSpec") -> None:
        self._connection_rid = connection_rid
        self._log_query = log_query
        self._log_set_spec = log_set_spec

    @builtins.property
    def connection_rid(self) -> str:
        return self._connection_rid

    @builtins.property
    def log_query(self) -> "ingest_LogQuery":
        return self._log_query

    @builtins.property
    def log_set_spec(self) -> "ingest_LogSetSpec":
        return self._log_set_spec


ingest_IngestLogsFromConnectionRequest.__name__ = "IngestLogsFromConnectionRequest"
ingest_IngestLogsFromConnectionRequest.__qualname__ = "IngestLogsFromConnectionRequest"
ingest_IngestLogsFromConnectionRequest.__module__ = "ingest_service_api.ingest"


class ingest_IngestService(Service):

    def ingest_logs_from_connection(self, auth_header: str, request: "ingest_IngestLogsFromConnectionRequest") -> str:

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = ConjureEncoder().default(request)

        _path = '/ingest/v1/ingest-log-set'
        _path = _path.format(**_path_params)

        _response: Response = self._request(
            'POST',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), ingest_LogSetRid, self._return_none_for_unknown_union_types)


ingest_IngestService.__name__ = "IngestService"
ingest_IngestService.__qualname__ = "IngestService"
ingest_IngestService.__module__ = "ingest_service_api.ingest"


class ingest_LogQuery(ConjureUnionType):
    _influx2: Optional["ingest_Influx2LogQuery"] = None

    @builtins.classmethod
    def _options(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'influx2': ConjureFieldDefinition('influx2', ingest_Influx2LogQuery)
        }

    def __init__(
            self,
            influx2: Optional["ingest_Influx2LogQuery"] = None,
            type_of_union: Optional[str] = None
            ) -> None:
        if type_of_union is None:
            if (influx2 is not None) != 1:
                raise ValueError('a union must contain a single member')

            if influx2 is not None:
                self._influx2 = influx2
                self._type = 'influx2'

        elif type_of_union == 'influx2':
            if influx2 is None:
                raise ValueError('a union value must not be None')
            self._influx2 = influx2
            self._type = 'influx2'

    @builtins.property
    def influx2(self) -> Optional["ingest_Influx2LogQuery"]:
        return self._influx2

    def accept(self, visitor) -> Any:
        if not isinstance(visitor, ingest_LogQueryVisitor):
            raise ValueError('{} is not an instance of ingest_LogQueryVisitor'.format(visitor.__class__.__name__))
        if self._type == 'influx2' and self.influx2 is not None:
            return visitor._influx2(self.influx2)


ingest_LogQuery.__name__ = "LogQuery"
ingest_LogQuery.__qualname__ = "LogQuery"
ingest_LogQuery.__module__ = "ingest_service_api.ingest"


class ingest_LogQueryVisitor:

    @abstractmethod
    def _influx2(self, influx2: "ingest_Influx2LogQuery") -> Any:
        pass


ingest_LogQueryVisitor.__name__ = "LogQueryVisitor"
ingest_LogQueryVisitor.__qualname__ = "LogQueryVisitor"
ingest_LogQueryVisitor.__module__ = "ingest_service_api.ingest"


class ingest_LogSetSpec(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'name': ConjureFieldDefinition('name', str),
            'description': ConjureFieldDefinition('description', str)
        }

    __slots__: List[str] = ['_name', '_description']

    def __init__(self, description: str, name: str) -> None:
        self._name = name
        self._description = description

    @builtins.property
    def name(self) -> str:
        return self._name

    @builtins.property
    def description(self) -> str:
        return self._description


ingest_LogSetSpec.__name__ = "LogSetSpec"
ingest_LogSetSpec.__qualname__ = "LogSetSpec"
ingest_LogSetSpec.__module__ = "ingest_service_api.ingest"


class ingest_UtcTimestamp(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'seconds_since_epoch': ConjureFieldDefinition('secondsSinceEpoch', int),
            'offset_nanoseconds': ConjureFieldDefinition('offsetNanoseconds', OptionalTypeWrapper[int])
        }

    __slots__: List[str] = ['_seconds_since_epoch', '_offset_nanoseconds']

    def __init__(self, seconds_since_epoch: int, offset_nanoseconds: Optional[int] = None) -> None:
        self._seconds_since_epoch = seconds_since_epoch
        self._offset_nanoseconds = offset_nanoseconds

    @builtins.property
    def seconds_since_epoch(self) -> int:
        return self._seconds_since_epoch

    @builtins.property
    def offset_nanoseconds(self) -> Optional[int]:
        return self._offset_nanoseconds


ingest_UtcTimestamp.__name__ = "UtcTimestamp"
ingest_UtcTimestamp.__qualname__ = "UtcTimestamp"
ingest_UtcTimestamp.__module__ = "ingest_service_api.ingest"


ingest_MeasurementName = str

ingest_LogSetRid = str

ingest_FieldName = str

ingest_TagValue = str

ingest_BucketName = str

ingest_TagName = str

ingest_ConnectionRid = str

