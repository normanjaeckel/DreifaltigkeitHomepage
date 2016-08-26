angular.module 'dreifaltigkeithomepage', [
    'js-data'
    'ui.router'
    'dreifaltigkeithomepage-templates'
    'dreifaltigkeithomepage.home'
    'dreifaltigkeithomepage.page'
]

.config [
    '$locationProvider'
    '$stateProvider'
    '$urlRouterProvider'
    ($locationProvider, $stateProvider, $urlRouterProvider) ->

        # Uses HTML5 mode for location in browser address bar
        $locationProvider.html5Mode true

        # For any unmatched url, redirect to /
        $urlRouterProvider.otherwise '/'

        # Set up the states
        $stateProvider
        .state 'home',
            url: '/'
            templateUrl: 'home.html'
        .state 'page',
            url: '/{slug:any}/'
            templateUrl: 'page.html'
        return
]

.config [
    'DSHttpAdapterProvider'
    (DSHttpAdapterProvider) ->
        angular.extend DSHttpAdapterProvider.defaults,
            basePath: '/api'
]


.factory 'Page', [
    'DS'
    (DS) ->
        DS.defineResource
            name: 'page/'
            methods:
                getSlug: () ->
                    slug = ''
                    angular.forEach @path, (element) ->
                        slug += '/' + element.slug
                    slug.slice(1)
]

.run [
    'Page'
    (Page) ->
]
