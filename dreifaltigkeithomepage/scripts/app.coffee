angular.module 'dreifaltigkeithomepage', [
    'ui.router'
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
        .state 'state1',
            url: '/state1'
            templateUrl: 'partials/state1.html'
        return
]
