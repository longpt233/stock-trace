package com.company.crawl.category;

import com.company.model.elements.TextBlock;
import com.company.model.elements.TextDocument;
import com.company.parse.ParseWebsite;
import com.company.parse.support.SeleniumCrawler;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class CrawlCategory {

    private List<Category> categories;

    public CrawlCategory(){
        categories = new ArrayList<>();
    }

    public void writeOut(String path) {
        BufferedWriter bw = null;
        try {
            bw = new BufferedWriter(new FileWriter(path));
            bw.flush();
            System.out.println("cate size = " + categories.size());
            for (Category it : categories) {
                bw.write(it + "\n");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            try {
                if (bw != null) {
                    bw.close();
                }
            } catch (Exception ex1) {
                ex1.printStackTrace();
            }
        }

    }

    public void crawl(String url){
        try {

            Document doc = Jsoup.connect(url)
                    .userAgent("Mozilla/5.0")
                    .timeout(60 * 1000)
                    .get();
            Elements data = doc.select("#js-screener-container > div.tv-screener__content-pane > table > tbody > tr");

            for (Element it : data) {
                String [] col = new String[7];
                for (int i =0;i<7;i++){
                    col[i] = it.select("td:nth-child("+(i+1)+")").text();
                }

                String[] urlCateSplit = it.select("td:nth-child(1) > div ").select("a").attr("href").split("\\/");
                String cateEng = urlCateSplit[urlCateSplit.length-1];

                Category category = new Category(col[0], cateEng, col[1], col[2], col[3] ,col[4], Integer.parseInt(col[5]), Integer.parseInt(col[6])  );
                categories.add(category);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }

    }

    public static void main(String[] args) {

        CrawlCategory crawlCategory = new CrawlCategory();
        crawlCategory.crawl("https://vn.tradingview.com/markets/stocks-vietnam/sectorandindustry-sector/");
        crawlCategory.writeOut("data/company/category.csv");

    }
}
