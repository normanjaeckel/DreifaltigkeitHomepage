angular.module 'dreifaltigkeithomepage.page', []

.controller 'PageCtrl', [
    '$scope'
    '$stateParams'
    'Page'
    ($scope, $stateParams, Page) ->
        index = $stateParams.slug.lastIndexOf('/')
        if index == -1
            slug = $stateParams.slug
        else
            index++
            slug = $stateParams.slug.slice index
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


        @stateParams = $stateParams
        return
]
