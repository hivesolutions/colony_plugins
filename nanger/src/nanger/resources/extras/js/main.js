// Hive Colony Framework
// Copyright (c) 2008-2012 Hive Solutions Lda.
//
// This file is part of Hive Colony Framework.
//
// Hive Colony Framework is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Hive Colony Framework is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2012 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

(function($) {
    jQuery.fn.uxconsole = function(query, callback, options) {
        // the default values for the data query
        var defaults = {};

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

jQuery(document).ready(function() {

    // the offset in pixels of the autocomplete
    // window relative to the console line
    var AUTOCOMPLETE_OFFSET = 2;

    // the basic commands of the console to be
    // executed at the client side
    var COMMANDS = ["clear", "fullscreen", "window"];

    // registers for the click event in the console to
    // propagate the focus event to the text area
    jQuery(".console").click(function() {
                var element = jQuery(this);
                var text = jQuery(".text", element);
                var autocomplete = jQuery(".autocomplete", element);
                text.focus();
                autocomplete.hide();
            });

    jQuery(".console").bind("dragenter", function(event) {
                // retrieves the current element and
                // adds the drag class to it (styling
                // of the element structure)
                var element = jQuery(this);
                element.addClass("drag");
            });

    jQuery(".console").bind("dragover", function(event) {
                // retrieves the current element and
                // adds the drag class to it (styling
                // of the element structure)
                var element = jQuery(this);
                element.addClass("drag");
            });

    jQuery(".console").bind("dragleave", function(event) {
                // retrieves the current element and
                // removes the drag class to it (styling
                // of the element structure)
                var element = jQuery(this);
                element.removeClass("drag");
            });

    jQuery(".console").bind("drop", function(event) {
                // retrieves the current element and
                // removes the drag class to it (styling
                // of the element structure)
                var element = jQuery(this);
                element.removeClass("drag");

                // prevents the default event (avoids browser showing
                // the file in raw mode)
                event.preventDefault();

                // retrieves the first file and create a new file
                // reader object to handle the loading of the file
                var dataTransfer = event.originalEvent.dataTransfer;
                var file = dataTransfer.files[0];
                reader = new FileReader();
                reader.onload = function(event) {
                    // retrieves the provided text value from
                    // the event to be processed by the console
                    // then replaces the windows style newlines
                    // with the basic unix styled ones
                    var value = event.target.result;
                    value = value.replace(/\r\n/g, "\n");

                    // retrieves the current console commands and appends
                    // the complete file value into it (for execution) then
                    // puts the commands value back into the console
                    var _commands = jQuery(".console").data("commands") || [];
                    _commands.push(value);
                    jQuery(".console").data("commands", _commands);

                    // runs the process command on the console and waits for the
                    // response to print the newline with the information regarding
                    // the execution of the file
                    process(true, function(result) {
                                newline("load " + file.name, "", result);
                            });
                };
                reader.readAsText(file);

                // stops the event propagation to avoid any possible
                // problem with upper handlers
                event.stopPropagation();
                event.stopImmediatePropagation();
            });

    jQuery(".console .text").keydown(function(event) {
        // retrieves the current element
        var element = jQuery(this);

        // retrieves the text currently in used for the context
        // of the console (current command)
        var value = jQuery(".console").data("text") || "";

        // retrieves the key value
        var keyValue = event.keyCode ? event.keyCode : event.charCode
                ? event.charCode
                : event.which;

        // sets the default value for the canceling operation
        // (no default behavior) as true (most of the times)
        var cancel = true;

        if (event.ctrlKey) {
            switch (keyValue) {
                case 32 :
                    autocomplete(true);
                    break;

                default :
                    break;
            }
        }

        switch (keyValue) {
            case 8 :
                // prevents the default behavior for the backspace
                // key because it would focus the window on the text area
                event.preventDefault();

                var cursor = jQuery(".console").data("cursor");
                if (cursor == value.length - 1) {
                    break;
                }

                var first = value.slice(0, value.length - cursor - 2);
                var second = value.slice(value.length - cursor - 1,
                        value.length);
                var value = first + second;
                jQuery(".console").data("text", value)

                refresh();
                break;

            case 9 :
                // prevents the default behavior for the tab key
                // to avoid the focus from jumping to a different element
                event.preventDefault();

                // checks if the autocomplete window is visible and in case
                // it is flushes the currently selected autocomplete option
                // to the console (autocomplete selection)
                var isVisible = jQuery(".console .autocomplete").is(":visible");
                if (isVisible) {
                    flushAutocomplete();
                    break;
                }

                var cursor = jQuery(".console").data("cursor");
                var first = value.slice(0, value.length - cursor - 1);
                var second = value.slice(value.length - cursor - 1,
                        value.length);
                var value = first + "    " + second;
                jQuery(".console").data("text", value)

                refresh();
                break;

            case 27 :
                jQuery(".console .autocomplete").hide();
                break;

            case 32 :
                jQuery(".console .autocomplete").hide();
                cancel = false;
                break;

            case 33 :
                var isVisible = jQuery(".console .autocomplete").is(":visible");

                if (isVisible) {
                    var selected = jQuery(".console .autocomplete ul > li.selected");
                    selected.removeClass("selected");
                    var target = jQuery(".console .autocomplete ul > li:first-child");
                    target.addClass("selected");
                    ensureVisible(target, jQuery(".console .autocomplete"));
                    selectAutocomplete();

                    // prevernts the default behavior (avoids the top level window
                    // from moving, expected behavior)
                    event.preventDefault();

                    // breaks the switch
                    break;
                }

                break;

            case 34 :
                var isVisible = jQuery(".console .autocomplete").is(":visible");

                if (isVisible) {
                    var selected = jQuery(".console .autocomplete ul > li.selected");
                    selected.removeClass("selected");
                    var target = jQuery(".console .autocomplete ul > li:last-child");
                    target.addClass("selected");
                    ensureVisible(target, jQuery(".console .autocomplete"));
                    selectAutocomplete();

                    // prevernts the default behavior (avoids the top level window
                    // from moving, expected behavior)
                    event.preventDefault();

                    // breaks the switch
                    break;
                }

                break;

            case 35 :
                jQuery(".console").data("cursor", -1);
                refresh();
                break;

            case 36 :
                jQuery(".console").data("cursor", value.length - 1);
                refresh();
                break;

            case 37 :
                var cursor = jQuery(".console").data("cursor");
                if (cursor == value.length - 1) {
                    break;
                }
                cursor++;
                jQuery(".console").data("cursor", cursor);

                refresh();

                break;

            case 38 :
                var isVisible = jQuery(".console .autocomplete").is(":visible");

                if (isVisible) {
                    var selected = jQuery(".console .autocomplete ul > li.selected");
                    if (selected.is(":first-child")) {
                        return;
                    }
                    selected.removeClass("selected");
                    var selectedIndex = selected.index();
                    var target = jQuery(".console .autocomplete ul > li:nth-child("
                            + (selectedIndex) + ")");

                    target.addClass("selected");
                    ensureVisible(target, jQuery(".console .autocomplete"));
                    selectAutocomplete();

                    // breaks the switch
                    break;
                }

                var history = jQuery(".console").data("history") || [];
                var historyIndex = jQuery(".console").data("history_index")
                        || 0;

                var value = history[history.length - historyIndex - 1];
                if (historyIndex != history.length - 1) {
                    historyIndex++;
                }

                jQuery(".console").data("text", value)
                jQuery(".console").data("history_index", historyIndex)

                refresh();
                break;

            case 39 :
                var cursor = jQuery(".console").data("cursor");
                if (cursor == -1) {
                    break;
                }
                cursor--;
                jQuery(".console").data("cursor", cursor);

                refresh();
                break;

            case 40 :
                var isVisible = jQuery(".console .autocomplete").is(":visible");

                if (isVisible) {
                    var selected = jQuery(".console .autocomplete ul > li.selected");
                    if (selected.is(":last-child")) {
                        return;
                    }
                    selected.removeClass("selected");
                    var selectedIndex = selected.index();
                    var target = jQuery(".console .autocomplete ul > li:nth-child("
                            + (selectedIndex + 2) + ")");
                    target.addClass("selected");
                    ensureVisible(target, jQuery(".console .autocomplete"));
                    selectAutocomplete();

                    // breaks the switch
                    break;
                }

                var history = jQuery(".console").data("history") || [];
                var historyIndex = jQuery(".console").data("history_index")
                        || 0;

                var value = history[history.length - historyIndex];
                if (historyIndex != 0) {
                    historyIndex--;
                }

                jQuery(".console").data("text", value)
                jQuery(".console").data("history_index", historyIndex)

                refresh();
                break;

            case 46 :
                // prevents the default behavior for the delete
                // key because it would focus the window on the text area
                event.preventDefault();

                var cursor = jQuery(".console").data("cursor");
                if (cursor == -1) {
                    break;
                }

                var first = value.slice(0, value.length - cursor - 1);
                var second = value.slice(value.length - cursor, value.length);
                var value = first + second;

                jQuery(".console").data("text", value)
                jQuery(".console").data("cursor", cursor - 1)

                refresh();
                break;

            default :
                cancel = false;
                break;
        }

        // updates the cancel data attribute in the
        // console to provide information to the hadling
        // of the key pressing in the next event
        jQuery(".console").data("cancel", cancel)

        // stops the event propagation this should be able
        // to avoid possible problems with double handling
        event.stopPropagation();
        event.stopImmediatePropagation();
    });

    jQuery(".console .text").bind("paste", function(event) {
        // retrieves the element
        var element = jQuery(this);

        // sets a timeout so that the complete paste data
        // is set in the text area (deferred event)
        setTimeout(function() {
                    // retrieves the current value of the element and clears
                    // the contents of the text element to avoid  any duplicate
                    // paste operation (unwanted behavior)
                    var character = element.val();
                    element.val("");

                    // retrieves the current console text to be able to be used
                    // as teh base data for the paste operation
                    var text = jQuery(".console").data("text") || "";

                    // adds the new character into the text buffer
                    // by slicing the value around the current position,
                    // then joins the value back with the character
                    var cursor = jQuery(".console").data("cursor");
                    var first = text.slice(0, text.length - cursor - 1);
                    var second = text.slice(text.length - cursor - 1,
                            text.length);
                    var value = first + character + second;

                    // splits the various lines of the value arround
                    // the newline character to retrieve the commands
                    var commands = value.split("\n");

                    // in case there are multiple commands the multiline
                    // mode is activated and execution of the commands
                    // is ensured immediately
                    if (commands.length > 1) {
                        var _commands = jQuery(".console").data("commands")
                                || [];
                        for (var index = 0; index < commands.length; index++) {
                            _commands.push(commands[index]);
                        }
                        jQuery(".console").data("commands", _commands);
                        process();
                    }

                    // updates the text value of the console and refreshes
                    // the visual part of it
                    var value = commands[commands.length - 1];
                    jQuery(".console").data("text", value);
                    refresh();
                }, 0);
    });

    jQuery(".console .text").keypress(function(event) {
        // retrieves the element
        var element = jQuery(this);

        // retrieves the key value
        var keyValue = event.keyCode ? event.keyCode : event.charCode
                ? event.charCode
                : event.which;

        var keyCode = event.keyCode || event.which;
        var character = String.fromCharCode(keyCode);
        var text = jQuery(".console").data("text") || "";
        var cancel = jQuery(".console").data("cancel") || false;

        // in case the cancel flag is set the key press must
        // be ignored and the call returned immediately
        if (cancel) {
            return false;
        }

        if ((event.ctrlKey || event.metaKey)
                && String.fromCharCode(keyCode).toLowerCase() == "v") {
            return true;
        }

        if ((event.ctrlKey || event.metaKey)
                && String.fromCharCode(keyCode).toLowerCase() == "r") {
            return true;
        }

        // switches over the key value
        switch (keyValue) {
            case 13 :
                // checks if the autocomplete window is visible and in case
                // it is flushes the currently selected autocomplete option
                // to the console (autocomplete selection)
                var isVisible = jQuery(".console .autocomplete").is(":visible");
                if (isVisible) {
                    flushAutocomplete();
                    break;
                }

                var value = jQuery(".console").data("text") || "";

                switch (value) {
                    case "clear" :
                        // clears the current console display removing the various
                        // information contained in it
                        clear(true);
                        event.preventDefault();

                        // breaks the switch
                        break;

                    case "fullscreen" :
                        // puts the current console window into the fullscreen mode
                        // this action should change the current body and window status
                        // so it should be used carefully to avoid side effects
                        fullscreen();
                        clear(false);
                        event.preventDefault();

                        // breaks the switch
                        break;

                    case "window" :
                        // puts the current console window into the window mode
                        // this action should change the current body and window status
                        // so it should be used carefully to avoid side effects
                        _window();
                        clear(false);
                        event.preventDefault();

                        // breaks the switch
                        break;

                    default :
                        // runs the process of the "remote" command this should trigger
                        // the execution of the server side execution
                        var commands = jQuery(".console").data("commands")
                                || [];
                        commands.push(value);
                        jQuery(".console").data("commands", commands)
                        process();

                        // breaks the switch
                        break;
                }

                // breaks the switch
                break;

            default :
                // adds the new character into the text buffer
                // by slicing the value around the current position,
                // then joins the value back with the character
                var cursor = jQuery(".console").data("cursor");
                var first = text.slice(0, text.length - cursor - 1);
                var second = text.slice(text.length - cursor - 1, text.length);
                var value = first + character + second;

                // updates the text value of the console and refreshes
                // the visual part of it, note that the autocomplete
                // is only run in case the character is not a space
                jQuery(".console").data("text", value);
                refresh();
                character != " " && autocomplete(true);

                // breaks the switch
                break;
        }

        // stops the event propagation and prevents the default
        // behavior (no printing in the text area)
        event.stopPropagation();
        event.stopImmediatePropagation();
        event.preventDefault();
    });

    jQuery(".console .text").focus(function() {
                jQuery(".console").addClass("focus");
            });

    jQuery(".console .text").blur(function() {
                jQuery(".console").removeClass("focus");
                jQuery(".console .autocomplete").hide();
            });

    jQuery(window).scroll(function() {
                jQuery(".console .autocomplete").hide();
            });

    var escapeHtml = function(value) {
        return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g,
                "&gt;").replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;");
    };

    var splitValue = function(value, escape, cursor) {
        // in case there is no value defined there is no need
        // to split because there is no definition of it
        if (value == null) {
            return value;
        }

        var length = value.length;

        var slices = [];

        for (var index = 0; index < length; index += 1) {
            var slice = value.slice(index, index + 1);
            slices.push(slice);
        }

        var word = "";
        var slice = "";

        var sliceLength = slices.length;
        for (var index = 0; index < sliceLength; index++) {
            slice = escape ? escapeHtml(slices[index]) : slices[index];
            slice = length - cursor - 1 == index ? "<span class=\"cursor\">"
                    + slice + "</span>" : slice;
            word += slice + "<wbr></wbr>";
        }

        if (cursor == -1) {
            word += "<span class=\"cursor\">&nbsp;</span>"
        }

        return word;
    };

    var refresh = function() {
        var value = jQuery(".console").data("text") || "";
        var scrollHeight = jQuery(".console")[0].scrollHeight;
        var cursor = jQuery(".console").data("cursor");
        word = splitValue(value, true, cursor);
        jQuery(".console .line").html(word);
        jQuery(".console").scrollTop(scrollHeight);
        autocomplete(false);
    };

    /**
     * Clears the contents of the console, this should include the current line,
     * the previous lines and the text field. At the end of the execution the
     * console is refreshed.
     *
     * @param {Boolean}
     *            complete If the clearing of the consol should be complete
     *            (previous elements removed) or if only the current line is to
     *            be removed.
     */
    var clear = function(complete) {
        jQuery(".console").data("text", "");
        jQuery(".console").data("cursor", -1);
        jQuery(".console .text").val("");
        jQuery(".console .line").empty();
        complete && jQuery(".console .previous").empty();
        refresh();
    };

    var joinResult = function(token, result) {
        for (var index = 0; index < COMMANDS.length; index++) {
            var current = COMMANDS[index];
            var offset = current.indexOf(token);
            if (offset != 0) {
                continue;
            }
            result.push([current, "command"]);
        }
    };

    var autocomplete = function(force) {
        // checks if the autocomplete window is currently visible
        // in case it's not and the force flag is not set avoid
        // the processing of the autocomplete elements
        var isVisible = jQuery(".console .autocomplete").is(":visible");
        if (!force && !isVisible) {
            return;
        }

        // retrieves the token structure and uses it to retrieve
        // the currently selected token (selected word)
        var tokenStructure = getToken();
        var token = tokenStructure[0];

        // runs the remove query to retrieve the various autcomplete
        // results (this query is meant to be fast 100ms maximum)
        jQuery.ajax({
            url : "console/autocomplete",
            data : {
                command : token,
                instance : jQuery(".console").data("instance")
            },
            success : function(data) {
                // unpacks the resulting json data into the result
                // and the instance part, so that they may be used
                // in the processing of the results
                var result = data["result"];
                var offset = data["offset"];
                var instance = data["instance"];

                // joins the received result set with the local commands
                // set so that the local commands may also appear in the
                // autocomplete list
                joinResult(token, result);

                // retrieves the autocomplete list item and clears
                // all of its items (component reset)
                var list = jQuery(".console .autocomplete ul");
                list.empty();

                // iterates over all the values to be inserted into
                // the autocomplete options list
                for (var index = 0; index < result.length; index++) {
                    // retrieves the current value in iteration to
                    // add it to the options list, then unpacks it into
                    // name and the type part of the "tuple"
                    var value = result[index];
                    var name = value[0];
                    var type = value[1];
                    var options = value[2];

                    // retrieves the highlight and the remainder part
                    // of the name using the command length as base
                    var highlight = name.slice(0, token.length - offset);
                    var remainder = name.slice(token.length - offset);

                    // creates the new item with both the highlight and
                    // the remaind part and adds it to the list of options
                    var item = jQuery("<li class=\"" + type
                            + "\"><span class=\"high\">" + highlight
                            + "</span>" + remainder + "</li>");
                    list.append(item);
                    item.data("options", options);
                }

                // sets the instance (identifier) value in the console
                // for latter usage of the value
                jQuery(".console").data("instance", instance);

                // sets the first child of the autocomplete list as the
                // currently selected child element
                jQuery(":first-child", list).addClass("selected");

                // forces the display of the autocomplete in case there
                // are results available otherwise hides the autocomplete
                // list (no need to display the result)
                result.length
                        ? jQuery(".console .autocomplete").show()
                        : jQuery(".console .autocomplete").hide();

                // in case there are no results to be displayed no additional
                // processing should occur (not significant) returns immediately
                if (!result.length) {
                    return;
                }

                // calculates the offset to the top of the screen based
                // on the current line position and offset to the top,
                // then scrolls the autocomplete scrolling back the top
                // (considered to be the original position)
                var offsetTop = jQuery(".console .line").offset().top
                        + jQuery(".console .line").outerHeight();
                jQuery(".console .autocomplete").css("top", offsetTop + "px");
                jQuery(".console .autocomplete").scrollTop(0);

                // retrieves the current token structure and uses it to
                // retrieve the start index of the token (for autocomplete
                // box positioning)
                var tokenStructure = getToken();
                var startIndex = tokenStructure[1];

                // retrieves the size of the font currently being used for the
                // text and converts it into an integer value then uses it to
                // calculate the offset to be used in the autocomplete
                var fontSize = jQuery(".console .text").css("font-size");
                fontSize = parseInt(fontSize);
                jQuery(".console .autocomplete").css("margin-left",
                        (startIndex * fontSize + 24) + "px");

                // updates the autocomplete window margin so that the window is
                // displayed bellow the current line and then checks if it's
                // visible, in case it's not it must be placed above the line
                jQuery(".console .autocomplete").css("margin-top",
                        AUTOCOMPLETE_OFFSET + "px");
                var isVisible = checkVisible(jQuery(".console .autocomplete"),
                        jQuery(window));

                // calculates the margin top position to be used to place
                // the autocomplete window above the current line and then
                // in case the window is not visible places in such
                // place (notice the minus sign in the margin)
                var aboveMargin = jQuery(".console .autocomplete").outerHeight()
                        + jQuery(".console .line").outerHeight()
                        + AUTOCOMPLETE_OFFSET;
                if (isVisible) {
                    jQuery(".console .autocomplete").removeClass("above");
                } else {
                    jQuery(".console .autocomplete").addClass("above");
                    jQuery(".console .autocomplete").css("margin-top",
                            (aboveMargin * -1) + "px");
                }

                // selects the autocomplete item, this should trigger the
                // placement of the tooltip window at the appropriate side
                selectAutocomplete();
            }
        });

    };

    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, "");
    }
    String.prototype.ltrim = function() {
        return this.replace(/^\s+/, "");
    }
    String.prototype.rtrim = function() {
        return this.replace(/\s+$/, "");
    }

    /**
     * Processes one command from the current console queue in case there's at
     * least one command there. The order of execution is first in first out
     * (fifo) and one command is executed then only after the return from the
     * server side is completed the next command is executed.
     *
     * @param {Boolean}
     *            silent Flag that controls if the processing of the command
     *            should generate console output.
     * @param {Function}
     *            callback The callback function to be called at the end of each
     *            command processed durring this process call.
     */
    var process = function(silent, callback) {
        // tries to retrieve the command queue and checks if it's empty
        // in such case must return immediately
        var commands = jQuery(".console").data("commands") || [];
        if (commands.length == 0) {
            return;
        }

        // retrieves the currently pending data to be flushed to the
        // server side (important for multiple line commands)
        var _pending = jQuery(".console").data("pending") || "";

        // retrieves the current command and then retrives the remaining
        // parts of the commands queue
        var value = commands[0];
        var next = commands[1] || "";
        var command = value.rtrim();
        commands = commands.slice(1);
        jQuery(".console").data("commands", commands);

        // in case there is pendind data to be sent and the command is not
        // empty (end of pending operation) must delay command processing
        if (_pending && command) {
            newline(value, next, "", _pending + "\n" + value, true);
            process(silent, callback);
            return;
        }

        // updates the command value by prepending the pending part
        // of the command to the command itself (this will allow for
        // complete execution of the previous lines)
        command = _pending + "\n" + command;

        jQuery.ajax({
                    url : "console/execute",
                    data : {
                        command : command,
                        instance : jQuery(".console").data("instance")
                    },
                    success : function(data) {
                        // unpacks the resulting json data into the result
                        // and the instance part, so that they may be used
                        // in the processing and printing of the result
                        var result = data["result"];
                        var pending = data["pending"];
                        var instance = data["instance"];

                        // sets the instance (identifier) value in the console
                        // for latter usage of the value only in case the instance
                        // value is defined (otherwise leave as it is)
                        instance
                                && jQuery(".console").data("instance", instance);

                        // in case the current processing mode is not silent
                        // must create a newline with the current context (verbose)
                        !silent
                                && newline(value, next, result, command,
                                        pending);

                        // in case the callback is defined calls it with
                        // the resulting values from the client side
                        callback && callback(result, pending, instance);

                        // runs the process command again to continue the processing
                        // of the current queue
                        process(silent, callback);
                    }
                });
    };

    var flushAutocomplete = function() {
        // retrieves the currently selected autocomplete element and
        // then retrieves its value and its options map (in case one
        // is available)
        var selected = jQuery(".console .autocomplete ul > li.selected");
        var text = selected.text();
        var options = selected.data("options") || {};

        // retrieves the current's console text and then retrieves
        // the token structure for the currrently selected text
        var _text = jQuery(".console").data("text") || "";
        var tokenStructure = getToken();

        // unpacks the token structure into the various components
        // of it, the token and the start and end indexes
        var token = tokenStructure[0];
        var startIndex = tokenStructure[1];
        var endIndex = tokenStructure[2];

        var tokenElements = token.split(".");
        var tokenElements = tokenElements.slice(0, tokenElements.length - 1);
        tokenElements.push(text);
        token = tokenElements.join(".")

        var start = _text.slice(0, startIndex);
        var end = _text.slice(endIndex);

        // in case there is an extra string value to be added to the token
        // adds it (this will appear at the front of the value)
        token += options["extra"] || "";

        call = false;

        // in case the currently selected item is a method or a function
        // extra care must be taken to provide the calling part
        if (selected.hasClass("method") || selected.hasClass("function")) {
            // appends the calling part of the line to the token
            // to provide calling shortcut
            token += "()";
            call = true;
        }

        // creates the final text value to be set in the line using
        // the start part the token and the (final) end part
        text = start + token + end;

        // calculates the new cursor position based on the partial
        // token values and the start string length and takes into
        // account the possible offset for the call situations
        var cursor = text.length
                - (start.length + token.length + (call ? 0 : 1))

        jQuery(".console").data("text", text);
        jQuery(".console").data("cursor", cursor);
        jQuery(".console .autocomplete").hide();
        refresh();
    };

    var newline = function(value, next, result, command, pending) {
        // recalculates the pending command value using the
        // pending flag as the guide for this operation and
        // then sets the new pending string in the console
        _pending = pending ? command : "";
        jQuery(".console").data("pending", _pending);

        // retrieves the value of the currently displayed prompt
        // as the previous prompt and "calculates" the value for
        // the next primpt string
        var previousPrompt = jQuery(".console .current .prompt").html();
        var prompt = pending ? ". " : "# ";

        // trims the resulting value to avoid any possible extra
        // newline values (typical for some interpreters)
        result = result.rtrim();

        // resets the element value (virtual value) and clear the
        // console line (to the original value) and updates the
        // prompt value with the "calculated" one
        jQuery(".console").data("text", next);
        jQuery(".console .line").html("<span class=\"cursor\">&nbsp;</span>");
        jQuery(".console .current .prompt").html(prompt);

        // resets the cursor position to the top right most position
        // of the current line in printing
        jQuery(".console").data("cursor", -1);

        // creates a new previous line and adds it to the previous container
        // this line will contain the values of the executed command
        jQuery(".console .previous").append("<div><span class=\"prompt\">"
                + previousPrompt + "</span><span>" + splitValue(value, true)
                + "</span></div>");

        // splits the result value (into the appropriate components) and
        // also adds it to the previous action container, then scrolls
        // the current console area to the lower part
        var line = splitValue(result, true);
        jQuery(".console .previous").append("<div>" + line + "</div>");
        jQuery(".console").scrollTop(jQuery(".console")[0].scrollHeight);

        // retrieves the sequence object that contains the various
        // command strings that compose the history of the console
        var history = jQuery(".console").data("history") || [];

        // checks if the current value to be inserted
        // into the history is not equal to the one already
        // present at the top of the history only in that
        // situation shall the value be inserted in history
        if (value != history[history.length - 1]) {
            history.push(value);
        }
        jQuery(".console").data("history", history);
        jQuery(".console").data("history_index", 0);

        // hides the autocomplete window, no need to display
        // it durring the initial part of the line processing
        jQuery(".console .autocomplete").hide();
    };

    var selectAutocomplete = function() {
        // retrieves the currently selected autocomplete item to
        // be used for the selection process
        var selected = jQuery(".console .autocomplete ul > li.selected");

        // retrieves the various options from the selected item defaulting
        // to the basic values in case of non existence
        var options = selected.data("options") || {};
        var doc = options["doc"] || "";
        var params = options["params"] || [];
        var _return = options["return"] || null;
        doc = doc.trim();

        // hides the tooltip window (default behavior) and in case there
        // is documentation string available returns immediately (not tooltip
        // will be shown for this case)
        jQuery(".console .autocomplete .tooltip").hide();
        if (!doc) {
            return;
        }

        // shows the tooltip window back to the screen to ensure visibility
        // of the it (documentation exists)
        jQuery(".console .autocomplete .tooltip").show();

        jQuery(".console .autocomplete .tooltip").css("margin-left",
                jQuery(".console .autocomplete").outerWidth() + 4);

        var _doc = jQuery(".console .autocomplete .tooltip").data("doc") || "";
        if (doc != _doc) {
            jQuery(".console .autocomplete .tooltip .doc").html(splitValue(doc,
                    true));
        }
        jQuery(".console .autocomplete .tooltip").data("doc", doc);

        var _params = jQuery(".console .autocomplete .tooltip").data("params")
                || [];
        if (params != _params) {
            jQuery(".console .autocomplete .tooltip .params").empty();

            for (var index = 0; index < params.length; index++) {
                var param = params[index];
                jQuery(".console .autocomplete .tooltip .params").append("<div class=\"param\"><span class=\"name\">"
                        + param[0]
                        + "</span>&nbsp;<span class=\"type\">("
                        + param[1]
                        + ")</span><br />&nbsp;&nbsp;<span class=\"description\">"
                        + splitValue(param[2], true) + "</span></div>")
            }
        }
        jQuery(".console .autocomplete .tooltip").data("params", params);

        var __return = jQuery(".console .autocomplete .tooltip").data("return")
                || [];
        if (_return != __return) {
            jQuery(".console .autocomplete .tooltip .return").empty();

            _return
                    && jQuery(".console .autocomplete .tooltip .return").append("<div class=\"param\"><span class=\"name\">"
                            + _return[0]
                            + "</span>&nbsp;<span class=\"type\">("
                            + _return[1]
                            + ")</span><br />&nbsp;&nbsp;<span class=\"description\">"
                            + splitValue(_return[2], true) + "</span></div>")
        }
        jQuery(".console .autocomplete .tooltip").data("return", _return);

        var isAbove = jQuery(".console .autocomplete").hasClass("above");

        var autocompleteHeight = jQuery(".console .autocomplete").outerHeight();
        var tooltipHeight = jQuery(".console .autocomplete .tooltip").outerHeight();
        var borderBottom = parseInt(jQuery(".console .autocomplete").css("border-bottom"));
        var delta = autocompleteHeight - tooltipHeight - borderBottom;

        delta = delta < 0 ? delta : null;
        delta = isAbove ? delta : null;

        jQuery(".console .autocomplete .tooltip").css("margin-top", delta);

        var isVisible = checkVisible(jQuery(".console .autocomplete .tooltip"),
                jQuery(window));

        var aboveMargin = jQuery(".console .autocomplete").outerHeight()
                + jQuery(".console .line").outerHeight() + AUTOCOMPLETE_OFFSET;

        if (!isVisible) {
            isAbove = true

            jQuery(".console .autocomplete").addClass("above");
            jQuery(".console .autocomplete").css("margin-top",
                    (aboveMargin * -1) + "px");

            var delta = autocompleteHeight - tooltipHeight - marginBottom;

            delta = delta < 0 ? delta : null;
            delta = isAbove ? delta : null;

            jQuery(".console .autocomplete .tooltip").css("margin-top", delta);

            var isVisible = checkVisible(
                    jQuery(".console .autocomplete .tooltip"), jQuery(window));
        }
    };

    var getToken = function() {
        // retrieves the current console command in execution
        // to retrieve the associated autocomplete value
        var command = jQuery(".console").data("text") || "";

        // retrieves the current cursor position and uses it to
        // try to find the index of the token to be used in the retrieval
        var cursor = jQuery(".console").data("cursor") || -1;
        for (var index = command.length - cursor - 2; index >= 0; index--) {
            if (command[index] != " ") {
                continue;
            }
            break;
        }

        index++;

        // saves the current index position as the start index position
        // for the command (the reference to the first letter)
        var startIndex = index;

        for (var index = startIndex; index < command.length; index++) {
            if (command[index] != " ") {
                continue;
            }
            break;
        }

        var endIndex = index;
        var token = command.slice(startIndex, endIndex);

        return [token, startIndex, endIndex];
    };

    var maximize = function() {
        // retrieves the window
        var _window = jQuery(window);

        jQuery("html").css("overflow-y", "hidden");

        jQuery("body").css("margin", "0px 0px 0px 0px");
        jQuery("body").css("padding", "0px 0px 0px 0px");

        var windowHeight = _window.height();
        var windowWidth = _window.width();

        jQuery(".console").css("margin", "0px 0px 0px 0px");
        jQuery(".console").css("position", "absolute");
        jQuery(".console").css("top", "0px");
        jQuery(".console").css("left", "0px");
        jQuery(".console").height(windowHeight - 4);
        jQuery(".console").width(windowWidth - 8);

        var scrollHeight = jQuery(".console")[0].scrollHeight;
        jQuery(".console").scrollTop(scrollHeight);
    };

    var minimize = function() {
        jQuery("html").css("overflow-y", null);

        jQuery("body").css("margin", null);
        jQuery("body").css("padding", null);

        jQuery(".console").css("margin", null);
        jQuery(".console").css("position", null);
        jQuery(".console").css("top", null);
        jQuery(".console").css("left", null);
        jQuery(".console").css("height", null);
        jQuery(".console").css("width", null);

        var scrollHeight = jQuery(".console")[0].scrollHeight;
        jQuery(".console").scrollTop(scrollHeight);
    };

    var fullscreen = function() {
        // adds the fullscrren class to the console element
        // so that the specific style are applied to it
        jQuery(".console").addClass("fullscreen");

        // creates the function that will be used to update the
        // size of the console on a resize of the parent
        var resize = function(event) {
            // hides the autocomplete window so that no visual
            // disturbances are displayed as a result of the new size
            jQuery(".console .autocomplete").hide();

            // refreshes the current console window to fill the
            // newly available space
            maximize();
        };

        // retrieves the window and registers the resize in
        // the window to update the console size
        var _window = jQuery(window);
        _window.resize(resize);

        // saves the resize function in the console to be latter
        // used in the unbind process of the window resize event
        jQuery(".console").data("resize", resize);

        // maximizes the current window to fill the currently
        // available space (in body)
        maximize();
    };

    var _window = function() {
        // removes the fullscreen class from the console element
        // to avoid unexpected visuals in the console
        jQuery(".console").removeClass("fullscreen");

        // retrieves the currently used resize function from the
        // console to be used in the unset of the event handler
        var resize = jQuery(".console").data("resize", resize);

        // retrieves the window and uses it to unbind the resize
        // event (currently set) from it
        var _window = jQuery(window);
        _window.unbind("resize", resize)

        // minimizes the console removing all the custom style
        // applied to the current environment
        minimize();
    };

    var checkVisible = function(element, parent) {
        // retrieves the various measures of the parent for the
        // partial calculus of the visibility status of the element
        var parentHeight = parent.height();
        var parentTop = parent.scrollTop();
        var parentBottom = parentTop + parentHeight;

        // retrieves the measures for the element in order to be able
        // to calculate its own visibility status
        var elementHeight = element.outerHeight();
        var elementTop = element.offset().top;
        var elementBottom = elementTop + elementHeight;

        // checks if the element is visible in the current context
        // and returns that result to the caller method
        var isVisible = elementBottom <= parentBottom
                && elementTop >= parentTop;
        return isVisible;
    };

    var ensureVisible = function(element, parent) {
        // retrieves the various measures of the parent for the
        // partial calculus of the visibility status of the element
        var parentHeight = parent.height();
        var parentTop = parent.scrollTop();
        var parentBottom = parentTop + parentHeight;

        // retrieves the measures for the element in order to be able
        // to calculate its own visibility status
        var elementHeight = element.outerHeight();
        var elementTop = element.offset().top - element.parent().offset().top;
        var elementBottom = elementTop + elementHeight;

        // checks if the element is visible in the current context
        // and in case it's retunrs immediately no need to change the
        // parent element to ensure visibility
        var isVisible = elementBottom <= parentBottom
                && elementTop >= parentTop;
        if (isVisible) {
            return;
        }

        // calculates the signal using the relative position of the
        // element to determine if it should be negative or positive
        var signal = elementTop > parentTop ? 1 : -1;

        // calculates the (new) current scroll position base on the
        // signal (relative position) of the element in relation with
        // the current scroll position
        var current = signal == 1
                ? elementTop - (parentHeight - elementHeight)
                : elementTop;
        parent.scrollTop(current);
    };

    var init = function() {
        // hides the current line, no input will be possible durring
        // the initial loading of the console
        jQuery(".console .current").hide();

        // runs the remove query to retrieve the various autcomplete
        // results (this query is meant to be fast 100ms maximum)
        jQuery.ajax({
            url : "console/init",
            success : function(data) {
                // unpacks the resulting json data into the result
                // and the instance part, so that they may be used
                // in the processing of the results
                var result = data["result"];
                var instance = data["instance"];

                // splits the result value (into the appropriate components) and
                // also adds it to the previous action container, then scrolls
                // the current console area to the lower part
                var line = splitValue(result, true);
                jQuery(".console .previous").append("<div>" + line + "</div>");
                jQuery(".console").scrollTop(jQuery(".console")[0].scrollHeight);

                // sets the instance (identifier) value in the console
                // for latter usage of the value
                jQuery(".console").data("instance", instance);

                // restores the current line display, because the loading is now
                // considered complete
                jQuery(".console .current").show();
            }
        });
    };

    // initializes the cursor position at the end
    // of the console line (initial position)
    jQuery(".console").data("cursor", -1);

    // resets the console text to avoid any possible auto
    // complete operation
    jQuery(".console .text").val("");

    // "clicks" in the console so that the focus is started
    // at the console (immediate interaction)
    jQuery(".console").click();

    // initializes the console by requesting the initial instace
    // from the client side (initialization scripts should be
    // executed at this stage)
    init();
});