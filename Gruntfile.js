module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      dist: {
        files: [{
          expand: true,
          cwd: 'materialize/dist/',
          src: [
            'font/**',
          ],
          dest: 'theme/static/',
          flatten: false
        }]
      }
    },
    sass: {
      dist: {
        options: {
          loadPath: ['materialize/sass/'],
          style: 'compressed'
        },
        files: {
          'theme/static/css/main.css': 'theme/static/sass/main.scss'
        }
      }
    },
    uglify: {
      dist: {
        files: [{
          expand: true,
          flatten: true,
          cwd: 'theme/static/',
          src: 'js-src/*.js',
          dest: 'theme/static/js'
        }]
      }
    },
    concat: {
      dist: {
        src: [
          'materialize/dist/js/materialize.min.js',
          'theme/static/js/init.js',
        ],
        dest: 'theme/static/js/main.js',
      },
    },
    watch: {
      options: {
        atBegin: true
      },  
      sass: {
        files: ['materialize/sass/**', 'theme/static/sass/**'],
        tasks: ['default'],
      }
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.registerTask('default', ['sass', 'copy', 'uglify', 'concat']);
};
