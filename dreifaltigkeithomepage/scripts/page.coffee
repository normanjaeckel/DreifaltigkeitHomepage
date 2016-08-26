angular.module 'dreifaltigkeithomepage.page', []

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
                  '<span ng-show="element.page.slug === slug">*</span>' +
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
        @slug = SlugParser.getSlug $stateParams
        Page.findAll()
        $scope.$watch(
            () ->
                Page.lastModified()
            () =>
                @rootElement =
                    page: {}
                    children: PageTree.getTree pages
                return
        )
        return
]

.controller 'PageCtrl', [
    '$scope'
    '$stateParams'
    'Page'
    'SlugParser'
    ($scope, $stateParams, Page, SlugParser) ->
        slug = SlugParser.getSlug $stateParams
        params =
            where:
                slug:
                    '===': slug
        Page.findAll(params)
        $scope.$watch(
            () ->
                Page.lastModified()
            () =>
                pages = Page.filter params
                @page = pages[0]
                return
        )
        return
]
