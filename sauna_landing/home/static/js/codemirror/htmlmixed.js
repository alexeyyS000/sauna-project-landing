(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("codemirror"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["codemirror"], mod);
  else // Plain browser env
    mod(CodeMirror);
})(function(CodeMirror) {
  "use strict";

  CodeMirror.defineMode("htmlmixed", function(config, parserConfig) {
    var htmlMode = CodeMirror.getMode(config, {name: "xml", htmlMode: true});
    var cssMode = CodeMirror.getMode(config, "css");
    var jsMode = CodeMirror.getMode(config, "javascript");

    function dispatch(stream, state) {
      if (state.curMode == "html") return htmlMode.token(stream, state.htmlState);
      if (state.curMode == "css") return cssMode.token(stream, state.cssState);
      if (state.curMode == "javascript") return jsMode.token(stream, state.jsState);
    }

    return {
      startState: function() {
        return {curMode: "html", htmlState: CodeMirror.startState(htmlMode)};
      },
      token: dispatch,
    };
  });
});
