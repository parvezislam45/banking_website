$(document).ready(function() {
    var clickCount = 0;
    var clickCountElement = $('#clickCount');
    var clickButton = $('#clickButton');
    
    clickButton.click(function() {
        clickCount++;
        clickCountElement.text(clickCount);
    });
});

