argv = require 'yargs'
    .argv
cleanCSS = require 'gulp-cleancss'
concat = require 'gulp-concat'
fs = require 'fs'
gulp = require 'gulp'
coffee = require 'gulp-coffee'
gulpif = require 'gulp-if'
gutil = require 'gulp-util'
mainBowerFiles = require 'main-bower-files'
path = require 'path'
rename = require 'gulp-rename'
template = require 'gulp-template'
uglify = require 'gulp-uglify'


# Helpers and config

productionMode = argv.production

projectName = 'dreifaltigkeithomepage'

outputDirectory = path.join __dirname, 'dreifalthomeDeploy'

staticDirectory = path.join outputDirectory, 'static'

mediaDirectory = path.join outputDirectory, 'media'


# Gulp default task

gulp.task 'default', ['django', 'css', 'js'], ->


# Django settings and wsgi file and media directory

gulp.task 'django', [
    'createmanage'
    'createsettings'
    'createwsgifile'
    'createmediadirectory'
], ->

gulp.task 'createmanage', ->
    gulp.src path.join __dirname, projectName, 'default_manage.py'
    .pipe template
        outputDirectoryBaseName: path.basename outputDirectory
    .pipe rename 'manage.py'
    .pipe gulp.dest __dirname

gulp.task 'createsettings', (callback) ->
    settingsPath = path.join outputDirectory, 'settings.py'
    fs.access settingsPath, (error) ->
        if error? and error.code is 'ENOENT'
            secretKey = ''
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            for i in [1..50]
                randomnumber = Math.floor Math.random() * chars.length
                secretKey += chars[randomnumber]
            gulp.src path.join __dirname, projectName, 'default_settings.py'
            .pipe template
                outputDirectoryBaseName: path.basename outputDirectory
                projectName: projectName
                secretKey: secretKey
            .pipe rename 'settings.py'
            .pipe gulp.dest outputDirectory
            .on 'end', callback
        else
            gutil.log 'Task createsettings: Settings file does already exist.
                Skip task.'
            callback error
        return
    return

gulp.task 'createwsgifile', (callback) ->
    wsgiPath = path.join outputDirectory, 'wsgi.py'
    fs.access wsgiPath, (error) ->
        if error? and error.code is 'ENOENT'
            gulp.src path.join __dirname, projectName, 'default_wsgi.py'
            .pipe template
                outputDirectory: outputDirectory
                outputDirectoryBaseName: path.basename outputDirectory
            .pipe rename 'wsgi.py'
            .pipe gulp.dest outputDirectory
            .on 'end', callback
        else
            gutil.log 'Task createwsgifile: Wsgi file does already exist. Skip
                task.'
            callback error
        return
    return

gulp.task 'createmediadirectory', ['createsettings'], (callback) ->
    fs.mkdir mediaDirectory, (error) ->
        if error? and error.code is 'EEXIST'
            callback()
        else
            callback error
        return
    return


# CSS and font files

gulp.task 'css', [
    'sass'
    'css-extra'
    'css-libs'
    'fonts-libs'
    'maps-libs'
], ->

gulp.task 'sass', ->

gulp.task 'css-extra', ->
    gulp.src path.join projectName, 'static', 'css', '*.css'
    .pipe concat "#{projectName}-extra.css"
    .pipe gulpif productionMode, cleanCSS
        compatibility: 'ie8'
    .pipe gulp.dest path.join staticDirectory, 'css'

gulp.task 'css-libs', ->
    gulp.src mainBowerFiles
        filter: /\.css$/
    .pipe concat "#{projectName}-libs.css"
    .pipe gulpif productionMode, cleanCSS
        compatibility: 'ie8'
    .pipe gulp.dest path.join staticDirectory, 'css'

gulp.task 'fonts-libs', ->
    gulp.src mainBowerFiles
        filter: /\.(eot)|(svg)|(ttf)|(woff)|(woff2)$/
    .pipe gulp.dest path.join staticDirectory, 'fonts'

gulp.task 'maps-libs', ->
    gulp.src mainBowerFiles
        filter: /\.map$/
    .pipe gulp.dest path.join staticDirectory, 'css'


# JavaScript files

gulp.task 'js', [
    'coffee'
    'js-extra'
    'js-libs'
], ->

gulp.task 'coffee', ->
    gulp.src path.join projectName, 'scripts', '**', '*.coffee'
    .pipe coffee()
    .pipe concat "#{projectName}.js"
    .pipe gulpif productionMode, uglify()
    .pipe gulp.dest path.join outputDirectory, 'static', 'js'

gulp.task 'js-extra', ->
    gulp.src path.join projectName, 'static', 'js', '*.js'
    .pipe concat "#{projectName}-extra.js"
    .pipe gulpif productionMode, uglify()
    .pipe gulp.dest path.join outputDirectory, 'static', 'js'

gulp.task 'js-libs', ->
    isntSpecialFile = (file) ->
        name = path.basename file.path
        name isnt 'html5shiv.js' and name isnt 'respond.min.js'
    gulp.src mainBowerFiles
        filter: /\.js$/
    .pipe gulpif isntSpecialFile, concat "#{projectName}-libs.js"
    .pipe gulpif productionMode, uglify()
    .pipe gulp.dest path.join staticDirectory, 'js'


# Helper tasks.

gulp.task 'watch', ['coffee'], ->
    gulp.watch path.join(projectName, 'scripts', '**', '*.coffee'),
        ['coffee']
    return
