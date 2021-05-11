<?php

use DivarScraper\Scrapers\ExtractPosterLinks;

require __DIR__ . "/vendor/autoload.php";

// Take the scroll Timeout from the user
echo "Enter the scrollPage timeout(Default 3): ";
$scrollTimeout = intval(fgets(STDIN));
// Take the category URL from the user
echo "Enter the pageLoadTimeout timeout(Default 10): ";
$pageLoadTimeout = intval(fgets(STDIN));

// Create instance of ExtractPosterLinks Class
$extractPosterLinks = new ExtractPosterLinks($scrollTimeout, $pageLoadTimeout);
// Extract the posters link
$postersLink = $extractPosterLinks->getLinks();
