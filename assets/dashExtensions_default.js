window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(e) {
            if (e && e.points) {
                return e.points[0].x;
            }
            return null;
        }
    }
});