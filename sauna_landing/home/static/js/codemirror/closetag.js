(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("codemirror"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["codemirror"], mod);
  else // Plain browser env
    mod(CodeMirror);
})(function(CodeMirror) {
  "use strict";

  CodeMirror.defineExtension("autoCloseTags", function(cm) {
    cm.on("inputRead", function(cm, change) {
      if (change.text[0] === ">" && cm.getMode().name === "htmlmixed") {
        var cursor = cm.getCursor();
        var line = cm.getLine(cursor.line);
        var tag = line.slice(line.lastIndexOf("<") + 1, line.length - 1);

        if (/^[a-zA-Z]+$/.test(tag)) {
          cm.replaceRange("</" + tag + ">", cursor, cursor, "+input");
        }
      }
    });
  });
});
