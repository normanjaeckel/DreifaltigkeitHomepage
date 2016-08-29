angular.module 'dreifaltigkeithomepage.page', []

.config [
    '$stateProvider'
    ($stateProvider) ->
        $stateProvider
        .state 'page',
            url: '/{slug:any}/'
            templateUrl: 'page.html'
            resolve:
                page: [
                    '$q'
                    '$stateParams'
                    'Event'
                    'EventType'
                    'Page'
                    'SlugParser'
                    ($q, $stateParams, Event, EventType, Page, SlugParser) ->
                        slug = SlugParser.getSlug $stateParams
                        params =
                            where:
                                slug:
                                    '===': slug
                        promises = [
                            Page.findAll params
                            .then(
                                () ->
                                    pages = Page.filter params
                                    pages[0]
                            )
                            Page.findAll()  # TODO: Do not load all. What do we need for the main menu?
                            Event.findAll()  # TODO: Do not load all but only required events.
                            EventType.findAll()  # TODO: Do not load all but only required event types.
                        ]
                        $q.all promises
                ]
        return
]

.factory 'SlugParser', [
    () ->
        getSlug: (stateParams) ->
            index = stateParams.slug.lastIndexOf '/'
            if index is -1
                stateParams.slug
            else
                index++
                stateParams.slug.slice index
]

.factory 'PageTree', [
    () ->
        getTree: (pages) ->
            # Build an object with all children to a specific page
            pageStore = {}
            angular.forEach pages, (page) ->
                if page.parent?
                    if not pageStore[page.parent]
                        pageStore[page.parent] = []
                    pageStore[page.parent].push page
                return

            # Recursive function that generates a nested list with all pages
            # with their children
            getChildren = (pages) ->
                children = []
                angular.forEach pages, (page) ->
                    children.push
                        id: page.id
                        page: page
                        children: getChildren pageStore[page.id]
                children

            # Build the list of root pages (without parents)
            rootPages = pages.filter (page) ->
                not page.parent

            getChildren rootPages
]

.directive 'mainMenuTree', [
    () ->
        restrict: 'E',
        scope:
            element: '='
            slug: '='
        template: '<a ui-sref="page({ slug: element.page.getSlug() })">{{ element.page.title }}</a> ' +
                  '<span ng-show="slug && element.page.slug === slug">*</span>' +
                  '<ul>' +
                    '<li ng-repeat="child in element.children">' +
                      '<main-menu-tree element="child" slug="slug"></main-menu-tree>' +
                    '</li>' +
                  '</ul>'
]

.controller 'MenuCtrl', [
    '$scope'
    '$stateParams'
    'Page'
    'SlugParser'
    'PageTree'
    ($scope, $stateParams, Page, SlugParser, PageTree) ->
        if $stateParams.slug
            @slug = SlugParser.getSlug $stateParams
        $scope.$watch(
            () ->
                Page.lastModified()
            () =>
                @rootElement =
                    page:
                        getSlug: () ->  # Empty function to avoid error in directive template
                    children: PageTree.getTree Page.getAll()
                return
        )
        return
]

.controller 'PageCtrl', [
    '$scope'
    '$stateParams'
    'Event'
    'EventType'
    'Page'
    'SlugParser'
    ($scope, $stateParams, Event, EventType, Page, SlugParser) ->
        page = $scope.$parent.$resolve.page[0]
        events = $scope.$parent.$resolve.events
        $scope.$watch(
            () ->
                Page.lastModified(page.id)
            () =>
                @page = page
                if @page.type is 'event'
                    @events = @page.getEvents()
                    @eventType = EventType.get @page.event_type
                return
        )
        return
]
