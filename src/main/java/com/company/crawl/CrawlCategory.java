package com.company.crawl;

import com.company.parse.support.SeleniumCrawler;

public class CrawlCategory {

    SeleniumCrawler seleniumCrawler ;

    public CrawlCategory(){
        seleniumCrawler = new SeleniumCrawler();
    }

    public void crawl(String url){

    }

    public static void main(String[] args) {

        CrawlCategory crawlCategory = new CrawlCategory();
        crawlCategory.crawl("");

    }
}
