(function (window, $) {

    var Fileselect = function (fileInput, options) {
        this.$fileInput = $(fileInput);
        this.options = options;
        this.userLanguage = 'en';
        this.$fileselect = $(this);
        this.metadata = this.$fileInput.data();
        this.$inputGroup = $('<div>').addClass('input-group');
        this.$inputGroupBtn = $('<label>').addClass('input-group-btn');
        this.$browseBtn = $('<span>');
        this.$labelInput = $('<input>').attr('type', 'text').attr('readonly', true).addClass('form-control');
        this.translations = {
            'en': {
                'browse': 'Browse',
                'rules': {
                    'numberOfFiles': 'The number of uploadable files is limited to [num] file(s)',
                    'fileExtensions': 'The files are restricted to following file extensions: [ext]',
                    'fileSize': 'The file size is limited to [size]',
                }
            },
            'de': {
                'browse': 'Durchsuchen',
                'rules': {
                    'numberOfFiles': 'Die Anzahl der hochladbaren Dateien ist limitiert auf [num] Datei(en)',
                    'fileExtensions': 'Die Dateien sind eingeschränkt auf folgende Dateierweiterungen: [ext]',
                    'fileSize': 'Die Grösse ist eingeschränkt auf [size] pro Datei',
                }
            }
        };
        this.init();
    };
    Fileselect.prototype = {
        defaults: {
            browseBtnClass: 'btn btn-primary',
            browserBtnPosition: 'right',
            limit: false,
            extensions: false,
            allowedFileSize: false,
            allowedFileExtensions: false,
            allowedNumberOfFiles: false,
            language: 'en',
            validationCallback: function (message, instance) {
                alert(message);
            }
        },
        init: function () {
            this.config = this.loadConfig();
            this.translations = this.loadTranslation();

            this.$fileInput
                    .hide()
                    .after(this.$inputGroup);

            if (this.config.browseBtnPosition === 'left') {
                this.$inputGroup.append(this.$inputGroupBtn, this.$labelInput);
            } else {
                this.$inputGroup.append(this.$labelInput, this.$inputGroupBtn);
            }

            this.$inputGroupBtn
                    .append(this.$browseBtn)
                    .append(this.$fileInput)
                    .css('margin-bottom', 0);

            this.$browseBtn
                    .addClass(this.config.browseBtnClass)
                    .text(this.translations.browse);

            this.$fileInput.on('change', $.proxy(this.changeEvent, this));

            return $(this);
        },
        changeEvent: function (e) {
            this.$fileInput.trigger('bs.fs.change', [this]);

            var files = this.$fileInput[0].files,
                    label = $.map(files, function (file) {
                        return file.name;
                    }).join(', ');

            var result = false;
            if (this.validateNumberOfFiles(files) && this.valiateFileExtensions(files) && this.validateFileSize(files)) {
                this.$labelInput.val(label);
                result = true;
            } else {
                this.$fileInput.val(null);
            }

            this.$fileInput.trigger('bs.fs.changed', [this]);

            return result;
        },
        loadConfig: function () {
            var config = $.extend({}, this.defaults, this.options, this.metadata);
            if (typeof config.allowedFileExtensions === 'string') {
                config.allowedFileExtensions = config.allowedFileExtensions.split(',');
            }
            return config;
        },
        loadTranslation: function () {
            var userLanguage = this.config.language || navigator.language || navigator.userLanguage,
                    translatedLanguages = $.map(this.translations, function (translations, key) {
                        return key;
                    });

            if ($.inArray(userLanguage, translatedLanguages) >= 0) {
                this.userLanguage = userLanguage;
            } else {
                console.warn('Current user language has no translation. Switched to english as default language.')
            }

            return this.translations[userLanguage];
        },
        validateNumberOfFiles: function (files) {
            this.$fileInput
                    .trigger('bs.fs.validate', [this])
                    .trigger('bs.fs.number-of-files-validate', [this]);

            var result = true;
            if (this.config.allowedNumberOfFiles && files.length > parseInt(this.config.allowedNumberOfFiles)) {
                this.config.validationCallback(this.translations.rules.numberOfFiles.replace('[num]', this.config.allowedNumberOfFiles), 'allowedNumberOfFiles', this);
                result = false;
            }

            this.$fileInput
                    .trigger('bs.fs.validated', [this])
                    .trigger('bs.fs.number-of-files-validated', [this]);

            return result;
        },
        valiateFileExtensions: function (files) {
            this.$fileInput
                    .trigger('bs.fs.validate', [this])
                    .trigger('bs.fs.file-extensions-validate', [this]);

            var result = true;
            if (this.config.allowedFileExtensions) {
                $.each(files, $.proxy(function (i, file) {
                    var fileExtension = file.name.replace(/^.*\./, '').toLowerCase();
                    if ($.inArray(fileExtension, this.config.allowedFileExtensions) === -1) {
                        this.config.validationCallback(this.translations.rules.fileExtensions.replace('[ext]', this.config.allowedFileExtensions.join(', ')), 'allowedFileExtensions', this);
                        result = false;
                        return;
                    }
                }, this));
            }

            this.$fileInput
                    .trigger('bs.fs.validated', [this])
                    .trigger('bs.fs.file-extensions-validated', [this]);

            return result;
        },
        validateFileSize: function (files) {
            this.$fileInput
                    .trigger('bs.fs.validate', [this])
                    .trigger('bs.fs.file-size-validate', [this]);

            var result = true;
            if (this.config.allowedFileSize) {
                $.each(files, $.proxy(function (i, file) {
                    if (file.size > this.config.allowedFileSize) {
                        this.config.validationCallback(this.translations.rules.fileSize.replace('[size]', Math.round(this.config.allowedFileSize / 1024 / 1024) + 'MB'), 'allowedFileSize', this);
                        result = false;
                        return;
                    }
                }, this));
            }

            this.$fileInput
                    .trigger('bs.fs.validated', [this])
                    .trigger('bs.fs.file-size-validated', [this]);

            return result;
        },

    };


    Fileselect.defaults = Fileselect.prototype.defaults;

    $.fn.fileselect = function (options) {
        this.each(function () {
            new Fileselect(this, options);
        });
        return this;
    };

    window.Fileselect = Fileselect;
})(window, jQuery);
