// Get all elements that have the data attribute from the widget set
document.querySelectorAll("[data-dj-cleavejs]").forEach(function(element) {
    // Parse JSON generated from widget data class into object
    let cleave_options = JSON.parse(element.getAttribute("data-dj-cleavejs"));
    // Pass options verbatim to Cleave constructor
    new Cleave(element, cleave_options);
});
