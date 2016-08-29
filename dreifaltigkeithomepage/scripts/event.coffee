angular.module 'dreifaltigkeithomepage.event', []

.config [
    '$stateProvider'
    ($stateProvider) ->
        $stateProvider
        .state 'event',
            url: '/event/:id/'
            templateUrl: 'event.html'
            resolve:
                page: [
                    '$q'
                    '$stateParams'
                    'Event'
                    'Page'
                    ($q, $stateParams, Event, Page) ->
                        Event.find $stateParams.id
                        promises = [
                            Event.find $stateParams.id
                            Page.findAll()  # TODO: Do not load all. What do we need for the main menu?
                        ]
                        $q.all promises
                ]
        return
]

.controller 'EventCtrl', [
    () ->
        # TODO: Add event here and watch it.
        return
]
