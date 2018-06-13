module.exports = function(grunt) {
grunt.initConfig({
  uglify: {
    compile: {
      files: {
        'src/angular-resource-tastypie.min.js': ['src/angular-resource-tastypie.js']
      }
    }
  }
});

grunt.loadNpmTasks('grunt-contrib-uglify'); // load the given tasks
grunt.registerTask('default', ['uglify']); // Default grunt tasks maps to grunt
};