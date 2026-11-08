extends RefCounted
## Small strict lexical guard around Godot's deliberately permissive JSON parser.
## Reject ambiguous duplicate keys, trailing commas, invalid UTF-8 and deep input.
const MAX_DEPTH = 8
const MAX_TOKENS = 256
var source := ""
var cursor := 0
var tokens := 0
var error := ""
var value: Variant
var number_pattern := RegEx.new()

func parse(bytes: PackedByteArray) -> bool:
    source = bytes.get_string_from_utf8()
    cursor = 0
    tokens = 0
    error = ""
    value = null
    if source.to_utf8_buffer() != bytes:
        return fail("Invalid UTF-8")
    number_pattern.compile("^-?(0|[1-9][0-9]*)(\\.[0-9]+)?([eE][+-]?[0-9]+)?")
    if not scan_value(0):
        return false
    whitespace()
    if cursor != source.length():
        return fail("Unexpected trailing input")
    var parser := JSON.new()
    if parser.parse(source) != OK:
        return fail("Invalid JSON")
    value = parser.data
    if not finite_tree(value):
        return fail("Numbers must be finite")
    return true

func fail(message: String) -> bool:
    error = message
    return false

func whitespace():
    while cursor < source.length() and source[cursor] in [" ", "\t", "\r", "\n"]:
        cursor += 1

func scan_value(depth: int) -> bool:
    whitespace()
    tokens += 1
    if depth > MAX_DEPTH or tokens > MAX_TOKENS:
        return fail("JSON complexity limit exceeded")
    if cursor >= source.length():
        return fail("Missing JSON value")
    var ch := source[cursor]
    if ch == "\"":
        return scan_string()
    if ch == "{" or ch == "[":
        return scan_collection(depth, ch == "{")
    for literal in ["true", "false", "null"]:
        if source.substr(cursor, literal.length()) == literal:
            cursor += literal.length()
            return true
    var found := number_pattern.search(source.substr(cursor))
    if found == null:
        return fail("Invalid JSON value")
    cursor += found.get_string().length()
    return true

func scan_string() -> bool:
    var start := cursor
    cursor += 1
    while cursor < source.length():
        var code := source.unicode_at(cursor)
        if code < 32:
            return fail("Unescaped control in string")
        if source[cursor] == "\"":
            cursor += 1
            var parser := JSON.new()
            if parser.parse(source.substr(start, cursor - start)) != OK:
                return fail("Invalid string escape")
            return true
        if source[cursor] == "\\":
            cursor += 1
            if cursor >= source.length():
                return fail("Incomplete escape")
            if source[cursor] == "u":
                if cursor + 4 >= source.length():
                    return fail("Incomplete unicode escape")
                for i in range(1, 5):
                    if source[cursor + i] not in "0123456789abcdefABCDEF":
                        return fail("Invalid unicode escape")
                cursor += 4
            elif source[cursor] not in ["\"", "\\", "/", "b", "f", "n", "r", "t"]:
                return fail("Invalid string escape")
        cursor += 1
    return fail("Unterminated string")

func scan_collection(depth: int, object: bool) -> bool:
    cursor += 1
    whitespace()
    var closing := "}" if object else "]"
    var keys := {}
    if cursor < source.length() and source[cursor] == closing:
        cursor += 1
        return true
    while cursor < source.length():
        if object:
            if source[cursor] != "\"":
                return fail("Expected object key")
            var start := cursor
            if not scan_string():
                return false
            var key: String = JSON.parse_string(source.substr(start, cursor - start))
            if keys.has(key):
                return fail("Duplicate object key")
            keys[key] = true
            whitespace()
            if cursor >= source.length() or source[cursor] != ":":
                return fail("Expected colon")
            cursor += 1
        if not scan_value(depth + 1):
            return false
        whitespace()
        if cursor < source.length() and source[cursor] == closing:
            cursor += 1
            return true
        if cursor >= source.length() or source[cursor] != ",":
            return fail("Expected comma or closing delimiter")
        cursor += 1
        whitespace()
        # Next iteration requires a value/key, so trailing commas cannot pass.
    return fail("Unclosed collection")

func finite_tree(item: Variant) -> bool:
    if item is float:
        return is_finite(item)
    if item is Array:
        for child in item:
            if not finite_tree(child):
                return false
    if item is Dictionary:
        for child in item.values():
            if not finite_tree(child):
                return false
    return true
