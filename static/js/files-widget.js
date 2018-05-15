var FilesWidgetController = (function() {

    function FilesWidgetFile(id, name, date, download_url, direct_url, thumbnail_url) {
        this.id = id;
        this.name = name;
        this.date = date;
        this.download_url = download_url;
        this.direct_url = direct_url;
        this.thumbnail_url = thumbnail_url;
    }

    function FilesWidgetController(root_el, options = {}) {
        var default_options = {
            "list_url": "/act/files/ls",
            "upload_url": "/act/files/upload",
            "update_immediately": true
        };

        for (var opt in options) {
            default_options[opt] = options[opt];
        }

        // Initialize
        this.files = new Array();
        this.sorted_files = {
            "name": new Array(),
            "date": new Array()
        }

        this.comparators = {
            "name": function(a, b) { return a < b; },
            "date": function(a, b) { return a > b; }
        }
        
        this.sort_by = "date";
        this.file_widgets = new Array();

        // Options
        this.upload_url = default_options.upload_url;
        this.list_url = default_options.list_url;

        // Collect DOM elements
        this.root = root_el;
        this.list_widget = this._findElementByDataId("list-block");
        this.upload_widget = this._findElementByDataId("upload-block");
        this.upload_input = $(this.upload_widget).find("input[type=\"file\"]")[0];
        this.upload_progress_widget = this._findElementByDataId("upload-progress-block");
        $(this.upload_progress_widget).hide();
        this.loading_list_widget = this._findElementByDataId("list-loading-block");
        $(this.loading_list_widget).hide();

        this.search_widget = this._findElementByDataId("search-block");
        this.search_input = $(this.search_widget).find("input[type=\"text\"]")[0];
        this.search_clear_button = $(this.search_widget).find("button[data-id=\"search-clear\"]")[0];

        this.sort_widget = this._findElementByDataId("sort-block");
        this.sort_by_name_link = this._findElementByDataId("sort-by-name");
        this.sort_by_date_link = this._findElementByDataId("sort-by-date");

        $(this.sort_by_date_link).addClass("selected");

        // Calculate list size
        var height = $(this.root).innerHeight();
        var topBarHeight = $(this.upload_widget).outerHeight() + $(this.search_widget).outerHeight() + $(this.sort_widget).outerHeight();
        $(this.list_widget).height(height - topBarHeight);

        // Assign event handlers
        var self = this;

        $(this.upload_input).change(function(event) {
            event.preventDefault();
            event.stopPropagation();
            self.do_upload(self.upload_url);
        });

        $(this.sort_by_name_link).click(function(event) {
            event.preventDefault();
            event.stopPropagation();
            self.set_sort_by("name");
            $(self.sort_by_date_link).removeClass("selected");
            $(self.sort_by_name_link).addClass("selected");
        });

        $(this.sort_by_date_link).click(function(event) {
            event.preventDefault();
            event.stopPropagation();
            self.set_sort_by("date");
            $(self.sort_by_date_link).addClass("selected");
            $(self.sort_by_name_link).removeClass("selected");
        });

        $(this.search_input).on('input', function(event) {
            event.preventDefault();
            event.stopPropagation();
            self.filter($(this).val());
        });

        $(this.search_clear_button).click(function(event) {
            event.preventDefault();
            event.stopPropagation();
            $(self.search_input).val("");
            self.filter("");
        });

        if (default_options.update_immediately) {
            this.get_files_from_server();
        }
    }

    FilesWidgetController.prototype._findElementByDataId = function(data_id) {
        return this._findElementBySelector("[data-id=\"" + data_id + "\"]");
    }

    FilesWidgetController.prototype._findElementBySelector = function(selector) {
        var children = $(this.root).find(selector);
        if (children.length == 0) {
            throw new Error("Selector not found: \"" + selector + "\".");
        }
        return children[0];
    }

    FilesWidgetController.prototype.add_file = function(fileObject) {
        var new_id = this.files.length;
        var file = new FilesWidgetFile(
                new_id,
                fileObject["name"], 
                fileObject["date"],
                fileObject["url"],
                fileObject["direct_url"],
                fileObject["thumb_url"]
            );
        this.files.push(file);
        this.insert_sorted(file, "name");
        this.insert_sorted(file, "date");
        this.synchronize_view();
    };

    FilesWidgetController.prototype.insert_sorted = function(file, key) {
        var list = this.sorted_files[key];
        for (var i = 0; i < list.length; ++i) {
            if (this.comparators[key](file[key], list[i][key])) {
                list.splice(i, 0, file);
                return;
            }
        }
        list.push(file);

    };

    FilesWidgetController.prototype.synchronize_view = function() {
        var i = 0;
        var j = 0;
        var sorted_list = this.sorted_files[this.sort_by];
        var file_widgets = this.file_widgets;
        while (j < file_widgets.length && i < sorted_list.length) {
            if (file_widgets[j].attr("file-id") != sorted_list[i].id) {
                var w = this.create_file_widget(sorted_list[i]);
                file_widgets[j].before(w);
                file_widgets.splice(j, 0, w);
            }
            ++i;
            ++j;
        }

        for (;i < sorted_list.length; ++i) {
            var w = this.create_file_widget(sorted_list[i]);
            file_widgets.push(w);
            $(this.list_widget).append(w);
        }
    }

    FilesWidgetController.prototype.create_file_widget = function(file) {
        var div = $(document.createElement("li"));
        div.addClass("files-widget-file");
        div.attr("file-id", file.id);
        div.append("<img src=\"" + file.thumbnail_url + "\" class=\"thumb\">");
        div.append("<div class=\"filename\">" + file.name + "</div>");
        var links_div = $("<div class=\"file-links\"></div>");
        links_div.append("<a href=\"" + file.download_url + "\">Download</a>");
        links_div.append(" | ");
        links_div.append("<a href=\"" + file.direct_url + "\">Direct</a>");
        div.append(links_div);
        div.append("<div class=\"file-date\">" + file.date + "</div>");
        return div;
    }

    FilesWidgetController.prototype.get_files_from_server = function() {
        $(this.list_widget).hide();
        $(this.loading_list_widget).show();
        var url = this.list_url;
        
        var self = this;
        $.getJSON(url).done(function(data) {
            $(self.loading_list_widget).hide();
            $(self.list_widget).show();
            self.clear();

            for (var i = 0; i < data.files.length; ++i) {
                self.add_file(data.files[i]);
            }

        }).fail(function() {
            $(self.loading_list_widget).html("<p>Error: can not retrieve list of files. Try to refresh the page.</p>");
        });
    }

    FilesWidgetController.prototype.clear = function() {
        this.files = new Array();
        this.sorted_files["name"] = new Array();
        this.sorted_files["date"] = new Array();
        this.clear_file_widgets();
    }

    FilesWidgetController.prototype.clear_file_widgets = function() {
        for (var i = 0; i < this.file_widgets.length; ++i) {
            this.file_widgets[i].remove();
        }
        this.file_widgets = new Array();
    }

    FilesWidgetController.prototype.set_sort_by = function(key) {
        if (key == this.sort_by) {
            return;
        }
        this.clear_file_widgets();
        this.sort_by = key;
        this.synchronize_view();
    }

    FilesWidgetController.prototype.do_upload = function(url) {
        if ("files" in this.upload_input) {
            if (this.upload_input.files.length == 0) {
                return;
            }
            var data = new FormData();
            for (var i = 0; i < this.upload_input.files.length; ++i) {
                var f = this.upload_input.files[i];
                data.append("upload", f, f.name);
            }

            var csrf_token = this.find_csrf_token();

            data.append("csrfmiddlewaretoken", csrf_token);

            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
            var self = this
            xhr.onload = function() {
                if (xhr.status == 200) {
                    var newFiles = JSON.parse(xhr.responseText);
                    $(self.upload_widget).show();
                    $(self.upload_progress_widget).hide();
                    $(self.upload_input).val("");
                    for (var i = 0; i < newFiles.files.length; ++i) {
                        self.add_file(newFiles.files[i]);
                    }
                }
            }

            $(this.upload_widget).hide();
            $(this.upload_progress_widget).show();
            xhr.send(data);
        }
    }

    FilesWidgetController.prototype.find_csrf_token = function() {
        var token_input = $("input[name=\"csrfmiddlewaretoken\"]");
        if (token_input) {
            return token_input.val();
        }
        return "";
    }

    FilesWidgetController.prototype.filter = function(s) {
        var list = this.sorted_files[this.sort_by];
        var widgets = this.file_widgets;
        var re = new RegExp(s, "i");
        for (var i = 0; i < list.length; ++i) {
            if (s.length == 0 || list[i].name.search(re) > -1) {
                widgets[i].show();
            } else {
                widgets[i].hide();
            }
        }
    }

    return FilesWidgetController;

}());
