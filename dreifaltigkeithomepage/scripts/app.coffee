angular.module 'dreifaltigkeithomepage', [
    'js-data'
    'ui.router'
    'dreifaltigkeithomepage-templates'
    'dreifaltigkeithomepage.home'
    'dreifaltigkeithomepage.event'
    'dreifaltigkeithomepage.page'
]

.config [
    '$locationProvider'
    '$urlRouterProvider'
    ($locationProvider, $urlRouterProvider) ->

        # Uses HTML5 mode for location in browser address bar
        $locationProvider.html5Mode true

        # For any unmatched url, redirect to /
        $urlRouterProvider.otherwise '/'
]

.config [
    'DSHttpAdapterProvider'
    (DSHttpAdapterProvider) ->
        angular.extend DSHttpAdapterProvider.defaults,
            basePath: '/api'
]


.factory 'Event', [
    'DS'
    (DS) ->
        DS.defineResource
            name: 'event/'
]

.factory 'EventType', [
    'DS'
    (DS) ->
        DS.defineResource
            name: 'eventtype/'
            idAttribute: 'db_value'
]

.factory 'Page', [
    'DS'
    'Event'
    (DS, Event) ->
        DS.defineResource
            name: 'page/'
            methods:
                getSlug: () ->
                    slug = ''
                    angular.forEach @path, (element) ->
                        slug += '/' + element.slug
                    slug.slice(1)
                getEvents: () ->
                    params =
                        where:
                            type:
                                '===': @event_type
                    Event.filter params
]

.run [
    'Event'
    'EventType'
    'Page'
    (Event, EventType, Page) ->
]
