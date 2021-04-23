import collections
import unittest
from typing import Any, Optional

from odoo.api import Environment
from odoo.modules.registry import Registry
from odoo.sql_db import Cursor

_logger: Any
ADDONS_PATH: Any
HOST: str
ADMIN_USER_ID: Any

def get_db_name(): ...

standalone_tests: Any

def standalone(*tags: Any): ...

DB: Any

def new_test_user(env: Any, login: str = ..., groups: str = ..., context: Optional[Any] = ..., **kwargs: Any): ...

class OdooSuite(unittest.suite.TestSuite):
    def _handleClassSetUp(self, test: Any, result: Any) -> None: ...
    def _createClassOrModuleLevelException(self, result: Any, exc: Any, method_name: Any, parent: Any, info: Optional[Any] = ...) -> None: ...
    def _addClassOrModuleLevelException(self, result: Any, exception: Any, errorName: Any, info: Optional[Any] = ...) -> None: ...
    def _tearDownPreviousClass(self, test: Any, result: Any) -> None: ...

class TreeCase(unittest.TestCase):
    _class_cleanups: Any = ...
    @classmethod
    def addClassCleanup(cls, function: Any, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def doClassCleanups(cls) -> None: ...
    def __init__(self, methodName: str = ...) -> None: ...
    def assertTreesEqual(self, n1: Any, n2: Any, msg: Optional[Any] = ...) -> None: ...

class MetaCase(type):
    def __init__(cls, name: Any, bases: Any, attrs: Any) -> None: ...

class BaseCase(TreeCase):
    longMessage: bool = ...
    warm: bool = ...
    registry: Registry = ...
    cr: Cursor = ...
    env: Environment = ...
    def cursor(self): ...
    @property
    def uid(self): ...
    @uid.setter
    def uid(self, user: Any) -> None: ...
    def ref(self, xid: Any): ...
    def browse_ref(self, xid: Any): ...
    def with_user(self, login: Any) -> None: ...
    def _assertRaises(self, exception: Any, *, msg: Optional[Any] = ...) -> None: ...
    def assertRaises(self, exception: Any, func: Optional[Any] = ..., *args: Any, **kwargs: Any): ...
    def assertQueries(self, expected: Any, flush: bool = ...): ...
    def assertQueryCount(self, default: int = ..., flush: bool = ..., **counters: Any): ...
    def assertRecordValues(self, records: Any, expected_values: Any): ...
    def shortDescription(self) -> None: ...
    def assertItemsEqual(self, a: Any, b: Any, msg: Optional[Any] = ...) -> None: ...

class TransactionCase(BaseCase):
    def setUp(self): ...
    def patch(self, obj: Any, key: Any, val: Any) -> None: ...
    def patch_order(self, model: Any, order: Any) -> None: ...

class SingleTransactionCase(BaseCase):
    @classmethod
    def setUpClass(cls) -> None: ...
    def setUp(self) -> None: ...

savepoint_seq: Any

class SavepointCase(SingleTransactionCase):
    _savepoint_id: Any = ...
    def setUp(self) -> None: ...

class ChromeBrowserException(Exception): ...

class ChromeBrowser:
    _logger: Any = ...
    test_class: Any = ...
    devtools_port: Any = ...
    ws_url: str = ...
    ws: Any = ...
    request_id: int = ...
    user_data_dir: Any = ...
    chrome_pid: Any = ...
    screenshots_dir: Any = ...
    screencasts_dir: Any = ...
    screencast_frames: Any = ...
    window_size: Any = ...
    sigxcpu_handler: Any = ...
    def __init__(self, logger: Any, window_size: Any, test_class: Any) -> None: ...
    def signal_handler(self, sig: Any, frame: Any) -> None: ...
    def stop(self) -> None: ...
    @property
    def executable(self): ...
    def _spawn_chrome(self, cmd: Any): ...
    def _chrome_start(self) -> None: ...
    def _find_websocket(self) -> None: ...
    def _json_command(self, command: Any, timeout: int = ..., get_key: Optional[Any] = ...): ...
    def _open_websocket(self) -> None: ...
    def _websocket_send(self, method: Any, params: Optional[Any] = ...): ...
    def _get_message(self, raise_log_error: bool = ...): ...
    _TO_LEVEL: Any = ...
    def _websocket_wait_id(self, awaited_id: Any, timeout: int = ...): ...
    def _websocket_wait_event(self, method: Any, params: Optional[Any] = ..., timeout: int = ...): ...
    def take_screenshot(self, prefix: str = ..., suffix: Optional[Any] = ...) -> None: ...
    def _save_screencast(self, prefix: str = ...) -> None: ...
    screencasts_frames_dir: Any = ...
    def start_screencast(self) -> None: ...
    def set_cookie(self, name: Any, value: Any, path: Any, domain: Any): ...
    def delete_cookie(self, name: Any, **kwargs: Any): ...
    def _wait_ready(self, ready_code: Any, timeout: int = ...): ...
    def _wait_code_ok(self, code: Any, timeout: Any): ...
    def navigate_to(self, url: Any, wait_stop: bool = ...) -> None: ...
    def clear(self) -> None: ...
    def _from_remoteobject(self, arg: Any): ...
    LINE_PATTERN: str = ...
    def _format_stack(self, logrecord: Any) -> None: ...
    def console_formatter(self, args: Any): ...

class HttpCaseCommon(BaseCase):
    registry_test_mode: bool = ...
    browser: Any = ...
    browser_size: str = ...
    xmlrpc_url: Any = ...
    xmlrpc_common: Any = ...
    xmlrpc_db: Any = ...
    xmlrpc_object: Any = ...
    def __init__(self, methodName: str = ...) -> None: ...
    opener: Any = ...
    def setUp(self) -> None: ...
    @classmethod
    def start_browser(cls) -> None: ...
    @classmethod
    def terminate_browser(cls) -> None: ...
    def url_open(self, url: Any, data: Optional[Any] = ..., files: Optional[Any] = ..., timeout: int = ..., headers: Optional[Any] = ..., allow_redirects: bool = ...): ...
    def _wait_remaining_requests(self, timeout: int = ...): ...
    def logout(self, keep_db: bool = ...) -> None: ...
    session: Any = ...
    def authenticate(self, user: Any, password: Any): ...
    def browser_js(self, url_path: Any, code: Any, ready: str = ..., login: Optional[Any] = ..., timeout: int = ..., **kw: Any) -> None: ...
    def start_tour(self, url_path: Any, tour_name: Any, step_delay: Optional[Any] = ..., **kwargs: Any): ...

class HttpCase(HttpCaseCommon, TransactionCase): ...
class HttpSavepointCase(HttpCaseCommon, SavepointCase): ...

def users(*logins: Any): ...
def warmup(func: Any, *args: Any, **kwargs: Any) -> None: ...
def can_import(module: Any): ...

ref_re: Any

class Form:
    def __init__(self, recordp: Any, view: Optional[Any] = ...) -> None: ...
    def _o2m_set_edition_view(self, descr: Any, node: Any, level: Any) -> None: ...
    def __str__(self): ...
    def _process_fvg(self, model: Any, fvg: Any, level: int = ...) -> None: ...
    def _init_from_defaults(self, model: Any) -> None: ...
    def _init_from_values(self, values: Any) -> None: ...
    def __getattr__(self, field: Any): ...
    def _get_modifier(self, field: Any, modifier: Any, default: bool = ..., modmap: Optional[Any] = ..., vals: Optional[Any] = ...): ...
    _OPS: Any = ...
    def _get_context(self, field: Any): ...
    def __setattr__(self, field: Any, value: Any) -> None: ...
    def __enter__(self): ...
    def __exit__(self, etype: Any, _evalue: Any, _etb: Any) -> None: ...
    def save(self): ...
    def _values_to_save(self, all_fields: bool = ...): ...
    def _values_to_save_(self, record_values: Any, fields: Any, view: Any, changed: Any, all_fields: bool = ..., modifiers_values: Optional[Any] = ..., parent_link: Optional[Any] = ...): ...
    def _perform_onchange(self, fields: Any) -> None: ...
    def _onchange_values(self): ...
    def _onchange_values_(self, fields: Any, record: Any): ...
    def _cleanup_onchange(self, descr: Any, value: Any, current: Any): ...

class O2MForm(Form):
    def __init__(self, proxy: Any, index: Optional[Any] = ...) -> None: ...
    def _get_modifier(self, field: Any, modifier: Any, default: bool = ..., modmap: Optional[Any] = ..., vals: Optional[Any] = ...): ...
    def _onchange_values(self): ...
    def save(self) -> None: ...
    def _values_to_save(self, all_fields: bool = ...): ...

class UpdateDict(dict):
    _changed: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def changed_items(self): ...
    def update(self, *args: Any, **kw: Any) -> None: ...

class X2MProxy:
    _parent: Any = ...
    _field: Any = ...
    def _assert_editable(self) -> None: ...

class O2MProxy(X2MProxy):
    _parent: Any = ...
    _field: Any = ...
    _records: Any = ...
    def __init__(self, parent: Any, field: Any) -> None: ...
    def __len__(self): ...
    @property
    def _model(self): ...
    @property
    def _descr(self): ...
    def _command_index(self, for_record: Any): ...
    def new(self): ...
    def edit(self, index: Any): ...
    def remove(self, index: Any) -> None: ...

class M2MProxy(X2MProxy, collections.Sequence):
    _parent: Any = ...
    _field: Any = ...
    def __init__(self, parent: Any, field: Any) -> None: ...
    def __getitem__(self, it: Any): ...
    def __len__(self): ...
    def __iter__(self) -> Any: ...
    def __contains__(self, record: Any): ...
    def add(self, record: Any) -> None: ...
    def _get_ids(self): ...
    def remove(self, id: Optional[Any] = ..., index: Optional[Any] = ...) -> None: ...
    def clear(self) -> None: ...

def record_to_values(fields: Any, record: Any): ...
def _cleanup_from_default(type_: Any, value: Any): ...
def _get_node(view: Any, f: Any, *arg: Any): ...
def tagged(*tags: Any): ...

class TagsSelector:
    filter_spec_re: Any = ...
    exclude: Any = ...
    include: Any = ...
    def __init__(self, spec: Any) -> None: ...
    def check(self, test: Any): ...
