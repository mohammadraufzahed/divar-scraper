<?php

namespace DivarScraper\Scrapers;

use Facebook\WebDriver\Exception\UnknownErrorException;
use Facebook\WebDriver\Exception\WebDriverCurlException;
use Facebook\WebDriver\Firefox\FirefoxDriver;
use Facebook\WebDriver\WebDriverBy;
use URL\Normalizer;

require __DIR__ . '/../../vendor/autoload.php';

/**
 * Extract the posters link
 */
class ExtractPosterLinks
{
    private object $driver;
    private string $categoryLink;
    private array $links = array();
    private int $timeout;

    public function __construct(int $scrollTimeout, int $pageLoadTimeout)
    {
        // Initial the web browser
        $this->driver = FirefoxDriver::start();
        // Take the category URL from the user 
        echo "Enter the category link: ";
        $this->categoryLink = rtrim(fgets(STDIN));
        // Load the category URL
        try {
            $this->driver->get($this->categoryLink);
        } catch (WebDriverCurlException $e) {
            print("Category link dosent load");
        }
        // 
        $this->driver->manage()->timeouts()->implicitlyWait((empty($pageLoadTimeout)) ? 10 : $pageLoadTimeout);
        // Assign the number to the timeout variable
        $this->timeout = (empty($scrollTimeout)) ? 3 : $scrollTimeout;
    }

    /***
     * Start the Links scraper
     * @return void
     */
    private function startScraping(): void
    {
        // Store the pause time
        $timeout = $this->timeout;
        // Select the posters box
        $postersBoxContainer = $this->driver->findElement(WebDriverBy::cssSelector('div.browse-post-list'));
        // Store the styles
        $nowStyle = $postersBoxContainer->getAttribute('style');
        $lastStyle = '';
        // Scroll height size
        $scrollHeight = 3104.5;
        // Start to scrap the data
        while ($nowStyle != $lastStyle) {
            // Grab the data
            $posters = $postersBoxContainer->findElements(WebDriverBy::cssSelector('div.post-card-item a'));
            // Iterate over the scraped data
            foreach ($posters as $poster) {
                // Grab the poster link and normalize it
                $link = 'https://divar.ir' . $poster->getAttribute('href');
                $normalizer = new Normalizer($link);
                $link = $normalizer->normalize();
                // Check the link that exists in the links list
                if (!in_array($link, $this->links)) {
                    // If it doesn't exist, append it to the array
                    array_push($this->links, $link);
                }
            }
            // Scroll the page
            $this->driver->executeScript("window.scrollTo({top: $scrollHeight, left: 0, behavior: 'smooth'});");
            // Increase the scroll_height variable
            $scrollHeight += 3104.5;
            // Make the app goes to sleep
            sleep($timeout);
            // Refresh the styles
            $lastStyle = $nowStyle;
            $nowStyle = $postersBoxContainer->getAttribute('style');
        }
        // Echo how many links scraped
        $linksLength = sizeof($this->links);
        echo ("Scraped $linksLength Links\n");
        // Terminate the browser
        $this->driver->quit();
    }
    /**
     * Get the posters link
     * @return array
     */
    public function getLinks(): array
    {
        $this->startScraping();
        return $this->links;
    }
}
