(function() {
    document.addEventListener("DOMContentLoaded", (function() {
        var doc_hostname = document.location.hostname
        var alt_doc_hostname = ""
        if (doc_hostname.startsWith("www.")) {
            alt_doc_hostname = doc_hostname.substring(4)
        } else {
            alt_doc_hostname = "www." + doc_hostname
        }
        var hostname_variants = [
            doc_hostname,
            alt_doc_hostname,
            "anhel.in",
            "www.anhel.in"
        ] 
        console.log(hostname_variants)
        var all_md_blocks = document.getElementsByClassName("md")
        for (var i = 0; i < all_md_blocks.length; ++i) {
            var block = all_md_blocks[i]
            var all_links = block.getElementsByTagName("a")
            for (var j = 0; j < all_links.length; ++j) {
                var link = all_links[j]
                if (link.hasAttribute("href")) {
                    if (link.hasAttribute("target")) {
                        if (link.getAttribute("target") == "_blank") {
                            continue
                        }
                    }
                    console.log("Processing link", link.hostname)
                    if (link.hostname && link.hostname.length > 0) {
                        var need_target = true
                        for (var k = 0; k < hostname_variants.length; ++k) {
                            if (link.hostname == hostname_variants[k]) {
                                need_target = false
                                break
                            }
                        }
                        if (need_target) {
                            link.setAttribute("target", "_blank")
                        }
                    }
                }
            }
        }
    }))
})();