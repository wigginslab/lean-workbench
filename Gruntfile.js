/*
 * lean-workbench
 * https://github.com/wigginslab/lean-workbench
 *
 * Copyright (c) 2013 Jennifer Brooke Rubinovitz
 * Licensed under the MIT license.
 */

'use strict';

'use strict';

module.exports = function (grunt) {

grunt.initConfig({
    sass: {
        dist: {
            options: {
                style: 'expanded'
            },
            files: [{
                expand: true,
                cwd: './static/sass',
                src: ['*.scss'],
                dest: './static/css',
                ext: '.css'
            }]
        }
    }
});
grunt.loadNpmTasks('grunt-sass');

grunt.registerTask('default', ['sass']);
};
  // Project configuration.
/*  grunt.initConfig({
    jshint: {
      all: [
        'Gruntfile.js',
        'tasks/*.js',
        '<%= nodeunit.tests %>',
      ],
      options: {
        jshintrc: '.jshintrc',
      },
    },

    // Before generating any new files, remove any previously-created files.
    clean: {
      tests: ['tmp'],
    },

    // Configuration to be run (and then tested).
    lean_workbench: {
      default_options: {
        options: {
        },
        files: {
          'tmp/default_options': ['test/fixtures/testing', 'test/fixtures/123'],
        },
      },
      custom_options: {
        options: {
          separator: ': ',
          punctuation: ' !!!',
        },
        files: {
          'tmp/custom_options': ['test/fixtures/testing', 'test/fixtures/123'],
        },
      },
    },

    // Unit tests.
    nodeunit: {
      tests: ['test/*_test.js'],
    },

  });

  // Actually load this plugin's task(s).
  grunt.loadTasks('tasks');

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-nodeunit');

  // Whenever the "test" task is run, first clean the "tmp" dir, then run this
  // plugin's task(s), then test the result.
  grunt.registerTask('test', ['clean', 'lean_workbench', 'nodeunit']);

  // By default, lint and run all tests.
  grunt.registerTask('default', ['jshint', 'test']);

};*/
