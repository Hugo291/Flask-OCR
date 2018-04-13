   // handle custom file inputs
    $('body').on('change', 'input[type="file"][data-toggle="custom-file"]', function (ev) {

      const $input = $(this);
      const target = $input.data('target');
      const $target = $(target);

      if (!$target.length)
        return console.error('Invalid target for custom file', $input);

      if (!$target.attr('data-content'))
        return console.error('Invalid `data-content` for custom file target', $input);

      // set original content so we can revert if user deselects file
      if (!$target.attr('data-original-content'))
        $target.attr('data-original-content', $target.attr('data-content'));

      const input = $input.get(0);

      let name = _.isObject(input)
        && _.isObject(input.files)
        && _.isObject(input.files[0])
        && _.isString(input.files[0].name) ? input.files[0].name : $input.val();

      if (_.isNull(name) || name === '')
        name = $target.attr('data-original-content');

      $target.attr('data-content', name);

    });