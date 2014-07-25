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
                style: 'compressed'
            },
            files: [{
                expand: true,
                cwd: './lean_workbench/static/sass',
                src: ['*.scss'],
                dest: './lean_workbench/static/css',
                ext: '.css'
            }]
        }
    },

      concat: {
        css: {
           src: [
                 'lean_workbench/static/css/*'
                ],
            dest: 'lean_workbench/static/css/combined.css'
        },
        js : {
            src : [
               'lean_workbench/static/js/app.js',
               'lean_workbench/static/js/controllers.js',
               'lean_workbench/static/js/directives.js',
               'lean_workbench/static/js/filters.js',
               'lean_workbench/static/js/resources.js',
               'lean_workbench/static/js/services.js',
            ],
            dest : 'lean_workbench/static/js/combined.js'
        }
    },

      cssmin : {
          css:{
              src: 'lean_workbench/static/css/combined.css',
              dest: 'lean_workbench/static/css/combined.min.css'
          }
      },

       uglify : {
        js: {
            files: {
                'lean_workbench/static/js/combined.js' : [ 'lean_workbench/static/js/combined.js' ]
            }
        },

        watch: {
          files: ['lean_workbench/static/css/*', 'lean_workbench/static/js/*'],
          tasks: ['concat', 'cssmin', 'uglify']
      }
    },


    pkg: grunt.file.readJSON('package.json')
});

    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.registerTask('default', [ 'sass','concat:css', 'cssmin:css', 'concat:js', 'uglify:js' ]);

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
