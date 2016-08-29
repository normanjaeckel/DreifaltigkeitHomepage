angular.module 'dreifaltigkeithomepage.home', []

.config [
    '$stateProvider'
    ($stateProvider) ->
        $stateProvider
        .state 'home',
            url: '/'
            templateUrl: 'home.html'
        return
]

.controller 'LosungenCtrl', [
    '$http'
    ($http) ->
        $http.get '/api/losungen/'
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

.controller 'MainLinksCtrl', [
    '$scope'
    'Page'
    ($scope, Page) ->
        params =
            where:
                parent:
                    '===': null
        Page.findAll(params)
        $scope.$watch(
            () ->
                Page.lastModified()
            () =>
                @pages = Page.filter params
                return
        )
        return
]

.controller 'EventsCtrl', [
    '$scope'
    'Event'
    ($scope, Event) ->
        params =
            where:
                on_home_before_begin:
                    '>': 0
        Event.findAll(params)
        $scope.$watch(
            () ->
                Event.lastModified()
            () =>
                @events = Event.filter params
                return
        )
        return
]
