var gulp = require('gulp')
	concat = require('gulp-concat')
	del = require('del');

gulp.task('scripts', function() {
	return gulp.src(['bower_components/angular/*.min.js','bower_components/**/*.min.js'])
		.pipe(concat('lib.js'))
		.pipe(gulp.dest('dist/js'));
});

gulp.task('styles', function() {
	return gulp.src('bower_components/**/*.min.css')
		.pipe(concat('lib.css'))
		.pipe(gulp.dest('dist/css'));
});

gulp.task('fonts', function() {
	return gulp.src('bower_components/bootstrap/fonts/*')
		.pipe(gulp.dest('dist/css/fonts'));
});

gulp.task('clean', function(cb) {
    del(['dist/css', 'dist/js', 'dist/img'], cb)
});

gulp.task('default', ['clean'], function() {
	gulp.start('scripts', 'styles', 'fonts');
});

gulp.task('watch', function() {

  // Watch .scss files
  gulp.watch('src/styles/**/*.scss', ['styles']);

  // Watch .js files
  gulp.watch('bower_components/**/*.js', ['scripts']);

  // Watch image files
  gulp.watch('src/images/**/*', ['images']);

});