/** From https://github.com/errwischt/stacktrace-parser/blob/master/src/stack-trace-parser.js */

/**
 * This parses the different stack traces and puts them into one format
 * This borrows heavily from TraceKit (https://github.com/csnover/TraceKit)
 */

const UNKNOWN_FUNCTION = '<unknown>';
const chromeRe = /^\s*at (.*?) ?\(((?:file|https?|blob|chrome-extension|native|eval|webpack|<anonymous>|\/).*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i;
const chromeEvalRe = /\((\S*)(?::(\d+))(?::(\d+))\)/;
const winjsRe = /^\s*at (?:((?:\[object object\])?.+) )?\(?((?:file|ms-appx|https?|webpack|blob):.*?):(\d+)(?::(\d+))?\)?\s*$/i;
const geckoRe = /^\s*(.*?)(?:\((.*?)\))?(?:^|@)((?:file|https?|blob|chrome|webpack|resource|\[native).*?|[^@]*bundle)(?::(\d+))?(?::(\d+))?\s*$/i;
const geckoEvalRe = /(\S+) line (\d+)(?: > eval line \d+)* > eval/i;

export function parse(stackString) {
  const lines = stackString.split('\n');

  return lines.reduce((stack, line) => {
    const parseResult =
      parseChrome(line) ||
      parseWinjs(line) ||
      parseGecko(line);

    if (parseResult) {
      stack.push(parseResult);
    }

    return stack;
  }, []);
}

export function parseChrome(line) {
  const parts = chromeRe.exec(line);

  if (!parts) {
    return null;
  }

  const isNative = parts[2] && parts[2].indexOf('native') === 0; // start of line
  const isEval = parts[2] && parts[2].indexOf('eval') === 0; // start of line

  const submatch = chromeEvalRe.exec(parts[2]);
  if (isEval && submatch != null) {
    // throw out eval line/column and use top-most line/column number
    parts[2] = submatch[1]; // url
    parts[3] = submatch[2]; // line
    parts[4] = submatch[3]; // column
  }

  return {
    file: !isNative ? parts[2] : null,
    methodName: parts[1] || UNKNOWN_FUNCTION,
    arguments: isNative ? [parts[2]] : [],
    lineNumber: parts[3] ? +parts[3] : null,
    column: parts[4] ? +parts[4] : null,
  };
}

export function parseWinjs(line) {
  const parts = winjsRe.exec(line);

  if (!parts) {
    return null;
  }

  return {
    file: parts[2],
    methodName: parts[1] || UNKNOWN_FUNCTION,
    arguments: [],
    lineNumber: +parts[3],
    column: parts[4] ? +parts[4] : null,
  };
}

export function parseGecko(line) {
  const parts = geckoRe.exec(line);

  if (!parts) {
    return null;
  }

  const isEval = parts[3] && parts[3].indexOf(' > eval') > -1;

  const submatch = geckoEvalRe.exec(parts[3]);
  if (isEval && submatch != null) {
    // throw out eval line/column and use top-most line number
    parts[3] = submatch[1];
    parts[4] = submatch[2];
    parts[5] = null; // no column when eval
  }

  return {
    file: parts[3],
    methodName: parts[1] || UNKNOWN_FUNCTION,
    arguments: parts[2] ? parts[2].split(',') : [],
    lineNumber: parts[4] ? +parts[4] : null,
    column: parts[5] ? +parts[5] : null,
  };
}