import codecs
import io
import token as tokens
import tokenize
from pprint import pprint
from functools import partial

tokens.TIEFIGHTER = 0xFF
tokens.tok_name[0xFF] = "TIEFIGHTER"
tokenize.EXACT_TOKEN_TYPES["|=|"] = tokens.TIEFIGHTER

tokenize.PseudoToken = tokenize.Whitespace + tokenize.group(
    r"\|=\|",
    tokenize.PseudoExtras,
    tokenize.Number,
    tokenize.Funny,
    tokenize.ContStr,
    tokenize.Name,
)


def tiefighter(readline):
    source_tokens = list(tokenize.tokenize(readline))
    modified_source_tokens = source_tokens.copy()

    def inc(token, by=1, page=0):
        start = list(token.start)
        end = list(token.end)

        start[page] += by
        end[page] += by

        return token._replace(start=tuple(start), end=tuple(end))

    for index, token in enumerate(source_tokens):
        if token.exact_type == tokens.TIEFIGHTER:
            cxx = index - 1
            
            left = modified_source_tokens.pop(cxx)
            __op = modified_source_tokens.pop(cxx)
            right = modified_source_tokens.pop(cxx)
            
            stmt_start = modified_source_tokens[cxx - 1]
            stmt_end = modified_source_tokens.pop(cxx)
            new_line = modified_source_tokens.pop(cxx)
            
            pattern = io.BytesIO(f"abs({left.string}) == abs({right.string})\n".encode("utf8"))
            absolute_comp = list(tokenize.tokenize(pattern.readline))[1:-2]
                
            stmt_end = inc(stmt_end, absolute_comp[-1].end[1], 1)
            new_line = inc(new_line, stmt_end.end[1] - new_line.start[1], 1)
            modified_source_tokens.insert(cxx, new_line)
            modified_source_tokens.insert(cxx, stmt_end)
            
            for token in reversed(absolute_comp):
                token = inc(token, by = stmt_start.end[0] - 1)
                token = inc(token, by = stmt_start.end[1] + 1, page = 1)
                modified_source_tokens.insert(cxx, token)
            
            
    
    return tokenize.untokenize(modified_source_tokens)

def decode(input, errors="strict", encoding=None):
    if not isinstance(input, bytes):
        input, _ = encoding.encode(input, errors)

    buffer = io.BytesIO(input)
    result = tiefighter(buffer.readline)
    return encoding.decode(result)

class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, input, errors, final):
        return decode(input, errors, encoding=self._encoding)


def search(name):
    if "tiefighter" in name:
        encoding = name.strip("tiefighter").strip("-") or "utf8"
        encoding = codecs.lookup(encoding)
        IncrementalDecoder._encoding = encoding

        tiefighter_codec = codecs.CodecInfo(
            name=name,
            encode=encoding.encode,
            decode=partial(decode, encoding=encoding),
            incrementalencoder=encoding.incrementalencoder,
            incrementaldecoder=IncrementalDecoder,
            streamreader=encoding.streamreader,
            streamwriter=encoding.streamwriter,
        )
        return tiefighter_codec
