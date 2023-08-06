js_arrow_key_navigation = """
<!-- Arrow key navigation -->
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"></script>
<script type="text/javascript">
$(document).ready(function() {
    {
        document.onkeydown = function() {
            {
                var j = event.key
                if (j == "ArrowRight")
                    window.location = nextUrl
                else if (j == "ArrowLeft")
                    window.location = prevUrl
            }
        }
    }
});

$(document).ready(function() {
    {
        var nextPage = $("#next_page_link")
        var prevPage = $("#previous_page_link")
        nextUrl = nextPage.attr("href")
        prevUrl = prevPage.attr("href")
    }
});

$(document).ready(function() {
    var textContainer = document.getElementById("text-container");
    if (textContainer.clientHeight >= textContainer.scrollHeight)
        $(".show-more-button").addClass('hide')
});

function showMore() {{
    $('#text-container').addClass('show-all')
    $(".show-more-button").addClass('hide')
}}

</script>
"""
