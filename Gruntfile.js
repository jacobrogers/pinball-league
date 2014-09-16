module.exports = function(grunt) {
	grunt.initConfig({
		uglify: {
			build: { 
				src: 'assets/js/src/*.js',
				dest: 'build/app.js'
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-uglify');

	grunt.registerTask('default', ['uglify']);
};