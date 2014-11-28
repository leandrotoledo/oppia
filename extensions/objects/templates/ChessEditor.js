oppia.directive('chessEditor', function($compile, warningsData) {
  return {
      link: function(scope, element, attrs) {
        scope.getTemplateUrl = function() {
          return OBJECT_EDITOR_TEMPLATES_URL + scope.$parent.objType;
        };
        $compile(element.contents())(scope);
      },
      restrict: 'E',
      scope: {},
      template: '<span ng-include="getTemplateUrl()"></span>',
      controller: ['$scope', '$attrs', function($scope, $attrs) {
        var cfg = {
          draggable: true,
          position: 'start',
          onChange: $scope.onChange
        };

        $scope.alwaysEditable = true;

        // make sure the editor partial is loaded, then laod chess board js and css
        $scope.$watch(
          function() { return angular.element('#chess-editor-board').length },
          function(newValue) {
            if (newValue)
              var board = new ChessBoard('chess-editor-board', cfg);
          }
        )

        // scope.onsubmit
      }]
    };
  }
);