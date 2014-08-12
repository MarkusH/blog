module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      dist: {
        files: [{
          expand: true,
          cwd: 'bower_components/foundation/js/',
          src: [
            'vendor/jquery.js',
            'vendor/modernizr.js',
          ],
          dest: 'theme/static/js/',
          flatten: true,
          filter: 'isFile',
        },
        {
          expand: true,
          cwd: 'bower_components/foundation/js/foundation/',
          src: [
            'foundation.js',
            'foundation.clearing.js',
            'foundation.topbar.js',
          ],
          dest: 'theme/static/js/src/',
          flatten: true,
          filter: 'isFile',
        }]
      }
    },
    sass: {
      dist: {
        options: {
          loadPath: ['bower_components/foundation/scss/'],
          style: 'compressed'
        },
        files: {
          'theme/static/css/normalize.css': 'bower_components/foundation/scss/normalize.scss',
          'theme/static/css/main.css': 'theme/static/sass/main.scss'
        }
      }
    },
    uglify: {
      dist: {
        files: [{
          expand: true,
          flatten: true,
          cwd: 'theme/static/js',
          src: 'src/*.js',
          dest: 'theme/static/js'
        }]
      }
    },
    concat: {
      options: {
        separator: ';',
        stripBanners: {block: true},
        process: function(src, filepath) {
          if (filepath === 'theme/static/js/jquery.js') {
            src = src.replace(/\/\*!/g, '\n\/\*!');
            src = src.replace(/^(\/\*!| \*.*)\n/gm, '');
          }
          return src;
        },
      },
      dist: {
        src: [
          'theme/static/js/modernizr.js',
          'theme/static/js/jquery.js',
          'theme/static/js/foundation.js',
          'theme/static/js/foundation.clearing.js',
          'theme/static/js/foundation.topbar.js',
        ],
        dest: 'theme/static/js/main.js',
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.registerTask('default', ['sass', 'copy', 'uglify', 'concat']);
};
