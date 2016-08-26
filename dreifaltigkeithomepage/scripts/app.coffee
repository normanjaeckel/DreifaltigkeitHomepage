angular.module 'dreifaltigkeithomepage', [
    'dreifaltigkeithomepage-templates'
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
        .state 'home',
            url: '/'
            templateUrl: 'home.html'
        return
]


.controller 'LosungenCtrl', [
    '$http'
    ($http) ->
        $http.get '/api/losungen'
        .then(
            (success) =>
                @losungen = success.data
                return
            (error) ->
                console.error error
                return
        )
        return
]
