$(document).ready(function() {
    // Hardcoded list of YouTube video IDs
    var videoIDs = [
        'dQw4w9WgXcQ', // Example video ID
        'M7lc1UVf-VE', // Another example video ID
        // Add more video IDs as needed
    ];

    // Function to shuffle an array
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    // Shuffle the videoIDs array
    shuffle(videoIDs);

    // Select the first video ID from the shuffled array
    var selectedVideoID = videoIDs[0];

    // Construct the YouTube embed URL
    var embedURL = `https://www.youtube.com/embed/${selectedVideoID}`;

    // Embed the video in the #videoPlayer div
    $('#videoPlayer').html(`<iframe width="560" height="315" src="${embedURL}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`);
});
