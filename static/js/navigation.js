(function() {
    const sideWidth = "100%";

    document.addEventListener("DOMContentLoaded", (function() {
        function closeNav() {
            var slide = document.getElementById("menu-slide")
            slide.style.marginLeft = "-" + sideWidth;
            document.documentElement.style.overflow = 'scroll';
            document.body.scroll = "yes";
        }

        function openNav() {
            var slide = document.getElementById("menu-slide")
            slide.style.marginLeft = "0"
            document.documentElement.style.overflow = 'hidden';
            document.body.scroll = "no";
        }

        document.getElementById("top-menu-button").addEventListener("click", (function(event) {
            event.preventDefault();
            openNav();
        }))

        document.getElementById("menu-close-button").addEventListener("click", (function(event) {
            event.preventDefault();
            closeNav();
        }))

        var listItems = document.querySelectorAll("#menu-slide>nav>ul>li>a")
        for (var i = 0; i < listItems.length; ++i) {
            var item = listItems[i]
            item.addEventListener("click", closeNav)
        }
    }))
})();