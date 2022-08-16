Search.setIndex({"docnames": ["README", "api", "generated/rxn.utilities", "generated/rxn.utilities.attrs", "generated/rxn.utilities.attrs.get_class_attributes", "generated/rxn.utilities.attrs.get_variables", "generated/rxn.utilities.attrs.get_variables_and_type_names", "generated/rxn.utilities.attrs.get_variables_and_types", "generated/rxn.utilities.basic", "generated/rxn.utilities.basic.identity", "generated/rxn.utilities.caching", "generated/rxn.utilities.caching.cached_on_disk", "generated/rxn.utilities.containers", "generated/rxn.utilities.containers.all_identical", "generated/rxn.utilities.containers.chunker", "generated/rxn.utilities.containers.pairwise", "generated/rxn.utilities.containers.remove_duplicates", "generated/rxn.utilities.databases", "generated/rxn.utilities.databases.pymongo", "generated/rxn.utilities.databases.pymongo.PyMongoSettings", "generated/rxn.utilities.databases.pymongo.get_pymongo_settings", "generated/rxn.utilities.files", "generated/rxn.utilities.files.count_lines", "generated/rxn.utilities.files.dump_list_to_file", "generated/rxn.utilities.files.is_path_creatable", "generated/rxn.utilities.files.is_path_exists_or_creatable", "generated/rxn.utilities.files.is_pathname_valid", "generated/rxn.utilities.files.iterate_lines_from_file", "generated/rxn.utilities.files.load_list_from_file", "generated/rxn.utilities.logging", "generated/rxn.utilities.logging.LoggingFormat", "generated/rxn.utilities.logging.log_debug", "generated/rxn.utilities.logging.log_error", "generated/rxn.utilities.logging.log_info", "generated/rxn.utilities.logging.log_warning", "generated/rxn.utilities.logging.setup_console_and_file_logger", "generated/rxn.utilities.logging.setup_console_logger", "generated/rxn.utilities.logging.setup_file_logger", "generated/rxn.utilities.regex", "generated/rxn.utilities.regex.alternation", "generated/rxn.utilities.regex.capturing", "generated/rxn.utilities.regex.optional", "generated/rxn.utilities.scripts", "generated/rxn.utilities.scripts.stable_shuffle", "generated/rxn.utilities.strings", "generated/rxn.utilities.strings.escape_latex", "generated/rxn.utilities.strings.remove_postfix", "generated/rxn.utilities.strings.remove_prefix", "generated/rxn.utilities.types", "generated/rxn.utilities.types.RxnEnum", "index"], "filenames": ["README.md", "api.rst", "generated/rxn.utilities.rst", "generated/rxn.utilities.attrs.rst", "generated/rxn.utilities.attrs.get_class_attributes.rst", "generated/rxn.utilities.attrs.get_variables.rst", "generated/rxn.utilities.attrs.get_variables_and_type_names.rst", "generated/rxn.utilities.attrs.get_variables_and_types.rst", "generated/rxn.utilities.basic.rst", "generated/rxn.utilities.basic.identity.rst", "generated/rxn.utilities.caching.rst", "generated/rxn.utilities.caching.cached_on_disk.rst", "generated/rxn.utilities.containers.rst", "generated/rxn.utilities.containers.all_identical.rst", "generated/rxn.utilities.containers.chunker.rst", "generated/rxn.utilities.containers.pairwise.rst", "generated/rxn.utilities.containers.remove_duplicates.rst", "generated/rxn.utilities.databases.rst", "generated/rxn.utilities.databases.pymongo.rst", "generated/rxn.utilities.databases.pymongo.PyMongoSettings.rst", "generated/rxn.utilities.databases.pymongo.get_pymongo_settings.rst", "generated/rxn.utilities.files.rst", "generated/rxn.utilities.files.count_lines.rst", "generated/rxn.utilities.files.dump_list_to_file.rst", "generated/rxn.utilities.files.is_path_creatable.rst", "generated/rxn.utilities.files.is_path_exists_or_creatable.rst", "generated/rxn.utilities.files.is_pathname_valid.rst", "generated/rxn.utilities.files.iterate_lines_from_file.rst", "generated/rxn.utilities.files.load_list_from_file.rst", "generated/rxn.utilities.logging.rst", "generated/rxn.utilities.logging.LoggingFormat.rst", "generated/rxn.utilities.logging.log_debug.rst", "generated/rxn.utilities.logging.log_error.rst", "generated/rxn.utilities.logging.log_info.rst", "generated/rxn.utilities.logging.log_warning.rst", "generated/rxn.utilities.logging.setup_console_and_file_logger.rst", "generated/rxn.utilities.logging.setup_console_logger.rst", "generated/rxn.utilities.logging.setup_file_logger.rst", "generated/rxn.utilities.regex.rst", "generated/rxn.utilities.regex.alternation.rst", "generated/rxn.utilities.regex.capturing.rst", "generated/rxn.utilities.regex.optional.rst", "generated/rxn.utilities.scripts.rst", "generated/rxn.utilities.scripts.stable_shuffle.rst", "generated/rxn.utilities.strings.rst", "generated/rxn.utilities.strings.escape_latex.rst", "generated/rxn.utilities.strings.remove_postfix.rst", "generated/rxn.utilities.strings.remove_prefix.rst", "generated/rxn.utilities.types.rst", "generated/rxn.utilities.types.RxnEnum.rst", "index.md"], "titles": ["RXN utilities package", "API", "rxn.utilities", "rxn.utilities.attrs", "rxn.utilities.attrs.get_class_attributes", "rxn.utilities.attrs.get_variables", "rxn.utilities.attrs.get_variables_and_type_names", "rxn.utilities.attrs.get_variables_and_types", "rxn.utilities.basic", "rxn.utilities.basic.identity", "rxn.utilities.caching", "rxn.utilities.caching.cached_on_disk", "rxn.utilities.containers", "rxn.utilities.containers.all_identical", "rxn.utilities.containers.chunker", "rxn.utilities.containers.pairwise", "rxn.utilities.containers.remove_duplicates", "rxn.utilities.databases", "rxn.utilities.databases.pymongo", "rxn.utilities.databases.pymongo.PyMongoSettings", "rxn.utilities.databases.pymongo.get_pymongo_settings", "rxn.utilities.files", "rxn.utilities.files.count_lines", "rxn.utilities.files.dump_list_to_file", "rxn.utilities.files.is_path_creatable", "rxn.utilities.files.is_path_exists_or_creatable", "rxn.utilities.files.is_pathname_valid", "rxn.utilities.files.iterate_lines_from_file", "rxn.utilities.files.load_list_from_file", "rxn.utilities.logging", "rxn.utilities.logging.LoggingFormat", "rxn.utilities.logging.log_debug", "rxn.utilities.logging.log_error", "rxn.utilities.logging.log_info", "rxn.utilities.logging.log_warning", "rxn.utilities.logging.setup_console_and_file_logger", "rxn.utilities.logging.setup_console_logger", "rxn.utilities.logging.setup_file_logger", "rxn.utilities.regex", "rxn.utilities.regex.alternation", "rxn.utilities.regex.capturing", "rxn.utilities.regex.optional", "rxn.utilities.scripts", "rxn.utilities.scripts.stable_shuffle", "rxn.utilities.strings", "rxn.utilities.strings.escape_latex", "rxn.utilities.strings.remove_postfix", "rxn.utilities.strings.remove_prefix", "rxn.utilities.types", "rxn.utilities.types.RxnEnum", "RXN utilities"], "terms": {"thi": [0, 19, 25], "repositori": 0, "contain": [0, 46, 47, 50], "gener": [0, 14, 19, 27, 49], "python": [0, 14, 31, 32, 33, 34, 50], "commonli": 0, "us": [0, 11, 19, 30, 31, 32, 33, 34, 48], "univers": [0, 30], "For": 0, "relat": [0, 18], "chemistri": 0, "see": [0, 38], "our": 0, "other": [0, 19], "chemutil": 0, "The": [0, 45], "document": [0, 14], "can": [0, 31, 32, 33, 34], "found": [0, 46, 47, 49], "here": 0, "support": 0, "all": [0, 13, 19, 49], "oper": [0, 39], "It": 0, "ha": [0, 24, 49], "been": 0, "test": [0, 31, 32, 33, 34, 38], "follow": [0, 49], "maco": 0, "big": 0, "sur": 0, "11": 0, "1": 0, "linux": 0, "ubuntu": 0, "18": 0, "04": 0, "4": 0, "A": 0, "version": 0, "3": [0, 14], "6": 0, "greater": 0, "recommend": 0, "from": [0, 14, 15, 16, 19, 24, 25, 26, 31, 32, 33, 34, 45, 46, 47, 49], "pypi": 0, "pip": 0, "local": 0, "develop": 0, "e": [0, 11, 35, 36, 37, 49], "dev": 0, "modul": [2, 17, 42, 50], "helper": 3, "function": [3, 8, 10, 11, 12, 14, 18, 19, 21, 25, 29, 31, 32, 33, 34, 38, 44, 49], "handl": 3, "class": [3, 4, 5, 6, 7, 18, 19, 29, 30, 48, 49], "defin": 3, "packag": [3, 31, 32, 33, 34], "cl": [4, 5, 6, 7, 19, 49], "sourc": [4, 5, 6, 7, 9, 11, 13, 14, 15, 16, 19, 20, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 45, 46, 47, 49], "return": [4, 5, 6, 7, 9, 13, 14, 15, 16, 19, 20, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 45, 46, 47, 49], "attribut": [4, 19, 30], "declar": [4, 5, 6, 7], "librari": [4, 5, 6, 7, 14], "paramet": [4, 5, 6, 7, 9, 13, 14, 15, 16, 19, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 45, 46, 47, 49], "type": [4, 5, 6, 7, 9, 13, 14, 15, 16, 19, 20, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 45, 46, 47, 50], "iter": [4, 14, 15, 16, 23, 39], "name": [5, 6, 7], "variabl": [5, 6, 7], "list": [5, 6, 7, 14, 15, 16, 28], "str": [5, 6, 7, 11, 19, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 45, 46, 47, 49], "correspond": [6, 7], "tupl": [6, 7, 15], "x": 9, "typevar": [9, 14, 15, 16, 49], "t": [9, 14, 15, 16, 49], "func": 11, "decor": 11, "reli": 11, "disk": 11, "when": 11, "functool": 11, "lru_cach": 11, "cannot": [11, 19], "becaus": 11, "thread": 11, "especi": 11, "celeri": 11, "worker": 11, "simplifi": 11, "syntax": 11, "compar": [11, 49], "diskcach": 11, "onli": 11, "note": [11, 19], "make": [11, 19, 41], "differ": 11, "between": 11, "arg": 11, "kwarg": 11, "i": [11, 35, 36, 37, 49], "call": 11, "one": 11, "time": 11, "argument": [11, 19], "keyword": [11, 19], "lead": 11, "wrap": 11, "bodi": 11, "being": 11, "execut": 11, "two": 11, "exampl": [11, 38, 45], "def": 11, "foo": 11, "bar": 11, "sequenc": [13, 16], "evalu": 13, "whether": [13, 46, 47], "element": [13, 16], "ar": [13, 19], "ident": 13, "ani": [13, 19], "bool": [13, 19, 24, 25, 26, 46, 47], "chunk_siz": 14, "fill_valu": 14, "object": [14, 19], "through": 14, "an": [14, 19, 49], "chunk": 14, "given": [14, 35, 37], "size": 14, "adapt": [14, 16, 45], "grouper": 14, "itertool": 14, "http": [14, 15, 16, 24, 25, 26, 45], "doc": 14, "org": 14, "html": 14, "recip": 14, "some": 14, "creat": [14, 19, 24, 41], "int": [14, 22, 35, 36, 37], "default": [14, 16, 19, 35, 36, 37, 46, 47], "0x7f9d0e5c2ab0": 14, "valu": [14, 19, 23, 30, 35, 36, 37, 49], "fill": 14, "last": 14, "too": 14, "small": 14, "If": 14, "noth": 14, "specifi": [14, 19], "mai": 14, "smaller": 14, "none": [14, 16, 19, 23, 27, 31, 32, 33, 34, 35, 36, 37], "over": [14, 15, 19], "repres": 14, "s": [15, 35, 36, 37], "neighbor": 15, "s0": 15, "s1": 15, "s2": 15, "s3": 15, "stackoverflow": [15, 16, 24, 25, 26, 45], "com": [15, 16, 24, 25, 26, 45], "5434936": 15, "seq": 16, "kei": 16, "remov": [16, 46, 47], "duplic": [16, 19], "preserv": 16, "order": 16, "480227": 16, "option": [16, 19], "callabl": [16, 19], "v": 16, "what": 16, "base": [16, 19, 30, 49], "must": 16, "hashabl": 16, "_env_fil": 19, "_env_file_encod": 19, "_env_nested_delimit": 19, "_secrets_dir": 19, "baseset": 19, "set": [19, 35, 36, 37], "connect": 19, "mongodb": 19, "via": 19, "union": [19, 22, 23, 24, 25, 26, 27, 28, 35, 36, 37], "pathlik": [19, 22, 23, 24, 25, 26, 27, 28, 35, 37], "0x7f9d0e5c2f10": 19, "mongo_uri": 19, "tls_ca_certificate_path": 19, "__init__": [19, 30, 49], "new": 19, "model": 19, "pars": 19, "valid": [19, 25, 26, 49], "input": 19, "data": 19, "rais": [19, 25, 46, 47, 49], "validationerror": 19, "form": 19, "method": [19, 49], "classmethod": [19, 49], "construct": [19, 49], "_fields_set": 19, "__dict__": 19, "__fields_set__": 19, "trust": 19, "pre": 19, "respect": 19, "perform": 19, "behav": 19, "config": 19, "extra": 19, "allow": 19, "wa": 19, "sinc": 19, "add": [19, 40], "pass": [19, 24, 25, 26], "setstr": 19, "copi": [19, 24, 25, 26], "includ": 19, "exclud": 19, "updat": 19, "deep": 19, "fals": [19, 24, 25, 26, 39, 41, 46, 47], "choos": 19, "which": 19, "field": 19, "chang": 19, "abstractsetintstr": 19, "mappingintstrani": 19, "take": 19, "preced": 19, "dictstrani": 19, "befor": 19, "you": 19, "should": 19, "true": [19, 24, 25, 26, 46, 47], "self": 19, "instanc": [19, 49], "dict": 19, "by_alia": 19, "skip_default": 19, "exclude_unset": 19, "exclude_default": 19, "exclude_non": 19, "dictionari": 19, "represent": [19, 49], "get_client": 19, "instanti": [19, 49], "mongo": 19, "client": 19, "provid": 19, "ssl": 19, "mongocli": 19, "static": 19, "instantiate_cli": 19, "string": [19, 35, 36, 37, 38, 40, 41, 49, 50], "path": 19, "ca": 19, "certif": 19, "json": 19, "encod": 19, "models_as_dict": 19, "dumps_kwarg": 19, "per": 19, "suppli": 19, "dump": 19, "unicod": 19, "update_forward_ref": 19, "localn": 19, "try": 19, "forwardref": 19, "globaln": 19, "pymongoset": 20, "filenam": [22, 23, 27, 28, 35, 37], "pathnam": [24, 25, 26], "current": [24, 25, 26], "user": 24, "suffici": 24, "permiss": 24, "otherwis": [24, 25, 26], "34102855": [24, 25, 26], "more": [24, 25, 26], "detail": [24, 25, 26], "os": [25, 26], "_and_": 25, "either": [25, 35, 36, 37], "exist": 25, "hypothet": 25, "creatabl": 25, "guarante": 25, "_never_": 25, "except": 25, "enum": [30, 49], "common": 30, "format": [30, 35, 36, 37], "messag": [31, 32, 33, 34, 35, 36, 37, 45], "debug": 31, "level": [31, 32, 33, 34, 35, 36, 37], "purpos": [31, 32, 33, 34], "capabl": [31, 32, 33, 34], "anoth": [31, 32, 33, 34, 49], "error": 32, "info": [33, 35, 36, 37], "warn": 34, "loggingformat": [35, 36, 37], "basic": [35, 36, 37, 50], "up": [35, 36, 37], "logger": [35, 36, 37], "write": [35, 36, 37], "both": [35, 49], "termin": 35, "file": [35, 37, 50], "overwrit": [35, 37], "mode": [35, 37], "w": [35, 37], "integ": [35, 36, 37], "asctim": [35, 36, 37], "levelnam": [35, 36, 37], "directli": [35, 36, 37], "consol": 36, "stderr": 36, "help": 38, "build": 38, "choic": 39, "capture_group": [39, 41], "OR": 39, "initial_regex": [40, 41], "parenthes": 40, "group": 41, "text": [45, 46, 47], "escap": 45, "special": 45, "latex": 45, "charact": 45, "25875504": 45, "convert": [45, 49], "30": 45, "appear": 45, "correctli": 45, "postfix": 46, "raise_if_miss": [46, 47], "present": [46, 47], "its": [46, 47, 49], "end": 46, "potenti": [46, 47], "valueerror": [46, 47, 49], "prefix": 47, "begin": 47, "custom": [48, 49], "project": 48, "addit": 49, "convers": 49, "standard": 49, "to_str": 49, "lowercas": 49, "from_str": 49, "constructor": 49, "possibl": 49, "bound": 49, "readm": 50, "system": 50, "requir": 50, "instal": 50, "guid": 50, "api": 50, "attr": 50, "cach": 50, "databas": 50, "log": 50, "regex": 50, "script": 50, "index": 50, "search": 50}, "objects": {"rxn": [[2, 0, 0, "-", "utilities"]], "rxn.utilities": [[3, 0, 0, "-", "attrs"], [8, 0, 0, "-", "basic"], [10, 0, 0, "-", "caching"], [12, 0, 0, "-", "containers"], [17, 0, 0, "-", "databases"], [21, 0, 0, "-", "files"], [29, 0, 0, "-", "logging"], [38, 0, 0, "-", "regex"], [42, 0, 0, "-", "scripts"], [44, 0, 0, "-", "strings"], [48, 0, 0, "-", "types"]], "rxn.utilities.attrs": [[4, 1, 1, "", "get_class_attributes"], [5, 1, 1, "", "get_variables"], [6, 1, 1, "", "get_variables_and_type_names"], [7, 1, 1, "", "get_variables_and_types"]], "rxn.utilities.basic": [[9, 1, 1, "", "identity"]], "rxn.utilities.caching": [[11, 1, 1, "", "cached_on_disk"]], "rxn.utilities.containers": [[13, 1, 1, "", "all_identical"], [14, 1, 1, "", "chunker"], [15, 1, 1, "", "pairwise"], [16, 1, 1, "", "remove_duplicates"]], "rxn.utilities.databases": [[18, 0, 0, "-", "pymongo"]], "rxn.utilities.databases.pymongo": [[19, 2, 1, "", "PyMongoSettings"], [20, 1, 1, "", "get_pymongo_settings"]], "rxn.utilities.databases.pymongo.PyMongoSettings": [[19, 3, 1, "", "__init__"], [19, 3, 1, "", "construct"], [19, 3, 1, "", "copy"], [19, 3, 1, "", "dict"], [19, 3, 1, "", "get_client"], [19, 3, 1, "", "instantiate_client"], [19, 3, 1, "", "json"], [19, 3, 1, "", "update_forward_refs"]], "rxn.utilities.files": [[22, 1, 1, "", "count_lines"], [23, 1, 1, "", "dump_list_to_file"], [24, 1, 1, "", "is_path_creatable"], [25, 1, 1, "", "is_path_exists_or_creatable"], [26, 1, 1, "", "is_pathname_valid"], [27, 1, 1, "", "iterate_lines_from_file"], [28, 1, 1, "", "load_list_from_file"]], "rxn.utilities.logging": [[30, 2, 1, "", "LoggingFormat"], [31, 1, 1, "", "log_debug"], [32, 1, 1, "", "log_error"], [33, 1, 1, "", "log_info"], [34, 1, 1, "", "log_warning"], [35, 1, 1, "", "setup_console_and_file_logger"], [36, 1, 1, "", "setup_console_logger"], [37, 1, 1, "", "setup_file_logger"]], "rxn.utilities.logging.LoggingFormat": [[30, 3, 1, "", "__init__"]], "rxn.utilities.regex": [[39, 1, 1, "", "alternation"], [40, 1, 1, "", "capturing"], [41, 1, 1, "", "optional"]], "rxn.utilities.scripts": [[43, 0, 0, "-", "stable_shuffle"]], "rxn.utilities.strings": [[45, 1, 1, "", "escape_latex"], [46, 1, 1, "", "remove_postfix"], [47, 1, 1, "", "remove_prefix"]], "rxn.utilities.types": [[49, 2, 1, "", "RxnEnum"]], "rxn.utilities.types.RxnEnum": [[49, 3, 1, "", "__init__"], [49, 3, 1, "", "from_string"], [49, 3, 1, "", "to_string"]]}, "objtypes": {"0": "py:module", "1": "py:function", "2": "py:class", "3": "py:method"}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "function", "Python function"], "2": ["py", "class", "Python class"], "3": ["py", "method", "Python method"]}, "titleterms": {"rxn": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], "util": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], "packag": 0, "system": 0, "requir": 0, "instal": 0, "guid": 0, "api": 1, "attr": [3, 4, 5, 6, 7], "get_class_attribut": 4, "get_vari": 5, "get_variables_and_type_nam": 6, "get_variables_and_typ": 7, "basic": [8, 9], "ident": 9, "cach": [10, 11], "cached_on_disk": 11, "contain": [12, 13, 14, 15, 16], "all_ident": 13, "chunker": 14, "pairwis": 15, "remove_dupl": 16, "databas": [17, 18, 19, 20], "pymongo": [18, 19, 20], "pymongoset": 19, "get_pymongo_set": 20, "file": [21, 22, 23, 24, 25, 26, 27, 28], "count_lin": 22, "dump_list_to_fil": 23, "is_path_creat": 24, "is_path_exists_or_creat": 25, "is_pathname_valid": 26, "iterate_lines_from_fil": 27, "load_list_from_fil": 28, "log": [29, 30, 31, 32, 33, 34, 35, 36, 37], "loggingformat": 30, "log_debug": 31, "log_error": 32, "log_info": 33, "log_warn": 34, "setup_console_and_file_logg": 35, "setup_console_logg": 36, "setup_file_logg": 37, "regex": [38, 39, 40, 41], "altern": 39, "captur": 40, "option": 41, "script": [42, 43], "stable_shuffl": 43, "string": [44, 45, 46, 47], "escape_latex": 45, "remove_postfix": 46, "remove_prefix": 47, "type": [48, 49], "rxnenum": 49, "content": 50, "indic": 50, "tabl": 50}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 6, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.viewcode": 1, "sphinx": 56}})