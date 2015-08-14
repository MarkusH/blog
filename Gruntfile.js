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
    webfont: {
      icons: {
        src: 'theme/static/font-src/*.svg',
        dest: 'theme/static/font',
        destCss: 'theme/static/sass',
        options: {
          htmlDemo: false,
          stylesheet: 'scss',
          syntax: 'bootstrap',
          types: 'eot,woff,ttf,svg'
        }
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
        files: {
          'theme/static/js/main.js': [
            'theme/static/js/jquery-2.1.1.min.js',
            'theme/static/js/masonry.pkgd.min.js',
            'theme/static/js/imagesloaded.pkgd.min.js',
            'materialize/dist/js/materialize.min.js',
            'theme/static/js/init.js',
          ],
          'theme/static/js/head.js': [
            'theme/static/js/picturefill.min.js',
          ],
        },
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
  grunt.loadNpmTasks('grunt-webfont');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.registerTask('default', ['webfont', 'sass', 'copy', 'uglify', 'concat']);
};
